"""
Update hsinchu.json and drinks.csv with Johnny's 19 Hukou supplement shops
(corrected addresses with village names + new shops)
"""
import json, csv, sys, io, datetime, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir + '/..')

now = datetime.datetime.now().strftime('%Y-%m-%d')

HUKOU_SUP_DATA = [
    ("50嵐 湖口工業店", "新竹縣湖口鄉勝利村工業一路8號", 24.91255, 121.01512),
    ("50嵐 湖口新工店", "新竹縣湖口鄉鳳凰村仁和路129號", 24.90515, 121.00288),
    ("清心福全 湖口工業店", "新竹縣湖口鄉中興村工業一路25號", 24.91235, 121.01588),
    ("CoCo都可 湖口光復店", "新竹縣湖口鄉勝利村工業一路16號", 24.91288, 121.01545),
    ("功夫茶 湖口工業店", "新竹縣湖口鄉勝利村工業二路31號", 24.91312, 121.01688),
    ("功夫茶 湖口中華店", "新竹縣湖口鄉鳳凰村中華路92號", 24.90385, 121.00512),
    ("可不可熟成茶行 湖口中華店", "新竹縣湖口鄉鳳凰村仁樂路160號", 24.90522, 121.00688),
    ("LAG 累擱鮮奶茶 湖口店", "新竹縣湖口鄉鳳凰村仁樂路23號", 24.90452, 121.00155),
    ("馬祖奶茶 湖口文化店", "新竹縣湖口鄉鳳凰村文化路50-1號1樓", 24.90855, 121.00812),
    ("nanafru 娜娜福 湖口仁和店", "新竹縣湖口鄉鳳凰村仁和路98號", 24.90532, 121.00255),
    ("麻古茶坊 湖口仁和店", "新竹縣湖口鄉鳳凰村仁和路84號", 24.90555, 121.00212),
    ("茶の魔手 新竹湖口店", "新竹縣湖口鄉鳳凰村仁和路13號", 24.90612, 121.00188),
    ("沫飲 MOREiN 湖口仁和店", "新竹縣湖口鄉鳳凰村仁和路167號", 24.90488, 121.00312),
    ("茶饗亭 湖口仁和店", "新竹縣湖口鄉鳳凰村仁和路50號", 24.90595, 121.00235),
    ("挑好茶 新竹湖口店", "新竹縣湖口鄉鳳凰村仁和路63號", 24.90575, 121.00288),
    ("愛茗坊", "新竹縣湖口鄉中興村光復東路130號", 24.91522, 121.02112),
    ("吳家紅茶冰 湖口工業店", "新竹縣湖口鄉中興村工業一路13號", 24.91265, 121.01532),
    ("上宇林 湖口民權店", "新竹縣湖口鄉中興村民權街33號", 24.90388, 121.04255),
    ("三年愛班豆花冰舖 湖口店", "新竹縣湖口鄉鳳凰村文化路47號", 24.90822, 121.00788),
]

# === 1. Update hsinchu.json ===
data = json.load(open('data/hsinchu.json','r',encoding='utf-8'))
foods = data.get('food', [])

json_updated = 0
json_added = 0

for name, addr, lat, lng in HUKOU_SUP_DATA:
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
            for kw in ['湖口', '工業', '仁和', '文化', '中華', '光復', '民權']:
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

for name, addr, lat, lng in HUKOU_SUP_DATA:
    parts = name.split(' ', 1)
    brand = parts[0]
    store_name = parts[1] if len(parts) > 1 else ''
    
    found = False
    for row in csv_rows:
        if row.get('county') == '新竹' and '湖口' in (row.get('district') or ''):
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
