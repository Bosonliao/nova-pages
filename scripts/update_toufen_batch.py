"""
Update miaoli.json and drinks.csv with Johnny's 24 Toufen drink shops
"""
import json, csv, sys, io, datetime, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir + '/..')

now = datetime.datetime.now().strftime('%Y-%m-%d')

TOUFEN_DATA = [
    ("八曜和茶 苗栗頭份中華門市", "苗栗縣頭份市中華路1023號", 24.69348, 120.91035),
    ("UG 苗栗頭份店", "苗栗縣頭份市成功里建國路156號", 24.69532, 120.90945),
    ("一沐日 頭份建國店", "苗栗縣頭份市成功里建國路185號", 24.69632, 120.90852),
    ("得正 #頭份建國計劃", "苗栗縣頭份市成功里建國路164號", 24.69568, 120.90912),
    ("50嵐 頭份建國店", "苗栗縣頭份市忠孝里建國路77號", 24.69315, 120.90888),
    ("50嵐 頭份尚順店", "苗栗縣頭份市東民五街8號", 24.69012, 120.91155),
    ("50嵐 頭份仁愛店", "苗栗縣頭份市自強里仁愛路103號", 24.68655, 120.90912),
    ("麻古茶坊 頭份尚順店", "苗栗縣頭份市東民一街2號", 24.68955, 120.91088),
    ("龜記茗品 頭份尚順店", "苗栗縣頭份市東庄里東民二街6號1樓", 24.68988, 120.91122),
    ("烏弄原生茶飲 頭份尚順店", "苗栗縣頭份市東庄里東民一街6號", 24.68925, 120.91065),
    ("思茶MissingTea 頭份尚順店", "苗栗縣頭份市東民六街3號", 24.69088, 120.91212),
    ("思茶MissingTea 頭份建國店", "苗栗縣頭份市建國路140號", 24.69488, 120.90985),
    ("匠飲ENJOY 解憂創始店", "苗栗縣頭份市東民二街11號", 24.69012, 120.91188),
    ("青山-青茶專業製作 頭份建國店", "苗栗縣頭份市成功里建國路166號", 24.69585, 120.90905),
    ("十二韻 頭份建國店", "苗栗縣頭份市建國路172號", 24.69602, 120.90888),
    ("喜力茶飲 頭份店", "苗栗縣頭份市信義里中正路110號", 24.68855, 120.90512),
    ("順道茶飲店 頭份店", "苗栗縣頭份市山下里八德二路300號", 24.68512, 120.89888),
    ("CoCo都可 頭份信義店", "苗栗縣頭份市民族里信義路89號", 24.68912, 120.90655),
    ("鶴茶樓 頭份中興店", "苗栗縣頭份市建國里中興路619號", 24.70112, 120.91255),
    ("茶聚CHAGE 頭份中央店", "苗栗縣頭份市東庄里中央路146號", 24.68555, 120.91212),
    ("上宇林 頭份信東店", "苗栗縣頭份市自強里信東路152號1樓", 24.68885, 120.91512),
    ("迷客夏Milksha 苗栗頭份建國店", "苗栗縣頭份市蟠桃里建國路二段130號", 24.70012, 120.90512),
    ("泰讚了泰式奶茶 頭份店", "苗栗縣頭份市東民一街30號", 24.68888, 120.91045),
    ("春芳號 頭份斗煥坪店", "苗栗縣頭份市中正二路214號", 24.68112, 120.94112),
]

# === 1. Update miaoli.json ===
data = json.load(open('data/miaoli.json','r',encoding='utf-8'))
foods = data.get('food', [])

json_updated = 0
json_added = 0

for name, addr, lat, lng in TOUFEN_DATA:
    found = False
    jn = name.replace(' ', '').replace('#', '').replace('.', '').replace('-', '').replace('（', '').replace('）', '')
    for f in foods:
        fn = (f.get('name') or '').replace(' ', '').replace('#', '').replace('.', '').replace('-', '').replace('（', '').replace('）', '')
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
            for kw in ['頭份', '尚順', '建國', '仁愛', '中華', '信義', '中興', '中央', '斗煥']:
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
            "area": "頭份市",
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

for name, addr, lat, lng in TOUFEN_DATA:
    parts = name.split(' ', 1)
    brand = parts[0]
    store_name = parts[1] if len(parts) > 1 else ''
    
    found = False
    for row in csv_rows:
        if row.get('county') == '苗栗' and '頭份' in (row.get('district') or ''):
            csv_full = f"{row.get('brand','')} {row.get('store_name','')}".strip().replace(' ', '').replace('#', '').replace('.', '').replace('-', '').replace('（', '').replace('）', '')
            jn = name.replace(' ', '').replace('#', '').replace('.', '').replace('-', '').replace('（', '').replace('）', '')
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
        new_row['district'] = '頭份市'
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
