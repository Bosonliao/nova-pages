"""
補飲料店評分 - 用 Playwright 爬 Google Maps
目標：台東-drinks-final.json (6家) + 澎湖-drinks-final.json (1家) = 最多5家
"""
from playwright.sync_api import sync_playwright
import json
import time
import sys
import io
import re
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATA_DIR = 'C:/Users/USER/.openclaw/workspace/nova-pages/data'

def load_shops(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, encoding='utf-8') as f:
        return json.load(f), path

def scrape_rating(query):
    """搜尋 Google Maps 並提取評分和評論數"""
    result = {"rating": None, "reviews": None}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        url = f"https://www.google.com/maps/search/{query}"
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
        except Exception as e:
            print(f"  頁面載入超時，繼續嘗試...")
        
        time.sleep(5)
        
        # 取得完整頁面內容
        try:
            content = page.inner_text("body")
        except:
            content = ""
        lines = [l.strip() for l in content.split("\n") if l.strip()]
        
        # 找評分 - Google Maps 評分通常顯示為 "4.5" 單獨一行
        for i, line in enumerate(lines):
            if re.match(r'^\d\.\d$', line):
                result["rating"] = float(line)
                # 往下找評論數
                for j in range(i+1, min(i+10, len(lines))):
                    next_line = lines[j]
                    m = re.search(r'\(([\d,]+)\)', next_line)
                    if m:
                        result["reviews"] = int(m.group(1).replace(',', ''))
                        break
                    m = re.search(r'([\d,]+)\s*(?:reviews|則評論|篇評論)', next_line)
                    if m:
                        result["reviews"] = int(m.group(1).replace(',', ''))
                        break
                break
        
        # 嘗試 aria-label
        if result["rating"] is None:
            try:
                rating_elements = page.query_selector_all('[aria-label*="星"]')
                for el in rating_elements:
                    label = el.get_attribute('aria-label')
                    if label:
                        m = re.search(r'(\d\.\d)', label)
                        if m:
                            result["rating"] = float(m.group(1))
                            m2 = re.search(r'([\d,]+)\s*(?:則|篇|個)?(?:評論|評分|review)', label)
                            if m2:
                                result["reviews"] = int(m2.group(1).replace(',', ''))
                            break
            except:
                pass
        
        # 嘗試 span
        if result["rating"] is None:
            try:
                spans = page.query_selector_all('span')
                for span in spans:
                    text = span.inner_text().strip()
                    if re.match(r'^\d\.\d$', text):
                        result["rating"] = float(text)
                        break
            except:
                pass
        
        # 嘗試找評論數
        if result["rating"] is not None and result["reviews"] is None:
            try:
                all_elements = page.query_selector_all('span, div, button')
                for el in all_elements:
                    text = el.inner_text().strip()
                    m = re.search(r'\(([\d,]+)\)', text)
                    if m:
                        val = int(m.group(1).replace(',', ''))
                        if val > 0:
                            result["reviews"] = val
                            break
                    m = re.search(r'([\d,]+)\s*(?:則評論|篇評論|reviews)', text)
                    if m:
                        result["reviews"] = int(m.group(1).replace(',', ''))
                        break
            except:
                pass
        
        print(f"  評分: {result['rating']}, 評論數: {result['reviews']}")
        if result["rating"] is None:
            print(f"  未找到評分，前20行：")
            for line in lines[:20]:
                if len(line) > 1:
                    print(f"    {line}")
        
        browser.close()
    
    return result

def update_shop_rating(filepath, shops, shop_index, rating, reviews):
    """更新 JSON 檔中特定店家的 rating 和 reviews"""
    shops[shop_index]["rating"] = rating
    shops[shop_index]["reviews"] = reviews
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(shops, f, ensure_ascii=False, indent=2)
    print(f"  已更新: rating={rating}, reviews={reviews}")

# ===== 主程式 =====
# 選擇要處理的檔案和店家
targets = [
    ("台東-drinks-final.json", 0, "50嵐", "臺東市"),
    ("台東-drinks-final.json", 1, "鮮茶道", "臺東市"),
    ("台東-drinks-final.json", 3, "鮮茶道", "綠島鄉"),
    ("台東-drinks-final.json", 4, "鮮茶道", "池上鄉"),
    ("台東-drinks-final.json", 5, "鮮茶道", "關山鎮"),
]

# 按檔案分組
from collections import defaultdict
file_groups = defaultdict(list)
for filename, idx, name, area in targets:
    file_groups[filename].append((idx, name, area))

updated_count = 0
results_log = []

for filename, shop_list in file_groups.items():
    print(f"\n=== 處理 {filename} ===")
    shops, filepath = load_shops(filename)
    
    for idx, name, area in shop_list:
        query = f"{name} {area} 台灣"
        print(f"\n搜尋: {query} (index={idx})")
        
        try:
            r = scrape_rating(query)
            if r["rating"] is not None:
                update_shop_rating(filepath, shops, idx, r["rating"], r["reviews"] or 0)
                updated_count += 1
                results_log.append(f"  ✓ {name} ({area}): rating={r['rating']}, reviews={r['reviews']}")
            else:
                results_log.append(f"  ✗ {name} ({area}): 未找到評分，跳過")
        except Exception as e:
            print(f"  錯誤: {e}")
            results_log.append(f"  ✗ {name} ({area}): 錯誤 {e}")
        
        time.sleep(3)
        # 重新載入以防檔案被修改
        shops, filepath = load_shops(filename)

print(f"\n=== 結果摘要 ===")
print(f"更新了 {updated_count} 家店")
for log in results_log:
    print(log)