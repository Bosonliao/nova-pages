import json, sys, io, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

# Check for duplicate coordinates
coord_map = {}
for f in foods:
    if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or [])):
        lat = f.get('lat')
        lng = f.get('lng')
        if lat and lng:
            key = f'{round(lat,4)},{round(lng,4)}'
            if key not in coord_map:
                coord_map[key] = []
            coord_map[key].append(f)

print('=== 重複座標的店家 ===')
for key, shops in coord_map.items():
    if len(shops) > 1:
        print(f'\n  ({key}) — {len(shops)} 家：')
        for s in shops:
            print(f'    {s["name"]:30s} | addr: {s.get("address","無")}')
