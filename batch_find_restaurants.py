"""批次找出需要補菜色的餐廳，跳過百貨/夜市等"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data_dir = 'C:/Users/USER/.openclaw/workspace/nova-pages/data'
all_need = []

skip_keywords = ['百貨', '購物中心', '夜市', '市場', '商場', 'outlet', 'Outlet', '美食街']

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
                        'rating': r.get('rating', 0),
                        'county': county,
                        'categories': r.get('categories', [])
                    })
        except:
            pass

all_need.sort(key=lambda x: x.get('reviews') or 0, reverse=True)
print(f'TOTAL_NEED: {len(all_need)}')
for i, r in enumerate(all_need[:50]):
    print(f'{i+1}. {r["name"]} | {r["county"]} | {r["area"]} | reviews={r["reviews"]} | cat={",".join(r["categories"])}')