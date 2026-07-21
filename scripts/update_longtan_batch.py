"""
Update taoyuan.json and drinks.csv with Johnny's 20 Longtan drink shops
"""
import json, csv, sys, io, datetime, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir + '/..')

now = datetime.datetime.now().strftime('%Y-%m-%d')

LONGTAN_DATA = [
    ("UG 桃園龍潭店", "桃園市龍潭區北龍路93號", 24.86536, 121.21445),
    ("一沐日 龍潭中正店", "桃園市龍潭區中正路239號", 24.86311, 121.21125),
    ("得正 #桃園龍潭計劃", "桃園市龍潭區北龍路121號", 24.86632, 121.21393),
    ("50嵐 龍潭北龍店", "桃園市龍潭區北龍路61號", 24.86421, 121.21488),
    ("麻古茶坊 龍潭北龍店", "桃園市龍潭區北龍路51號", 24.86385, 121.21512),
    ("龜記茗品 龍潭東龍店", "桃園市龍潭區東龍路230號", 24.86212, 121.21655),
    ("上宇林 龍潭東龍店", "桃園市龍潭區東龍路234號1樓", 24.86188, 121.21682),
    ("大茗本位製茶堂 桃園龍潭店", "桃園市龍潭區東龍路256號", 24.86112, 121.21755),
    ("青山-青茶專業製作 桃園龍潭店", "桃園市龍潭區東龍路221號", 24.86245, 121.21612),
    ("沫飲MOREiN 桃園龍潭店", "桃園市龍潭區龍元路110號", 24.86352, 121.21388),
    ("吾奶王 桃園龍潭店", "桃園市龍潭區龍青路30號", 24.86512, 121.21855),
    ("拾汣茶屋 龍潭北龍店", "桃園市龍潭區北龍路216號", 24.86885, 121.21212),
    ("五桐號 桃園龍潭北龍店", "桃園市龍潭區北龍路58號", 24.86312, 121.21588),
    ("福氣塘HOKI TEA 龍潭中正門市", "桃園市龍潭區中正路199號1樓", 24.86452, 121.21255),
    ("茶可斯TeaCos 龍潭東龍店", "桃園市龍潭區東龍路218號", 24.86288, 121.21552),
    ("TEATOP第一味 龍潭北龍店", "桃園市龍潭區北龍路103號", 24.86585, 121.21412),
    ("蔗家店 桃園龍潭店", "桃園市龍潭區龍青路12巷7號", 24.86411, 121.21925),
    ("COMEBUY 桃園龍潭店", "桃園市龍潭區東龍路214號1樓", 24.86322, 121.21515),
    ("CoCo都可 北潭店", "桃園市龍潭區北龍路116號", 24.86655, 121.21312),
    ("CoCo都可 百年店", "桃園市龍潭區中豐路315號", 24.85122, 121.19888),
]

# === 1. Update taoyuan.json ===
data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

json_updated = 0
json_added = 0

for name, addr, lat, lng in LONGTAN_DATA:
    found = False
    jn = name.replace(' ', '').replace('#', '').replace('.', '').replace('-', '')
    for f in foods:
        fn = (f.get('name') or '').replace(' ', '').replace('#', '').replace('.', '').replace('-', '')
        if fn == jn or jn in fn or fn in jn:
            f['lat'] = lat
            f['lng'] = lng
            f['address'] = addr
            f['name'] = name
            json_updated += 1
            found = True
            break
        brand_j = name.split(' ')[0].split('-')[0].split('（')[0].split('#')[0].strip()
        brand_f = (f.get('name') or '').split(' ')[0].split('-')[0].split('（')[0].split('#')[0].strip()
        if brand_f and brand_j and (brand_f == brand_j or brand_f in brand_j or brand_j in brand_f):
            for kw in ['龍潭', '北龍', '東龍', '中正', '龍元', '龍青', '百年', '北潭']:
                if kw in name and kw in (f.get('name') or ''):
                    f['lat'] = lat
                    f['lng'] = lng
                    f['address'] = addr
                    f['name'] = name
                    json_updated += 1
                    found = True
                    break
            if found:
                break
    
    if not found:
        foods.append({
            "name": name,
            "place_id": "",
            "lat": lat,
            "lng": lng,
            "rating": 0,
            "reviews": 0,
            "address": addr,
            "area": "龍潭區",
            "categories": ["飲品"],
            "description": ""
        })
        json_added += 1

data['food'] = foods
with open('data/taoyuan.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'=== taoyuan.json ===')
print(f'Updated: {json_updated}, Added: {json_added}')

# === 2. Update drinks.csv ===
with open('data/drinks.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    csv_rows = list(reader)

csv_updated = 0
csv_added = 0

for name, addr, lat, lng in LONGTAN_DATA:
    parts = name.split(' ', 1)
    brand = parts[0]
    store_name = parts[1] if len(parts) > 1 else ''
    
    found = False
    for row in csv_rows:
        if row.get('county') == '桃園' and '龍潭' in (row.get('district') or ''):
            csv_full = f"{row.get('brand','')} {row.get('store_name','')}".strip().replace(' ', '').replace('#', '').replace('.', '').replace('-', '')
            jn = name.replace(' ', '').replace('#', '').replace('.', '').replace('-', '')
            if csv_full == jn or jn in csv_full or csv_full in jn:
                row['lat'] = str(lat)
                row['lng'] = str(lng)
                row['address'] = addr
                row['source'] = 'johnny'
                row['updated_at'] = now
                csv_updated += 1
                found = True
                break
    
    if not found:
        new_id = 'TY' + str(len(csv_rows) + 1).zfill(3)
        new_row = {fn: '' for fn in fieldnames}
        new_row[fieldnames[0]] = new_id
        new_row['brand'] = brand
        new_row['store_name'] = store_name
        new_row['county'] = '桃園'
        new_row['district'] = '龍潭區'
        new_row['address'] = addr
        new_row['lat'] = str(lat)
        new_row['lng'] = str(lng)
        new_row['source'] = 'johnny'
        new_row['updated_at'] = now
        csv_rows.append(new_row)
        csv_added += 1

with open('data/drinks.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(csv_rows)

print(f'\n=== drinks.csv ===')
print(f'Updated: {csv_updated}, Added: {csv_added}')

has = sum(1 for r in csv_rows if r.get('lat') and r.get('lng'))
print(f'drinks.csv total: {len(csv_rows)}, with coords: {has}')
