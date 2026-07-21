"""
Update taoyuan.json and drinks.csv with Johnny's 20 Pingzhen drink shops
"""
import json, csv, sys, io, datetime, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir + '/..')

now = datetime.datetime.now().strftime('%Y-%m-%d')

PINGZHEN_DATA = [
    ("得正 #桃園平鎮計劃", "桃園市平鎮區中豐路南勢二段131號", 24.92138, 121.21528),
    ("拾汣茶屋 平鎮南勢店", "桃園市平鎮區中豐路南勢二段280號", 24.91925, 121.21482),
    ("先喝道 平鎮聯新國際店", "桃園市平鎮區復旦路二段23巷1號", 24.94528, 121.20612),
    ("林三茶研所 桃園平鎮店", "桃園市平鎮區中豐路南勢二段140號1樓", 24.92112, 121.21555),
    ("50嵐 平鎮中豐店", "桃園市平鎮區中豐路南勢二段95號", 24.92255, 121.21612),
    ("50嵐 平鎮南豐店", "桃園市平鎮區南豐路18號", 24.91588, 121.20812),
    ("50嵐 平鎮和平店", "桃園市平鎮區和平路177號", 24.95112, 121.22885),
    ("麻古茶坊 平鎮南豐店", "桃園市平鎮區南豐路45號", 24.91512, 121.20788),
    ("龜記茗品 平鎮南勢店", "桃園市平鎮區中豐路南勢二段128號", 24.92152, 121.21512),
    ("可不可熟成茶行 平鎮中豐店", "桃園市平鎮區中豐路南勢二段154號", 24.92088, 121.21588),
    ("五桐號WooTEA 桃園平鎮南勢店", "桃園市平鎮區中豐路南勢二段133號", 24.92125, 121.21532),
    ("吾奶王 桃園平鎮延平店", "桃園市平鎮區延平路一段32號1樓", 24.95312, 121.21688),
    ("上宇林 平鎮文化店", "桃園市平鎮區文化街184號1樓", 24.94122, 121.19655),
    ("無飲 育達店", "桃園市平鎮區育達路65號", 24.94855, 121.20912),
    ("茶今鑄茶所 CHA·JIN", "桃園市平鎮區中豐路南勢二段341號", 24.91788, 121.21412),
    ("炎午茶飲 平鎮金陵店", "桃園市平鎮區金陵路264號", 24.93812, 121.23212),
    ("美茶吧 滇緬泰手搖飲", "桃園市平鎮區中山路55號", 24.92552, 121.25112),
    ("COMEBUY 平鎮南豐店", "桃園市平鎮區南豐路17號1樓", 24.91612, 121.20845),
    ("出櫃 平鎮龍崗店", "桃園市平鎮區中山路205號", 24.92885, 121.25412),
    ("新井茶 平鎮和平店", "桃園市平鎮區和平路171號", 24.95088, 121.22912),
]

# === 1. Update taoyuan.json ===
data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

json_updated = 0
json_added = 0

for name, addr, lat, lng in PINGZHEN_DATA:
    found = False
    jn = name.replace(' ', '').replace('#', '').replace('.', '').replace('·', '')
    for f in foods:
        fn = (f.get('name') or '').replace(' ', '').replace('#', '').replace('.', '').replace('·', '')
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
            for kw in ['平鎮', '南勢', '南豐', '和平', '延平', '文化', '育達', '金陵', '龍崗', '中豐']:
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
            "area": "平鎮區",
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

for name, addr, lat, lng in PINGZHEN_DATA:
    parts = name.split(' ', 1)
    brand = parts[0]
    store_name = parts[1] if len(parts) > 1 else ''
    
    found = False
    for row in csv_rows:
        if row.get('county') == '桃園' and '平鎮' in (row.get('district') or ''):
            csv_full = f"{row.get('brand','')} {row.get('store_name','')}".strip().replace(' ', '').replace('#', '').replace('.', '').replace('·', '')
            jn = name.replace(' ', '').replace('#', '').replace('.', '').replace('·', '')
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
        new_row['district'] = '平鎮區'
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
