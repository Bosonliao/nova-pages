import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

# Johnny's precise coordinates
updates = {
    "UG": (24.91266, 121.14441, "桃園市楊梅區大成路137號"),
    "自然湉": (24.91187, 121.14385, "桃園市楊梅區大成路205號"),
    "茗茗究市": (24.91386, 121.14583, "桃園市楊梅區大成路37號"),
    "茂昌草本茶": (24.91458, 121.14652, "桃園市楊梅區楊新路78號"),
    "花火禾茶": (24.91032, 121.15786, "桃園市楊梅區新農街357號"),
    "功夫茶": (24.91523, 121.18042, "桃園市楊梅區四維路90號"),
    "金茶伍": (24.91316, 121.17387, "桃園市楊梅區瑞溪路二段215號1樓"),
    "吾奶王": (24.91892, 121.18231, "桃園市楊梅區梅獅路二段95號"),
}

updated = 0
for f in foods:
    if f.get('area') != '楊梅區':
        continue
    name = f.get('name', '')
    for keyword, (lat, lng, addr) in updates.items():
        if keyword in name:
            old_lat = f.get('lat')
            old_lng = f.get('lng')
            f['lat'] = lat
            f['lng'] = lng
            if not f.get('address') or f['address'] == '':
                f['address'] = addr
            print(f'✅ {name}: ({old_lat},{old_lng}) -> ({lat},{lng})')
            updated += 1
            break

print(f'\nUpdated: {updated}')

# Also add 茂昌草本茶 as new store if not exists
exists = any('茂昌' in f.get('name','') for f in foods if f.get('area') == '楊梅區')
if not exists:
    foods.append({
        "name": "茂昌草本茶 楊梅楊新店",
        "place_id": "",
        "lat": 24.91458,
        "lng": 121.14652,
        "rating": 0,
        "reviews": 0,
        "address": "桃園市楊梅區楊新路78號",
        "area": "楊梅區",
        "categories": ["飲品"],
        "description": ""
    })
    print('Added: 茂昌草本茶 楊梅楊新店')

data['food'] = foods
with open('data/taoyuan.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Saved')
