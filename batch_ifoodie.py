"""
批量搜尋餐廳推薦菜色 - 使用 ifoodie 網站
"""
import sys, io, json, os, time, re, urllib.request, urllib.parse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data_dir = 'C:/Users/USER/.openclaw/workspace/nova-pages/data'

def get_next_restaurants(n=50):
    """取得前 n 個需要菜色的餐廳"""
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
                        all_need.append({
                            'name': r.get('name', ''),
                            'area': r.get('area', ''),
                            'reviews': r.get('reviews', 0),
                            'rating': r.get('rating', 0),
                            'county': county,
                            'categories': r.get('categories', [])
                        })
            except:
                pass
    all_need.sort(key=lambda x: x.get('reviews') or 0, reverse=True)
    return all_need[:n], len(all_need)

def save_dishes(county, restaurant_name, dishes):
    """存菜色到 JSON"""
    path = os.path.join(data_dir, f'{county}.json')
    data = json.load(open(path, 'r', encoding='utf-8'))
    for f in data['food']:
        if f['name'] == restaurant_name:
            f['dishes'] = dishes
            break
    json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

def fetch_url(url, timeout=10):
    """Fetch URL with proper headers"""
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None

def search_ifoodie(restaurant_name, area=''):
    """Search for restaurant on ifoodie and get recommended dishes"""
    query = restaurant_name
    search_url = f"https://ifoodie.tw/search?q={urllib.parse.quote(query)}"
    html = fetch_url(search_url)
    if not html:
        return None
    
    # Find restaurant page URLs
    restaurant_urls = re.findall(r'/restaurant/([a-f0-9]+-[^\s"\']+)', html)
    if not restaurant_urls:
        # Try simpler pattern
        restaurant_urls = re.findall(r'/restaurant/([a-f0-9]+)', html)
    
    if not restaurant_urls:
        return None
    
    # Get the first restaurant page
    for rid in restaurant_urls[:3]:
        rest_url = f"https://ifoodie.tw/restaurant/{rid}"
        rest_html = fetch_url(rest_url)
        if not rest_html:
            continue
        
        # Extract recommended dishes (推薦菜色)
        dishes = set()
        
        # Pattern 1: 🌟菜名
        for m in re.finditer(r'🌟(.+?)(?:\n|$)', rest_html):
            dish = m.group(1).strip()
            if len(dish) > 1 and len(dish) < 20:
                dishes.add(dish)
        
        # Pattern 2: 推薦菜色 section
        menu_section = re.search(r'推薦菜色(.*?)(?:份量|環境|注意|價位|$$)', rest_html, re.DOTALL)
        if menu_section:
            for m in re.finditer(r'([\u4e00-\u9fffA-Za-z0-9]{2,15}(?:飯|麵|湯|粥|餅|糕|飲|茶|冰|肉|魚|蝦|蟹|雞|鴨|牛|豬|羊|蔬|果|莓|奶|酒|卷|壽司|沙拉|鍋|串|烤|煎|蒸|煮|炒|炸|滷|羹|粿|粽|糰|丸|餃|捲|拼盤|套餐|組合|握壽司|寒天|剉冰|冰沙|奶酪|布丁|蛋糕|吐司|三明治))', menu_section.group(1)):
                dishes.add(m.group(1))
        
        if dishes:
            return list(dishes)[:5]
    
    return None

# Main
restaurants, total = get_next_restaurants(50)
print(f"Total remaining: {total}")
print(f"Processing: {len(restaurants)}")

success = 0
failed = 0
failed_list = []

for i, r in enumerate(restaurants):
    name = r['name']
    county = r['county']
    area = r.get('area', '')
    
    # Skip non-restaurant entries (markets, streets, malls)
    skip_keywords = ['老街', '市場', '購物中心', '百貨', '夜市', '教堂', '周邊', '必吃', '陶瓷']
    if any(kw in name for kw in skip_keywords):
        print(f"[{i+1}/{len(restaurants)}] SKIP: {name} (not a restaurant)")
        save_dishes(county, name, [])
        continue
    
    print(f"[{i+1}/{len(restaurants)}] Searching: {name} ({county})")
    
    dishes = search_ifoodie(name, area)
    
    if dishes and len(dishes) >= 2:
        save_dishes(county, name, dishes)
        print(f"  -> SAVED: {dishes}")
        success += 1
    else:
        print(f"  -> FAILED: no dishes found")
        failed += 1
        failed_list.append(f"{name} ({county})")
    
    time.sleep(0.5)  # Be polite

print(f"\n=== RESULTS ===")
print(f"Success: {success}")
print(f"Failed: {failed}")
print(f"Skipped: {len(restaurants) - success - failed}")
print(f"Total remaining before: {total}")
print(f"Total remaining after: {total - success - failed - (len(restaurants) - success - failed)}")
if failed_list:
    print(f"\nFailed restaurants:")
    for f in failed_list:
        print(f"  - {f}")