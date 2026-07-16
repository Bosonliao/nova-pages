"""批量處理餐廳菜色補充腳本"""
import json, sys, io, os, time, subprocess
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

# Main
restaurants, total_remaining = get_next_restaurants(50)
print(f"Total remaining: {total_remaining}")
print(f"Processing: {len(restaurants)} restaurants")
print("---")

for i, r in enumerate(restaurants):
    name = r['name']
    county = r['county']
    area = r['area']
    print(f"\n[{i+1}/{len(restaurants)}] {name} | {county} | {area}")
    print(f"NAME:{name}")
    print(f"COUNTY:{county}")
    print(f"AREA:{area}")
    print("END_ITEM")

print("\n---DONE_LIST---")