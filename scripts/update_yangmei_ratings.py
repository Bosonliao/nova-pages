"""
Update ratings/reviews for Yangmei drink shops and breakfast shops
"""
import json, csv, sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')

# Data from Johnny
DRINK_RATINGS = [
    ("花火禾茶 はなび 製茶所", 4.9, 1128),
    ("茗茗究市 桃園旗艦店", 4.4, 135),
    ("思茶MissingTea 桃園楊梅店", 4.2, 353),
    ("茂昌草本茶 楊梅楊新店", 4.6, 220),
    ("吾奶王 桃園楊梅店", 4.6, 158),
    ("50嵐 埔心中興店", 4.2, 270),
    ("50嵐 楊梅大成店", 3.5, 472),
    ("茶聚CHAGE 楊梅大成店", 4.7, 75),
    ("食茶 特色茶飲", 4.8, 104),
    ("Mr.WISH 楊梅金溪店", 4.9, 110),
    ("可不可熟成茶行 楊梅大成店", 3.8, 196),
    ("CoCo都可 楊梅大成店", 4.4, 527),
]

BREAKFAST_RATINGS = [
    ("楊梅一品早餐", 4.6, 156),
    ("我想想咖啡早午餐", 4.5, 0),
    ("吐司基早午餐", 4.7, 0),
    ("楊梅大成路蛋餅飯糰", 4.3, 0),
    ("麥味登 楊梅新農店", 4.1, 0),
    ("阿發手工湯包", 4.2, 0),
]

ALL_RATINGS = DRINK_RATINGS + BREAKFAST_RATINGS

# === 1. Update taoyuan.json ===
data = json.load(open('data/taoyuan.json', 'r', encoding='utf-8'))
foods = data.get('food', [])

json_updated = 0
for name, rating, reviews in ALL_RATINGS:
    jn = name.replace(' ', '').replace('#', '').replace('.', '').replace('-', '')
    for f in foods:
        fn = (f.get('name') or '').replace(' ', '').replace('#', '').replace('.', '').replace('-', '')
        if fn == jn or jn in fn or fn in jn:
            f['rating'] = rating
            f['reviews'] = reviews
            json_updated += 1
            print(f'  ✅ {name} → ★{rating} ({reviews}則)')
            break

data['food'] = foods
with open('data/taoyuan.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\ntaoyuan.json updated: {json_updated}')

# === 2. Update drinks.csv ===
with open('data/drinks.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    csv_rows = list(reader)

csv_updated = 0
for name, rating, reviews in DRINK_RATINGS:
    jn = name.replace(' ', '').replace('#', '').replace('.', '').replace('-', '')
    for row in csv_rows:
        full = f"{row.get('brand','')} {row.get('store_name','')}".strip()
        rn = full.replace(' ', '').replace('#', '').replace('.', '').replace('-', '')
        if rn == jn or jn in rn or rn in jn:
            row['rating'] = str(rating)
            row['reviews'] = str(reviews)
            csv_updated += 1
            break

with open('data/drinks.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(csv_rows)

print(f'drinks.csv updated: {csv_updated}')

# === 3. Update restaurants.csv ===
with open('data/restaurants.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fieldnames_r = reader.fieldnames
    csv_rows_r = list(reader)

rest_updated = 0
for name, rating, reviews in BREAKFAST_RATINGS:
    jn = name.replace(' ', '').replace('#', '').replace('.', '').replace('-', '')
    for row in csv_rows_r:
        if '楊梅' in (row.get('district') or ''):
            rn = (row.get('name') or '').replace(' ', '').replace('#', '').replace('.', '').replace('-', '')
            if rn == jn or jn in rn or rn in jn:
                row['rating'] = str(rating)
                row['reviews'] = str(reviews)
                rest_updated += 1
                print(f'  ✅ restaurants: {name} → ★{rating}')
                break

with open('data/restaurants.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames_r)
    writer.writeheader()
    writer.writerows(csv_rows_r)

print(f'restaurants.csv updated: {rest_updated}')
