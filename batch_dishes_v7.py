"""
菜色補充批次處理 v7 — 使用 DuckDuckGo Lite 搜尋
DuckDuckGo Lite 版回傳純文字搜尋結果，可以被 web_fetch 抓到
"""
import json, os, sys, io, re, time, urllib.parse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data_dir = 'C:/Users/USER/.openclaw/workspace/nova-pages/data'

skip_keywords = ['百貨', '購物中心', '夜市', '市場', '商場', 'outlet', 'Outlet', '美食街',
                 '老街', '商圈', '一中街', '周邊小吃', '文化園區', '高跟鞋教堂']

def get_restaurants_need_dishes(top_n=30):
    """找出需要補菜色的餐廳"""
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

def search_dishes_ddg(restaurant_name, area=''):
    """用 DuckDuckGo Lite 搜尋菜色"""
    query = f'{restaurant_name} {area} 必點 推薦 招牌' if area else f'{restaurant_name} 必點 推薦 招牌'
    encoded = urllib.parse.quote(query)
    url = f'https://lite.duckduckgo.com/lite/?q={encoded}'
    
    # 用 web_fetch 的方式 — 這裡用 requests
    import requests
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        text = resp.text
        
        # DuckDuckGo Lite 回傳的結果是 HTML，包含搜尋結果摘要
        # 去掉 HTML tags
        clean = re.sub(r'<[^>]+>', '\n', text)
        clean = re.sub(r'\n+', '\n', clean)
        clean = re.sub(r'  +', ' ', clean)
        
        # 提取菜色
        dishes = set()
        
        # 從搜尋結果摘要中提取菜色
        # 常見模式：「必點」「招牌」「必吃」後面跟菜名
        patterns = [
            r'必點[：: ]+([^。\n,，！!？?；;（(]{2,25})',
            r'招牌[：: ]+([^。\n,，！!？?；;（(]{2,25})',
            r'必吃[：: ]+([^。\n,，！!？?；;（(]{2,25})',
            r'推薦[：: ]+([^。\n,，！!？?；;（(]{2,25})',
            r'人氣[：: ]+([^。\n,，！!？?；;（(]{2,25})',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, clean)
            for m in matches[:3]:
                m = m.strip()
                if 2 <= len(m) <= 20 and not any(x in m for x in 
                    ['我們', '這家', '這間', '可以', '比較', '非常', '覺得', '真的',
                     '一下', '口感', '味道', '好吃', '不錯', '地址', '電話', '營業',
                     '捷運', '公車', '停車', '價格', '價位', '消費', '每人', '低消',
                     '點了', '吃了', '朋友', '今天', '這次', '第一次', '菜單']):
                    dishes.add(m)
        
        # 也搜尋「黑金」「招牌」等前面是形容詞的菜名
        # 從搜尋摘要中找常見菜名格式
        food_keywords = ['飯', '湯', '麵', '餃', '肉', '雞', '魚', '蝦', '蟹', '鍋',
                        '糕', '冰', '茶', '粥', '捲', '排', '串', '豆腐', '肝', '腸',
                        '粽', '餅', '粄', '羹', '酥', '捲']
        
        # 找含有食物關鍵字的短語
        lines = clean.split('\n')
        for line in lines:
            line = line.strip()
            if 2 <= len(line) <= 20:
                if any(kw in line for kw in food_keywords):
                    # 確保看起來像菜名
                    if not any(x in line for x in ['地址', '電話', '營業', '捷運', '公車',
                         '停車', '價格', '價位', '消費', '店家', '餐廳', '位於', '推薦',
                         '今天', '這次', '可以', '非常', '真的', '朋友', '自己']):
                        dishes.add(line)
        
        return list(dishes)[:5]
    except Exception as e:
        print(f'  ERROR: {e}', file=sys.stderr)
        return []

# 主程式
restaurants = get_restaurants_need_dishes(30)
print(f'處理 {len(restaurants)} 家餐廳')
print(f'剩餘總數: {len(get_restaurants_need_dishes(99999))}')
print('---')

results = {}
for i, r in enumerate(restaurants):
    name = r['name']
    county = r['county']
    area = r['area']
    
    print(f'{i+1}/{len(restaurants)} 搜尋: {name} ({county})')
    
    dishes = search_dishes_ddg(name, area)
    
    if dishes:
        print(f'  找到菜色: {dishes}')
        results[name] = {'dishes': dishes, 'county': county}
    else:
        print(f'  未找到菜色，跳過')
        results[name] = {'dishes': [], 'county': county}
    
    # 存檔
    if dishes:
        path = os.path.join(data_dir, f'{county}.json')
        try:
            data = json.load(open(path, 'r', encoding='utf-8'))
            for f in data.get('food', []):
                if f.get('name') == name:
                    f['dishes'] = dishes
                    break
            json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
            print(f'  已存入 {county}.json')
        except Exception as e:
            print(f'  存檔失敗: {e}')
    
    time.sleep(3)  # 避免被擋

print('---')
print(f'完成: {sum(1 for v in results.values() if v["dishes"])}/{len(restaurants)}')
print(f'跳過: {sum(1 for v in results.values() if not v["dishes"])}/{len(restaurants)}')