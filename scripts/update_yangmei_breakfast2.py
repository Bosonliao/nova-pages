"""
Update ratings/reviews for 10 more Yangmei breakfast shops
"""
import json, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')

BREAKFAST_DATA = [
    ("楊梅無名早餐店", "桃園市楊梅區大平街51號", 24.91355, 121.14312, 4.0, 571),
    ("里歐歐式早午餐 楊梅金德店", "桃園市楊梅區金德路16號", 24.91612, 121.14512, 4.7, 194),
    ("朝氣美濃商行 楊梅楊新店", "桃園市楊梅區楊新路56號", 24.91421, 121.14588, 4.2, 173),
    ("饅旺早餐店", "桃園市楊梅區新農街463號", 24.91012, 121.15855, 4.7, 201),
    ("台灣第二代飯糰", "桃園市楊梅區大成路22號", 24.91421, 121.14588, 4.6, 78),
    ("早餐蛋包飯", "桃園市楊梅區楊新路22號", 24.91433, 121.14591, 4.6, 25),
    ("我想想咖啡早午餐", "桃園市楊梅區光前街46號", 24.91425, 121.14488, 4.3, 2014),
    ("酥皮君 楊梅創始店", "桃園市楊梅區新農街1-1號", 24.91032, 121.15786, 4.5, 12),
    ("楊梅大成路蛋餅飯糰", "桃園市楊梅區大成路33號", 24.91386, 121.14583, 4.3, 465),
    ("楊梅無名傳統早餐", "桃園市楊梅區新成路145號", 24.91185, 121.14652, 4.1, 9),
]

# === Update taoyuan.json ===
data = json.load(open('data/taoyuan.json', 'r', encoding='utf-8'))
foods = data.get('food', [])

json_updated = 0
json_added = 0

for name, addr, lat, lng, rating, reviews in BREAKFAST_DATA:
    found = False
    jn = name.replace(' ', '').replace('#', '').replace('.', '').replace('-', '').replace('（', '').replace('）', '')
    for f in foods:
        fn = (f.get('name') or '').replace(' ', '').replace('#', '').replace('.', '').replace('-', '').replace('（', '').replace('）', '')
        if fn == jn or jn in fn or fn in jn:
            f['lat'] = lat
            f['lng'] = lng
            f['address'] = addr
            f['rating'] = rating
            f['reviews'] = reviews
            f['name'] = name
            if '早餐' not in f.get('categories', []):
                f.setdefault('categories', []).append('早餐')
            json_updated += 1
            found = True
            print(f'  ✅ {name} → ★{rating} ({reviews}則)')
            break
    
    if not found:
        foods.append({
            "name": name,
            "place_id": "",
            "lat": lat,
            "lng": lng,
            "rating": rating,
            "reviews": reviews,
            "address": addr,
            "area": "楊梅區",
            "categories": ["早餐"],
            "description": ""
        })
        json_added += 1
        print(f'  🆕 {name} → ★{rating} ({reviews}則)')

data['food'] = foods
with open('data/taoyuan.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\ntaoyuan.json updated: {json_updated}, added: {json_added}')
