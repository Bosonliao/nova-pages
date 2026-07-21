"""
Update hsinchu.json and drinks.csv with Johnny's 25 Hukou drink shops
"""
import json, csv, sys, io, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

now = datetime.datetime.now().strftime('%Y-%m-%d')

HUKOU_DATA = [
    ("拾汣茶屋 湖口站前店", "新竹縣湖口鄉中正路一段7號", 24.90342, 121.04365),
    ("得正 #新竹湖口計劃", "新竹縣湖口鄉中正路一段8號", 24.90348, 121.04372),
    ("50嵐 湖口中正店", "新竹縣湖口鄉中正路一段20號", 24.90365, 121.04412),
    ("五桐號WooTEA 湖口中正店", "新竹縣湖口鄉中正路一段14號", 24.90355, 121.04388),
    ("龜記茗品 湖口中正店", "新竹縣湖口鄉中正路一段9號", 24.90341, 121.04378),
    ("麻古茶坊 新竹湖口車站店", "新竹縣湖口鄉中正路一段24號", 24.90372, 121.04425),
    ("CoCo都可 湖口中正店", "新竹縣湖口鄉中正路一段2號", 24.90335, 121.04342),
    ("茶聚CHAGE 湖口中正店", "新竹縣湖口鄉中正路一段61號", 24.90422, 121.04512),
    ("烏弄原生茶飲 湖口店", "新竹縣湖口鄉中正路一段137號", 24.90512, 121.04688),
    ("杜芳子古味茶鋪 新竹湖口店", "新竹縣湖口鄉中正路一段199號", 24.90588, 121.04812),
    ("無飲 湖口店", "新竹縣湖口鄉民族街96號", 24.90285, 121.04452),
    ("茂昌草本茶 湖口站前店", "新竹縣湖口鄉中山路二段162號", 24.90255, 121.04321),
    ("御私藏 Cozy Tea 湖口站前店", "新竹縣湖口鄉中山路二段178號", 24.90232, 121.04305),
    ("八稻茶 湖口達生店", "新竹縣湖口鄉達生路659號", 24.90212, 121.04855),
    ("TEATOP第一味 湖口達生店", "新竹縣湖口鄉中正七街177號1樓", 24.90455, 121.04912),
    ("嗜時候 Can't Help 新竹湖口店", "新竹縣湖口鄉中山路一段585號", 24.89855, 121.04012),
    ("nanafru 娜娜福 湖口仁和店", "新竹縣湖口鄉仁和路98號", 24.90532, 121.00255),
    ("沫飲MOREiN 湖口仁和店", "新竹縣湖口鄉仁和路167號", 24.90488, 121.00312),
    ("50嵐 湖口新工店", "新竹縣湖口鄉仁和路129號", 24.90515, 121.00288),
    ("茶の魔手 新竹湖口店", "新竹縣湖口鄉仁和路13號", 24.90612, 121.00188),
    ("清原芋圓 湖口仁和店", "新竹縣湖口鄉仁和路52號", 24.90585, 121.00212),
    ("LAG 累擱 鮮奶茶 湖口店", "新竹縣湖口鄉仁樂路23號", 24.90452, 121.00155),
    ("50嵐 湖口工業店", "新竹縣湖口鄉工業一路8號", 24.91255, 121.01512),
    ("功夫茶 KUNGFUTEA 湖口工業店", "新竹縣湖口鄉工業二路31號", 24.91312, 121.01688),
    ("馬祖奶茶 湖口文化店", "新竹縣湖口鄉文化路50-1號1樓", 24.90855, 121.00812),
]

# === 1. Update hsinchu.json ===
data = json.load(open('data/hsinchu.json','r',encoding='utf-8'))
foods = data.get('food', [])

json_updated = 0
json_added = 0

for name, addr, lat, lng in HUKOU_DATA:
    found = False
    jn = name.replace(' ', '').replace('#', '')
    for f in foods:
        fn = (f.get('name') or '').replace(' ', '').replace('#', '')
        if fn == jn or jn in fn or fn in jn:
            f['lat'] = lat
            f['lng'] = lng
            f['address'] = addr
            f['name'] = name
            json_updated += 1
            found = True
            break
        # Brand + branch match
        brand_j = name.split(' ')[0].split('-')[0].split('（')[0].strip()
        brand_f = (f.get('name') or '').split(' ')[0].split('-')[0].split('（')[0].strip()
        if brand_f == brand_j:
            for kw in ['湖口', '仁和', '工業', '文化', '達生']:
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
            "area": "湖口鄉",
            "categories": ["飲品"],
            "description": ""
        })
        json_added += 1

data['food'] = foods
with open('data/hsinchu.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'=== hsinchu.json ===')
print(f'Updated: {json_updated}, Added: {json_added}')

# === 2. Update drinks.csv ===
with open('data/drinks.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    csv_rows = list(reader)

csv_updated = 0
csv_added = 0

for name, addr, lat, lng in HUKOU_DATA:
    parts = name.split(' ', 1)
    brand = parts[0]
    store_name = parts[1] if len(parts) > 1 else ''
    
    found = False
    for row in csv_rows:
        if row.get('county') == '新竹' and '湖口' in (row.get('district') or ''):
            csv_full = f"{row.get('brand','')} {row.get('store_name','')}".strip().replace(' ', '').replace('#', '')
            jn = name.replace(' ', '').replace('#', '')
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
        new_id = 'HS' + str(len(csv_rows) + 1).zfill(3)
        new_row = {fn: '' for fn in fieldnames}
        new_row[fieldnames[0]] = new_id
        new_row['brand'] = brand
        new_row['store_name'] = store_name
        new_row['county'] = '新竹'
        new_row['district'] = '湖口鄉'
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
