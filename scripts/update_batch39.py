"""
Update both taoyuan.json and drinks.csv with Johnny's batch of 39 precise coords
"""
import json, csv, sys, io, datetime, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Johnny's data
JOHNNY_DATA = [
    ("UG 楊梅大成店", "桃園市楊梅區大成路137號", 24.91266, 121.14441),
    ("Go ba 自然湉 楊梅大成店", "桃園市楊梅區大成路205號", 24.91187, 121.14385),
    ("得正 楊梅大成計劃", "桃園市楊梅區大成路177號", 24.91201, 121.14408),
    ("茶聚CHAGE 楊梅大成店", "桃園市楊梅區大成路164號", 24.91218, 121.14412),
    ("五桐號WooTEA 楊梅大成店", "桃園市楊梅區大成路142號", 24.91255, 121.14436),
    ("萬波島嶼紅茶 楊梅大成店", "桃園市楊梅區大成路136號", 24.91271, 121.14445),
    ("迷客夏Milksha 桃園楊梅店", "桃園市楊梅區大成路122號", 24.91301, 121.14472),
    ("COMEBUY 楊梅大成店", "桃園市楊梅區大成路118號", 24.91312, 121.14488),
    ("可不可熟成茶行 楊梅大成店", "桃園市楊梅區大成路96號", 24.91345, 121.14521),
    ("清心福全 楊梅大成店", "桃園市楊梅區大成路186號", 24.91192, 121.14392),
    ("TEA TOP第一味 楊梅大成店", "桃園市楊梅區大成路188號", 24.91185, 121.14388),
    ("林三茶研所 楊梅大成店", "桃園市楊梅區大成路232號", 24.91132, 121.14311),
    ("上宇林 楊梅大成店", "桃園市楊梅區大成路138號", 24.91265, 121.14438),
    ("龜記茗品 楊梅大成店", "桃園市楊梅區大成路145號", 24.91248, 121.14422),
    ("CoCo都可 楊梅大成店", "桃園市楊梅區大成路10之1號", 24.91485, 121.14691),
    ("50嵐 楊梅大成店", "桃園市楊梅區大成路204號", 24.91254, 121.14591),
    ("茗茗究市 桃園旗艦店", "桃園市楊梅區大成路37號", 24.91386, 121.14583),
    ("思茶MissingTea 桃園楊梅店", "桃園市楊梅區大華街32號", 24.91315, 121.14612),
    ("茂昌草本茶 楊梅楊新店", "桃園市楊梅區楊新路78號", 24.91458, 121.14652),
    ("鮮茶道 楊梅楊新北店", "桃園市楊梅區楊新北路391號", 24.91811, 121.14925),
    ("蓋胖杯茶飲", "桃園市楊梅區新成路12號", 24.91402, 121.14498),
    ("先喝道 桃園楊梅店", "桃園市楊梅區環東路441號", 24.91433, 121.15412),
    ("花火禾茶 はなび 製茶所", "桃園市楊梅區新農街357號", 24.91032, 121.15786),
    ("Tea's原味 楊梅新農店", "桃園市楊梅區新農街二段52號", 24.90855, 121.16112),
    ("迷客夏Milksha 桃園楊梅埔心店", "桃園市楊梅區中興路109號", 24.91411, 121.18512),
    ("50嵐 埔心中興店", "桃園市楊梅區中興路103號", 24.91421, 121.18567),
    ("茶詠春 楊梅埔心店", "桃園市楊梅區中興路12號", 24.91522, 121.18688),
    ("鮮茶道 埔心站前店", "桃園市楊梅區中興路6號", 24.91544, 121.18712),
    ("紅茶大苑 埔心店", "桃園市楊梅區中興路15號1樓", 24.91515, 121.18665),
    ("麻古茶坊 楊梅文化店", "桃園市楊梅區文化街167號", 24.91488, 121.18122),
    ("五桐號WooTEA 楊梅文化店", "桃園市楊梅區文化街187號", 24.91425, 121.18095),
    ("COMEBUY 楊梅文化店", "桃園市楊梅區文化街181號", 24.91442, 121.18105),
    ("紅茶巴士 楊梅文化站", "桃園市楊梅區文化街203號", 24.91388, 121.18045),
    ("龜記 埔心文化店", "桃園市楊梅區文化街228號", 24.91312, 121.17988),
    ("可不可熟成茶行 埔心文化店", "桃園市楊梅區文化街252號", 24.91233, 121.17912),
    ("功夫茶 KUNGFUTEA 楊梅四維店", "桃園市楊梅區四維路90號", 24.91523, 121.18042),
    ("金茶伍手作飲品 楊梅瑞溪門市", "桃園市楊梅區瑞溪路二段215號1樓", 24.91316, 121.17387),
    ("吾奶王 桃園楊梅店", "桃園市楊梅區梅獅路二段95號", 24.91892, 121.18231),
    ("食茶 特色茶飲", "桃園市楊梅區成功路38號", 24.93512, 121.09015),
]

now = datetime.datetime.now().strftime('%Y-%m-%d')

# === 1. Update taoyuan.json ===
data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

# Build matching: try to match Johnny's name to existing entries
def match_shop(json_food, johnny_name, addr):
    """Try to match Johnny's shop name to existing JSON entry"""
    jn = johnny_name.replace(' ', '').replace('#', '')
    
    for f in foods:
        if f.get('area') != '楊梅區':
            continue
        if not any('飲品' in c for c in (f.get('categories') or [])):
            continue
        
        fn = (f.get('name') or '').replace(' ', '').replace('#', '')
        
        # Exact match
        if fn == jn:
            return f
        
        # Partial match (one contains the other)
        if jn in fn or fn in jn:
            return f
        
        # Brand + branch match
        # e.g. "可不可熟成茶行 楊梅大成店" vs "可不可熟成茶行 楊梅文化店"
        # Check if brand matches and branch keyword matches
        brand_j = jn.split('店')[0].split('號')[0] if '店' in jn else jn[:6]
        branch_keywords = ['大成', '文化', '埔心', '新農', '四維', '瑞溪', '梅獅', '永美', '環南', '環東', '青山', '中山', '富岡', '楊新']
        for kw in branch_keywords:
            if kw in johnny_name and kw in (f.get('name') or ''):
                # Also check brand
                brand_f = (f.get('name') or '').split(' ')[0].split('-')[0].split('（')[0].split('(')[0].strip()
                brand_j2 = johnny_name.split(' ')[0].split('-')[0].split('（')[0].split('(')[0].strip()
                if brand_f == brand_j2 or brand_f in brand_j2 or brand_j2 in brand_f:
                    return f
    
    return None

json_updated = 0
json_added = 0

for name, addr, lat, lng in JOHNNY_DATA:
    f = match_shop(foods, name, addr)
    
    if f:
        f['lat'] = lat
        f['lng'] = lng
        f['address'] = addr
        # Update name to Johnny's version (cleaner)
        f['name'] = name
        json_updated += 1
    else:
        # Add new
        new_f = {
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
        }
        foods.append(new_f)
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

for name, addr, lat, lng in JOHNNY_DATA:
    # Parse brand and store_name
    parts = name.split(' ', 1)
    brand = parts[0]
    store_name = parts[1] if len(parts) > 1 else ''
    
    # Try to find matching row
    found = False
    for row in csv_rows:
        if row.get('county') == '桃園' and row.get('district') == '楊梅區':
            csv_full = f"{row.get('brand','')} {row.get('store_name','')}".strip().replace(' ', '').replace('#', '')
            jn = name.replace(' ', '').replace('#', '')
            
            if csv_full == jn:
                row['lat'] = str(lat)
                row['lng'] = str(lng)
                row['address'] = addr
                row['source'] = 'johnny'
                row['updated_at'] = now
                csv_updated += 1
                found = True
                break
            
            # Brand + branch keyword match
            if row.get('brand') == brand:
                branch_keywords = ['大成', '文化', '埔心', '新農', '四維', '瑞溪', '梅獅', '楊新']
                for kw in branch_keywords:
                    if kw in name and kw in row.get('store_name', ''):
                        row['lat'] = str(lat)
                        row['lng'] = str(lng)
                        row['address'] = addr
                        row['store_name'] = store_name
                        row['source'] = 'johnny'
                        row['updated_at'] = now
                        csv_updated += 1
                        found = True
                        break
                if found:
                    break
    
    if not found:
        # Add new
        new_id = 'TY' + str(len(csv_rows) + 1).zfill(3)
        new_row = {fn: '' for fn in fieldnames}
        new_row[fieldnames[0]] = new_id
        new_row['brand'] = brand
        new_row['store_name'] = store_name
        new_row['county'] = '桃園'
        new_row['district'] = '楊梅區'
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

# Verify
has = sum(1 for r in csv_rows if r.get('lat') and r.get('lng'))
print(f'drinks.csv total: {len(csv_rows)}, with coords: {has}')

# Show new stores that were added
print(f'\n=== 新增的店 ===')
existing_brands = ['50嵐', '清心福全', 'CoCo', 'COMEBUY', '可不可', '茶湯會', '大苑子', '迷客夏', '麻古', '萬波', '五桐號', '龜記', '上宇林', '功夫茶', '花火禾茶', '茗茗究市', '金茶伍', '吾奶王', '先喝道', '蓋胖杯', '得正', '萃Da', '思茶', '紅茶巴士', '茶詠春', '鮮茶道', '茂昌', 'UG', '自然湉', '食茶', "Tea's", '皇后先生', '永珍', '菓點子', '紅茶帝國', '享飲', '回憶小時候', '鮮饗茶', 'TrueWin', '紅茶媽媽']
for name, addr, lat, lng in JOHNNY_DATA:
    brand = name.split(' ')[0]
    is_new = True
    for eb in existing_brands:
        if eb in name:
            is_new = False
            break
    if is_new:
        print(f'  🆕 {name} | {addr} | ({lat}, {lng})')
