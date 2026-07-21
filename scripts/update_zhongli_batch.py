"""
Update taoyuan.json and drinks.csv with Johnny's 22 Zhongli drink shops
"""
import json, csv, sys, io, datetime, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir + '/..')

now = datetime.datetime.now().strftime('%Y-%m-%d')

ZHONGLI_DATA = [
    ("50嵐 中壢站前店", "桃園市中壢區石頭里和平街25號", 24.95355, 121.22512),
    ("50嵐 中壢新生店", "桃園市中壢區興南里新生路162號", 24.96212, 121.22388),
    ("50嵐 中壢中原店", "桃園市中壢區日新路8號", 24.95422, 121.24055),
    ("50嵐 內壢忠孝店", "桃園市中壢區忠孝路35號", 24.97512, 121.25688),
    ("得正 #中壢新生計劃", "桃園市中壢區新生路138號", 24.96155, 121.22412),
    ("一沐日 中壢三民店", "桃園市中壢區三民路周邊", 24.96312, 121.21855),
    ("迷客夏Milksha 桃園中壢站前店", "桃園市中壢區石頭里中正路89號之2號", 24.95388, 121.22488),
    ("迷客夏Milksha 中壢元化店", "桃園市中壢區興南里元化路350號", 24.96422, 121.22555),
    ("迷客夏Milksha 桃園內壢忠孝店", "桃園市中壢區中原里忠孝路58號", 24.97588, 121.25712),
    ("可不可熟成茶行 中壢站前店", "桃園市中壢區石頭里中正路29號", 24.95322, 121.22455),
    ("可不可熟成茶行 中壢中山店", "桃園市中壢區新明里中山路536號", 24.95855, 121.21912),
    ("可不可熟成茶行 中壢中原店", "桃園市中壢區普忠里中北路155號", 24.95512, 121.24112),
    ("麻古茶坊 中壢新生店", "桃園市中壢區興國里新生路105號", 24.96088, 121.22445),
    ("弎茶TEEE TEA", "桃園市中壢區金華里新生路359號", 24.96552, 121.22312),
    ("河河 HOHO DRINKS 桃園中壢", "桃園市中壢區興平里新生路273號1樓", 24.96455, 121.22355),
    ("思茶MissingTea 內壢忠孝店", "桃園市中壢區忠孝里忠孝路201-2號", 24.97812, 121.25912),
    ("大茗本位製茶堂 中壢新明店", "桃園市中壢區新明里新明路40號", 24.95922, 121.21788),
    ("Lag累擱鮮奶茶 創始總店", "桃園市中壢區新明里中央西路二段26號", 24.95885, 121.21812),
    ("甘蔗媽媽 桃園中壢店", "桃園市中壢區舊明里中正路361號", 24.95655, 121.21988),
    ("北茶屋 中壢店", "桃園市中壢區幸福里福州二街412號", 24.96112, 121.23512),
    ("星M STAR M 中壢海華店", "桃園市中壢區新街里慈惠三街108巷8號", 24.96352, 121.22688),
    ("吾奶王 桃園內壢店", "桃園市中壢區中華路一段306號", 24.97122, 121.25312),
]

# === 1. Update taoyuan.json ===
data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

json_updated = 0
json_added = 0

for name, addr, lat, lng in ZHONGLI_DATA:
    found = False
    jn = name.replace(' ', '').replace('#', '').replace('.', '')
    for f in foods:
        fn = (f.get('name') or '').replace(' ', '').replace('#', '').replace('.', '')
        if fn == jn or jn in fn or fn in jn:
            f['lat'] = lat
            f['lng'] = lng
            f['address'] = addr
            f['name'] = name
            json_updated += 1
            found = True
            break
        # Brand + branch match
        brand_j = name.split(' ')[0].split('-')[0].split('（')[0].split('#')[0].strip()
        brand_f = (f.get('name') or '').split(' ')[0].split('-')[0].split('（')[0].split('#')[0].strip()
        if brand_f and brand_j and (brand_f == brand_j or brand_f in brand_j or brand_j in brand_f):
            for kw in ['中壢', '內壢', '站前', '新生', '中原', '忠孝', '中山', '元化', '海華', '新明', '三民']:
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
            "area": "中壢區",
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

for name, addr, lat, lng in ZHONGLI_DATA:
    parts = name.split(' ', 1)
    brand = parts[0]
    store_name = parts[1] if len(parts) > 1 else ''
    
    found = False
    for row in csv_rows:
        if row.get('county') == '桃園' and '中壢' in (row.get('district') or ''):
            csv_full = f"{row.get('brand','')} {row.get('store_name','')}".strip().replace(' ', '').replace('#', '').replace('.', '')
            jn = name.replace(' ', '').replace('#', '').replace('.', '')
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
        new_row['district'] = '中壢區'
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
