"""
RPA 自動查 Google Maps 店家資訊（評分、評論數、座標）
用 Playwright 模擬人工查詢，不需要 LLM
"""
from playwright.sync_api import sync_playwright
import json
import time
import sys
import io
import re
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def scrape_shop_info(query):
    """查詢 Google Maps，回傳店家資訊"""
    result = {'query': query, 'rating': None, 'reviews': None, 'lat': None, 'lng': None, 'address': None}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = f"https://www.google.com/maps/search/{query}"
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)
        
        # 嘗試點擊第一個搜尋結果（a role="article" 或 .placeResult）
        try:
            first_result = page.query_selector('a[role="article"]')
            if first_result:
                first_result.click()
                time.sleep(2)
        except:
            pass
        
        # 取得當前 URL（點進店家後通常含座標）
        current_url = page.url
        # 解析 URL 中的座標，多種格式
        coord_match = re.search(r'@(-?[\d.]+),(-?[\d.]+)', current_url)
        if coord_match:
            result['lat'] = float(coord_match.group(1))
            result['lng'] = float(coord_match.group(2))
        else:
            # 嘗試從 data URL 或 place ID 解析
            # 格式: !3d24.9106!4d121.1412
            coord_match2 = re.search(r'!3d(-?[\d.]+)!4d(-?[\d.]+)', current_url)
            if coord_match2:
                result['lat'] = float(coord_match2.group(1))
                result['lng'] = float(coord_match2.group(2))
        result['url'] = current_url
        # Debug: 印 URL 方便除錯
        print(f"  [debug] URL: {current_url[:200]}")
        
        # 截取頁面文字
        content = page.inner_text("body")
        lines = [l.strip() for l in content.split("\n") if l.strip()]
        
        # 找評分（格式: 4.6 或 4.6 顆星）
        for line in lines[:30]:
            # 評分模式: "4.6" 單獨出現在前面幾行
            if re.match(r'^(\d\.\d)$', line):
                result['rating'] = float(line)
                break
        
        # 找評論數（格式: (170) 或 170 則評論）
        for line in lines[:40]:
            m = re.match(r'^\((\d[\d,]*)\)$', line)
            if m:
                result['reviews'] = int(m.group(1).replace(',', ''))
                break
            m2 = re.match(r'^(\d[\d,]*)\s*則評論', line)
            if m2:
                result['reviews'] = int(m2.group(1).replace(',', ''))
                break
        
        # 找地址
        for line in lines[:50]:
            if any(k in line for k in ['號', '路', '街', '巷', '弄', '區']):
                if len(line) > 10 and len(line) < 80:
                    result['address'] = line
                    break
        
        # 如果沒抓到座標，用地址查 Nominatim
        if not result['lat'] and result['address']:
            try:
                addr_url = f"https://nominatim.openstreetmap.org/search?q={result['address']}&format=json&limit=1"
                page2 = browser.new_page()
                page2.goto(addr_url, wait_until="domcontentloaded", timeout=15000)
                time.sleep(1)
                geo_content = page2.inner_text('body')
                geo_data = json.loads(geo_content)
                if geo_data:
                    result['lat'] = float(geo_data[0]['lat'])
                    result['lng'] = float(geo_data[0]['lon'])
                page2.close()
            except:
                pass
        
        browser.close()
    
    return result

def update_json(city, shops_to_update):
    """更新 JSON 資料庫"""
    filepath = os.path.join(DATA_DIR, f'{city}.json')
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated = 0
    for shop in shops_to_update:
        # 找到對應的店
        for f in data['food']:
            if f['name'] == shop['original_name'] and f.get('area') == shop.get('area'):
                if shop.get('rating') and not f.get('rating'):
                    f['rating'] = shop['rating']
                if shop.get('reviews') and not f.get('reviews'):
                    f['reviews'] = shop['reviews']
                if shop.get('lat') and not f.get('lat'):
                    f['lat'] = shop['lat']
                if shop.get('lng') and not f.get('lng'):
                    f['lng'] = shop['lng']
                if shop.get('address') and not f.get('address'):
                    f['address'] = shop['address']
                updated += 1
                break
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return updated

def batch_scrape_city(city, max_count=10, delay=3):
    """批次查詢某城市缺資料的店"""
    filepath = os.path.join(DATA_DIR, f'{city}.json')
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 找出缺評分或缺座標的店
    missing = []
    for shop in data['food']:
        no_rating = not shop.get('rating') or shop.get('rating') == 0
        no_gps = not shop.get('lat') or not shop.get('lng')
        if no_rating or no_gps:
            # 清理店名：去掉 │ | - 之後的 SEO 廢話
            clean_name = shop['name']
            for sep in ['│', '|', ' - ', '（', '(', '：']:
                if sep in clean_name:
                    clean_name = clean_name.split(sep)[0].strip()
            shop['_clean_name'] = clean_name[:20]  # 最多 20 字
            missing.append(shop)
    
    print(f"[{city}] 總共 {len(data['food'])} 家，缺資料 {len(missing)} 家")
    
    if not missing:
        print(f"[{city}] 沒有缺資料的店，跳過")
        return
    
    # 限制數量
    missing = missing[:max_count]
    print(f"[{city}] 將查詢前 {len(missing)} 家")
    
    results = []
    for i, shop in enumerate(missing):
        name = shop.get('_clean_name', shop['name'])
        area = shop.get('area', '')
        query = f"{name} {area} 台灣"
        print(f"\n[{i+1}/{len(missing)}] 查詢: {query}")
        
        try:
            info = scrape_shop_info(query)
            info['original_name'] = shop['name']
            info['area'] = area
            results.append(info)
            print(f"  → 評分:{info['rating']} 評論:{info['reviews']} 座標:{info['lat']},{info['lng']}")
            if info['address']:
                print(f"  → 地址:{info['address']}")
        except Exception as e:
            print(f"  → 查詢失敗: {e}")
            results.append({'original_name': name, 'area': area})
        
        time.sleep(delay)
    
    # 更新 JSON
    updated = update_json(city, results)
    print(f"\n[{city}] 更新了 {updated} 家店")

if __name__ == "__main__":
    # 預設查桃園，前 10 家
    city = sys.argv[1] if len(sys.argv) > 1 else 'taoyuan'
    max_count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    batch_scrape_city(city, max_count)