"""
菜色補充 v8 — 用 web_fetch 抓 DuckDuckGo Lite，然後用 LLM 提取菜色
策略：先把 30 家餐廳的搜尋結果全部抓下來，再一次性分析
"""
import json, os, sys, io, re, time, urllib.parse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data_dir = 'C:/Users/USER/.openclaw/workspace/nova-pages/data'

skip_keywords = ['百貨', '購物中心', '夜市', '市場', '商場', 'outlet', 'Outlet', '美食街',
                 '老街', '商圈', '一中街', '周邊小吃', '文化園區', '高跟鞋教堂']

def get_restaurants_need_dishes(top_n=30):
    all_need = []
    for fn in os.listdir(data_dir):
        if fn.endswith('.json') and fn not in ['meta.json', 'cities.json', 'nightmarkets.json']:
            path = os.path.join(data_dir, fn)
            try:
                city = json.load(open(path, 'r', encoding='utf-8'))
                food = city.get('food', [])
                county = fn.replace('.json', '')
                for r in food:
                    if not r.get('dishes'):
                        name = r.get('name', '')
                        if any(kw in name for kw in skip_keywords):
                            continue
                        all_need.append({
                            'name': name,
                            'area': r.get('area', ''),
                            'reviews': r.get('reviews', 0),
                            'county': county,
                            'categories': r.get('categories', [])
                        })
            except:
                pass
    all_need.sort(key=lambda x: x.get('reviews') or 0, reverse=True)
    return all_need[:top_n]

def extract_dishes_from_ddg_text(text, restaurant_name):
    """從 DuckDuckGo Lite 搜尋結果純文字中提取菜色"""
    dishes = set()
    
    # 去除餐廳名稱本身
    name_clean = restaurant_name.split('(')[0].strip()
    
    # 找「必點」「招牌」附近的菜名
    # DuckDuckGo Lite 的搜尋結果摘要通常包含 "招牌的XXX" 或 "必吃XXX" 等
    
    patterns = [
        # 「招牌的XXX和YYY」
        r'招牌[的的是]?([\u4e00-\u9fff]{2,15}[飯湯麵餃肉雞魚蝦蟹鍋糕冰茶粥捲排串豆腐肝腸粽餅粄羹酥])',
        # 「必吃/必點XXX」
        r'必[吃點]([\u4e00-\u9fff]{2,15}[飯湯麵餃肉雞魚蝦蟹鍋糕冰茶粥捲排串豆腐肝腸粽餅粄羹酥])',
        # 「推薦的XXX」
        r'推薦[的的是]?([\u4e00-\u9fff]{2,15}[飯湯麵餃肉雞魚蝦蟹鍋糕冰茶粥捲排串豆腐肝腸粽餅粄羹酥])',
        # 「人氣XXX」
        r'人氣([\u4e00-\u9fff]{2,15}[飯湯麵餃肉雞魚蝦蟹鍋糕冰茶粥捲排串豆腐肝腸粽餅粄羹酥])',
        # 「XXX是必點/必吃/招牌」
        r'([\u4e00-\u9fff]{2,15}[飯湯麵餃肉雞魚蝦蟹鍋糕冰茶粥捲排串豆腐肝腸粽餅粄羹酥])[是就]?(?:必點|必吃|招牌|推薦)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for m in matches[:5]:
            m = m.strip()
            if 2 <= len(m) <= 20 and m != name_clean:
                dishes.add(m)
    
    # 也找「黑金」「黃金」等特殊菜名
    special_patterns = [
        r'(黑金[\u4e00-\u9fff]{1,10})',
        r'(黃金[\u4e00-\u9fff]{1,10})',
        r'(招牌[\u4e00-\u9fff]{2,10}[飯湯麵餃肉雞魚蝦蟹鍋糕冰茶粥捲排串豆腐肝腸粽餅粄羹酥])',
    ]
    
    for pattern in special_patterns:
        matches = re.findall(pattern, text)
        for m in matches[:3]:
            m = m.strip()
            if len(m) >= 3 and len(m) <= 20:
                dishes.add(m)
    
    # 過濾垃圾
    garbage = {'at DuckDuckGo', 'DuckDuckGo', '推薦 招牌', '招牌', '推薦', '必點', '必吃'}
    dishes = {d for d in dishes if d not in garbage and 'DuckDuckGo' not in d}
    
    return list(dishes)[:5]

# 主程式 — 先把搜尋結果存成檔案，再讓 Nova 分析
restaurants = get_restaurants_need_dishes(30)
print(f'處理 {len(restaurants)} 家餐廳')
print('---')

import requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

all_search_results = {}

for i, r in enumerate(restaurants):
    name = r['name']
    county = r['county']
    area = r['area']
    
    query = f'{name} {area} 必點 推薦 招牌' if area else f'{name} 必點 推薦 招牌'
    encoded = urllib.parse.quote(query)
    url = f'https://lite.duckduckgo.com/lite/?q={encoded}'
    
    print(f'{i+1}/{len(restaurants)} 搜尋: {name}')
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        # 去掉 HTML tags
        text = re.sub(r'<[^>]+>', '\n', resp.text)
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'  +', ' ', text)
        
        # 只取搜尋結果摘要部分（去掉導航和頁尾）
        # DuckDuckGo Lite 的結果在 "at DuckDuckGo" 之後
        results_text = text
        
        all_search_results[name] = {
            'county': county,
            'area': area,
            'text': results_text[:5000]  # 只存前 5000 字
        }
        
        dishes = extract_dishes_from_ddg_text(results_text, name)
        print(f'  提取菜色: {dishes}')
        
        if dishes:
            # 存入 JSON
            path = os.path.join(data_dir, f'{county}.json')
            data = json.load(open(path, 'r', encoding='utf-8'))
            for f in data.get('food', []):
                if f.get('name') == name:
                    f['dishes'] = dishes
                    break
            json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
            print(f'  已存入 {county}.json')
        
    except Exception as e:
        print(f'  ERROR: {e}')
    
    time.sleep(3)

# 把所有搜尋結果存成檔案供 Nova 分析
with open(os.path.join(data_dir, 'search_results_temp.json'), 'w', encoding='utf-8') as f:
    json.dump(all_search_results, f, ensure_ascii=False, indent=2)

print('---')
print('搜尋結果已存成 search_results_temp.json')