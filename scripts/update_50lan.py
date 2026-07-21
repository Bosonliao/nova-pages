import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

# Johnny's 50嵐 data
shops_50lan = [
    ("50嵐 楊梅大成店", 24.91225, 121.14418, "桃園市楊梅區大成路160號"),
    ("50嵐 楊梅新農店", 24.90998, 121.15545, "桃園市楊梅區新農街265號"),
    ("50嵐 埔心中興店", 24.91421, 121.18567, "桃園市楊梅區中興路119號"),
    ("50嵐 楊梅萬大店", 24.91745, 121.17932, "桃園市楊梅區萬大路136號"),
]

existing_names = {f['name'] for f in foods if f.get('area') == '楊梅區'}

for name, lat, lng, addr in shops_50lan:
    found = False
    for f in foods:
        if f.get('area') == '楊梅區' and '50嵐' in f.get('name', ''):
            # Update existing
            if '大成' in name and '大成' in f['name']:
                f['lat'] = lat
                f['lng'] = lng
                f['address'] = addr
                print(f'✅ Updated: {f["name"]} -> ({lat}, {lng}) {addr}')
                found = True
                break
            elif '新農' in name and '新農' in f['name']:
                f['lat'] = lat
                f['lng'] = lng
                f['address'] = addr
                print(f'✅ Updated: {f["name"]} -> ({lat}, {lng}) {addr}')
                found = True
                break
            elif '埔心' in name and '埔心' in f['name']:
                f['lat'] = lat
                f['lng'] = lng
                f['address'] = addr
                print(f'✅ Updated: {f["name"]} -> ({lat}, {lng}) {addr}')
                found = True
                break
            elif '萬大' in name and '萬大' in f['name']:
                f['lat'] = lat
                f['lng'] = lng
                f['address'] = addr
                print(f'✅ Updated: {f["name"]} -> ({lat}, {lng}) {addr}')
                found = True
                break
    
    if not found:
        # Add new
        if name not in existing_names:
            foods.append({
                "name": name,
                "place_id": "",
                "lat": lat,
                "lng": lng,
                "rating": 0,
                "reviews": 0,
                "address": addr,
                "area": "楊梅區",
                "categories": ["飲品"],
                "description": ""
            })
            existing_names.add(name)
            print(f'➕ Added: {name} -> ({lat}, {lng}) {addr}')

data['food'] = foods
with open('data/taoyuan.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('\nSaved')
