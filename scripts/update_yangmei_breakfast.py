"""
Update taoyuan.json and restaurants.csv with Johnny's 14 Yangmei breakfast shops
"""
import json, csv, sys, io, datetime, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir + '/..')

now = datetime.datetime.now().strftime('%Y-%m-%d')

BREAKFAST_DATA = [
    ("楊梅大成路蛋餅飯糰", "桃園市楊梅區大成路181號", 24.91212, 121.14388),
    ("我想想咖啡早午餐", "桃園市楊梅區光復街33號", 24.91425, 121.14488),
    ("吐司基早午餐", "桃園市楊梅區四維路125號", 24.91485, 121.17952),
    ("旅人咖啡館 楊梅店", "桃園市楊梅區新農街7號", 24.91185, 121.14652),
    ("楊梅無名早餐店 大平街", "桃園市楊梅區大平街53號", 24.91355, 121.14312),
    ("埔心無名早餐店", "桃園市楊梅區中興路119號", 24.91421, 121.18567),
    ("一品早餐", "桃園市楊梅區楊新路111號", 24.91522, 121.14788),
    ("四海豆漿 中山北路", "桃園市楊梅區中山北路二段100號", 24.91388, 121.15412),
    ("阿發手工湯包", "桃園市楊梅區大成路160號", 24.91225, 121.14418),
    ("大楊梅手工包子", "桃園市楊梅區環東路522號", 24.91585, 121.15812),
    ("六吋盤早午餐 楊梅中山店", "桃園市楊梅區中山北路一段420號", 24.91155, 121.15588),
    ("Q Burger 楊梅大成店", "桃園市楊梅區大成路190號", 24.91175, 121.14375),
    ("弘爺漢堡 楊梅金德店", "桃園市楊梅區金德路53號", 24.91612, 121.14512),
    ("麥味登 楊梅新農店", "桃園市楊梅區新農街406號", 24.91012, 121.15855),
]

# === 1. Update taoyuan.json ===
data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

json_updated = 0
json_added = 0

for name, addr, lat, lng in BREAKFAST_DATA:
    found = False
    jn = name.replace(' ', '').replace('#', '').replace('.', '').replace('-', '')
    for f in foods:
        fn = (f.get('name') or '').replace(' ', '').replace('#', '').replace('.', '').replace('-', '')
        if fn == jn or jn in fn or fn in jn:
            f['lat'] = lat
            f['lng'] = lng
            f['address'] = addr
            f['name'] = name
            if '早餐' not in f.get('categories',[]):
                f.setdefault('categories', []).append('早餐')
            json_updated += 1
            found = True
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
            "area": "楊梅區",
            "categories": ["早餐"],
            "description": ""
        })
        json_added += 1

data['food'] = foods
with open('data/taoyuan.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'=== taoyuan.json ===')
print(f'Updated: {json_updated}, Added: {json_added}')

# === 2. Update restaurants.csv ===
with open('data/restaurants.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    csv_rows = list(reader)

csv_updated = 0
csv_added = 0

for name, addr, lat, lng in BREAKFAST_DATA:
    found = False
    for row in csv_rows:
        if '楊梅' in (row.get('district') or ''):
            rn = (row.get('name') or '').replace(' ', '').replace('#', '').replace('.', '').replace('-', '')
            if rn == jn or jn in rn or rn in jn:
                row['lat'] = str(lat)
                row['lng'] = str(lng)
                row['address'] = addr
                row['source'] = 'johnny'
                row['updated_at'] = now
                cats = row.get('category','')
                if '早餐' not in cats:
                    row['category'] = cats + ',早餐' if cats else '早餐'
                csv_updated += 1
                found = True
                break
    
    if not found:
        new_id = 'TY_R_' + str(len(csv_rows) + 1).zfill(5)
        new_row = {fn: '' for fn in fieldnames}
        new_row[fieldnames[0]] = new_id
        new_row['name'] = name
        new_row['county'] = '桃園'
        new_row['district'] = '楊梅區'
        new_row['address'] = addr
        new_row['lat'] = str(lat)
        new_row['lng'] = str(lng)
        new_row['category'] = '早餐'
        new_row['source'] = 'johnny'
        new_row['updated_at'] = now
        csv_rows.append(new_row)
        csv_added += 1

with open('data/restaurants.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(csv_rows)

print(f'\n=== restaurants.csv ===')
print(f'Updated: {csv_updated}, Added: {csv_added}')
print(f'restaurants.csv total: {len(csv_rows)}')
