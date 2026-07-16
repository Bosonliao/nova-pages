"""找出下一個沒有菜色的餐廳（全部縣市），傳回名稱和基本資訊"""
import json, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data_dir = 'C:/Users/USER/.openclaw/workspace/nova-pages/data'
all_need = []

for fn in os.listdir(data_dir):
    if fn.endswith('.json') and fn not in ['meta.json', 'cities.json', 'nightmarkets.json']:
        path = os.path.join(data_dir, fn)
        try:
            city = json.load(open(path, 'r', encoding='utf-8'))
            food = city.get('food', [])
            county = fn.replace('.json', '')
            for r in food:
                if not r.get('dishes') and not r.get('dishes_searched'):
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

if not all_need:
    print('ALL_DONE')
    sys.exit(0)

r = all_need[0]
print(f'NEXT_RESTAURANT:{r["name"]}')
print(f'COUNTY:{r["county"]}')
print(f'AREA:{r["area"]}')
print(f'RATING:{r["rating"]}')
print(f'REVIEWS:{r["reviews"]}')
print(f'CATEGORIES:{",".join(r["categories"])}')
print(f'REMAINING:{len(all_need)}')