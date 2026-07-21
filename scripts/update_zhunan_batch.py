"""
Update miaoli.json and drinks.csv with Johnny's 20 Zhunan drink shops
"""
import json, csv, sys, io, datetime, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir + '/..')

now = datetime.datetime.now().strftime('%Y-%m-%d')

ZHUNAN_DATA = [
    ("UG 苗栗竹南店", "苗栗縣竹南鎮博愛街126號", 24.68662, 120.88055),
    ("一沐日 竹南博愛店", "苗栗縣竹南鎮博愛街158號", 24.68725, 120.88122),
    ("得正 #竹南博愛計劃", "苗栗縣竹南鎮博愛街138號", 24.68688, 120.88088),
    ("50嵐 竹南博愛店", "苗栗縣竹南鎮博愛街136號", 24.68652, 120.88065),
    ("50嵐 竹南延平店", "苗栗縣竹南鎮延平路106號", 24.68212, 120.88255),
    ("麻古茶坊 竹南博愛店", "苗栗縣竹南鎮博愛街145號", 24.68711, 120.88095),
    ("龜記茗品 竹南博愛店", "苗栗縣竹南鎮博愛街152號", 24.68695, 120.88105),
    ("迷客夏Milksha 竹南博愛店", "苗栗縣竹南鎮博愛街156號", 24.68712, 120.88118),
    ("大茗本位製茶堂 苗栗竹南店", "苗栗縣竹南鎮博愛街122號", 24.68633, 120.88022),
    ("烏弄原生茶飲 竹南博愛店", "苗栗縣竹南鎮博愛街159號", 24.68735, 120.88135),
    ("鶴茶樓 竹南博愛店", "苗栗縣竹南鎮博愛街132號", 24.68675, 120.88075),
    ("十二韻 竹南博愛店", "苗栗縣竹南鎮博愛街96號", 24.68585, 120.87955),
    ("思茶MissingTea 竹南博愛店", "苗栗縣竹南鎮博愛街179號", 24.68755, 120.88165),
    ("八曜和茶 苗栗竹南店", "苗栗縣竹南鎮民權街43號", 24.68352, 120.88155),
    ("春陽茶事 竹南博愛店", "苗栗縣竹南鎮博愛街189號", 24.68788, 120.88212),
    ("TEA TOP 第一味 竹南店", "苗栗縣竹南鎮延平路97號", 24.68222, 120.88215),
    ("上宇林 竹南環市店", "苗栗縣竹南鎮環市路一段275號", 24.68112, 120.87512),
    ("一芳水果茶 竹南店", "苗栗縣竹南鎮中山路108號", 24.67885, 120.88315),
    ("先喝道 竹南博愛店", "苗栗縣竹南鎮博愛街172號", 24.68742, 120.88145),
    ("CoCo都可 竹南光復店", "苗栗縣竹南鎮光復路198號", 24.68012, 120.88655),
]

# === 1. Update miaoli.json ===
data = json.load(open('data/miaoli.json','r',encoding='utf-8'))
foods = data.get('food', [])

json_updated = 0
json_added = 0

for name, addr, lat, lng in ZHUNAN_DATA:
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
            for kw in ['竹南', '博愛', '延平', '環市', '光復', '民權']:
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
            "area": "竹南鎮",
            "categories": ["飲品"],
            "description": ""
        })
        json_added += 1

data['food'] = foods
with open('data/miaoli.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'=== miaoli.json ===')
print(f'Updated: {json_updated}, Added: {json_added}')

# === 2. Update drinks.csv ===
with open('data/drinks.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    csv_rows = list(reader)

csv_updated = 0
csv_added = 0

for name, addr, lat, lng in ZHUNAN_DATA:
    parts = name.split(' ', 1)
    brand = parts[0]
    store_name = parts[1] if len(parts) > 1 else ''
    
    found = False
    for row in csv_rows:
        if row.get('county') == '苗栗' and '竹南' in (row.get('district') or ''):
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
        new_id = 'ML' + str(len(csv_rows) + 1).zfill(3)
        new_row = {fn: '' for fn in fieldnames}
        new_row[fieldnames[0]] = new_id
        new_row['brand'] = brand
        new_row['store_name'] = store_name
        new_row['county'] = '苗栗'
        new_row['district'] = '竹南鎮'
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
