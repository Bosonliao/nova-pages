"""
Update hsinchu.json and drinks.csv with Johnny's 22 新豐 drink shops
Also update taoyuan.json with the 39 Yangmei shops (already done but re-confirm)
"""
import json, csv, sys, io, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

now = datetime.datetime.now().strftime('%Y-%m-%d')

# Johnny's 新竹新豐 data
HSINCHU_DATA = [
    ("UG 新竹新豐店", "新竹縣新豐鄉建興路一段146之12號1樓", 24.90152, 121.00012),
    ("50嵐 新豐站前店", "新竹縣新豐鄉建興路一段25號", 24.89885, 120.99612),
    ("50嵐 新豐明新店", "新竹縣新豐鄉新興路67號", 24.90421, 120.99567),
    ("麻古茶坊 新竹新豐店", "新竹縣新豐鄉建興路一段87號", 24.90012, 120.99854),
    ("迷客夏Milksha 新竹新豐店", "新竹縣新豐鄉建興路一段159號", 24.90188, 121.00112),
    ("可不可熟成紅茶 新竹新豐店", "新竹縣新豐鄉建興路一段148號", 24.90145, 121.00045),
    ("得正 #新竹新豐計劃", "新竹縣新豐鄉建興路一段155-9號", 24.90166, 121.00088),
    ("五桐號WooTEA 新豐新興店", "新竹縣新豐鄉新興路9號", 24.89785, 120.99512),
    ("龜記茗品 新竹新豐店", "新竹縣新豐鄉建興路一段89號一樓", 24.90025, 120.99865),
    ("思茶MissingTea 新竹新豐店", "新竹縣新豐鄉建興路一段92號", 24.90035, 120.99888),
    ("青山-青茶專業製作 新竹新豐店", "新竹縣新豐鄉新興路43號", 24.90155, 120.99542),
    ("TEATOP第一味 新豐建興店", "新竹縣新豐鄉建興路一段139號", 24.90112, 120.99985),
    ("烏弄原生茶飲 新豐店", "新竹縣新豐鄉建興路一段50號", 24.89955, 120.99752),
    ("鶴茶樓 新豐建興店", "新竹縣新豐鄉建興路一段", 24.90088, 120.99925),
    ("甘蔗の媽媽 新豐建興店", "新竹縣新豐鄉建興路一段145-1號", 24.90132, 121.00022),
    ("走走茶迷 生態茶飲", "新竹縣新豐鄉建興路一段65號", 24.89988, 120.99785),
    ("藍衫茶所 新竹新豐店", "新竹縣新豐鄉民安街19號", 24.90512, 121.00122),
    ("上宇林 新豐新庄子店", "新竹縣新豐鄉新市路1號", 24.90235, 120.97885),
    ("CoCo都可 新豐建興店", "新竹縣新豐鄉建興路一段44號", 24.89921, 120.99712),
    ("金沐堂", "新竹縣新豐鄉明新一街12號", 24.90655, 120.99421),
    ("日出客棧 新竹新豐店", "新竹縣新豐鄉泰安街21號", 24.90388, 120.99812),
    ("無飲 新豐新興店", "新竹縣新豐鄉新興路149號", 24.90812, 120.99622),
]

# === 1. Update hsinchu.json ===
data = json.load(open('data/hsinchu.json','r',encoding='utf-8'))
foods = data.get('food', [])

json_updated = 0
json_added = 0

for name, addr, lat, lng in HSINCHU_DATA:
    # Try to find existing
    found = False
    for f in foods:
        fn = (f.get('name') or '').replace(' ', '').replace('#', '')
        jn = name.replace(' ', '').replace('#', '')
        if fn == jn:
            f['lat'] = lat
            f['lng'] = lng
            f['address'] = addr
            f['name'] = name
            json_updated += 1
            found = True
            break
        # Brand + branch match
        brand_f = (f.get('name') or '').split(' ')[0].split('-')[0].split('（')[0].strip()
        brand_j = name.split(' ')[0].split('-')[0].split('（')[0].strip()
        if brand_f == brand_j:
            branch_keywords = ['新豐', '建興', '新興']
            for kw in branch_keywords:
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
        # Determine area from address
        area = '新豐鄉'
        foods.append({
            "name": name,
            "place_id": "",
            "lat": lat,
            "lng": lng,
            "rating": 0,
            "reviews": 0,
            "address": addr,
            "area": area,
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

for name, addr, lat, lng in HSINCHU_DATA:
    parts = name.split(' ', 1)
    brand = parts[0]
    store_name = parts[1] if len(parts) > 1 else ''
    
    found = False
    for row in csv_rows:
        if row.get('county') == '新竹' and '新豐' in (row.get('district') or ''):
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
        new_row['district'] = '新豐鄉'
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
