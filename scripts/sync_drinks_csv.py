"""
Sync Johnny's precise coords back to drinks.csv (master file)
"""
import csv, sys, io, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Johnny's precise coords (all he provided today)
JOHNNY_COORDS = {
    "50嵐 楊梅大成店": (24.91225, 121.14418, "桃園市楊梅區大成路160號"),
    "50嵐 楊梅新農店": (24.90998, 121.15545, "桃園市楊梅區新農街265號"),
    "50嵐 埔心中興店": (24.91421, 121.18567, "桃園市楊梅區中興路119號"),
    "50嵐 楊梅萬大店": (24.91745, 121.17932, "桃園市楊梅區萬大路136號"),
    "UG 楊梅大成店": (24.91266, 121.14441, "桃園市楊梅區大成路137號"),
    "Go ba 自然湉 楊梅大成店": (24.91187, 121.14385, "桃園市楊梅區大成路205號"),
    "茗茗究市 桃園旗艦店": (24.91386, 121.14583, "桃園市楊梅區大成路37號"),
    "茂昌草本茶 楊梅楊新店": (24.91458, 121.14652, "桃園市楊梅區楊新路78號"),
    "花火禾茶 はなび 製茶所": (24.91032, 121.15786, "桃園市楊梅區新農街357號"),
    "功夫茶 楊梅四維店": (24.91523, 121.18042, "桃園市楊梅區四維路90號"),
    "金茶伍手作飲品 楊梅瑞溪門市": (24.91316, 121.17387, "桃園市楊梅區瑞溪路二段215號1樓"),
    "吾奶王 桃園楊梅店": (24.91892, 121.18231, "桃園市楊梅區梅獅路二段95號"),
}

# Read drinks.csv
with open('data/drinks.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

now = datetime.datetime.now().strftime('%Y-%m-%d')
updated = 0
added = 0

# Build brand+store_name lookup
def match_key(brand, store_name, district):
    return f"{brand} {store_name}".strip()

# Try to match and update
for name_key, (lat, lng, addr) in JOHNNY_COORDS.items():
    # Parse: "50嵐 楊梅大成店" -> brand="50嵐", store_name="楊梅大成店"
    parts = name_key.split(' ', 1)
    brand = parts[0]
    store_name = parts[1] if len(parts) > 1 else ''
    
    found = False
    for row in rows:
        if row.get('county') == '桃園' and row.get('district') == '楊梅區':
            if row.get('brand') == brand and (store_name in row.get('store_name','') or row.get('store_name','') in store_name):
                row['lat'] = str(lat)
                row['lng'] = str(lng)
                if addr:
                    row['address'] = addr
                row['source'] = 'johnny'
                row['updated_at'] = now
                print(f'✅ Updated CSV: {brand} {row["store_name"]} -> ({lat}, {lng})')
                updated += 1
                found = True
                break
    
    if not found:
        # Add new row
        import uuid
        new_id = 'TY' + str(len(rows) + 1).zfill(3)
        new_row = {
            fieldnames[0]: new_id,  # id (with BOM)
            'brand': brand,
            'store_name': store_name,
            'county': '桃園',
            'district': '楊梅區',
            'address': addr,
            'lat': str(lat),
            'lng': str(lng),
            'source': 'johnny',
            'updated_at': now
        }
        rows.append(new_row)
        print(f'➕ Added CSV: {name_key} -> ({lat}, {lng})')
        added += 1

# Write back
with open('data/drinks.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f'\nCSV Updated: {updated} updated, {added} added')

# Verify
with open('data/drinks.csv', 'r', encoding='utf-8-sig') as f:
    r = csv.DictReader(f)
    all_rows = list(r)
    has = sum(1 for x in all_rows if x.get('lat') and x.get('lng'))
    print(f'drinks.csv: {has}/{len(all_rows)} have coords')
