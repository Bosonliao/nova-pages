import json, csv, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')

# Check drinks.csv
with open('data/drinks.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    csv_rows = list(reader)

# Count by county
from collections import Counter
county_count = Counter()
county_with_coords = Counter()
for r in csv_rows:
    c = r.get('county', '')
    county_count[c] += 1
    if r.get('lat') and r.get('lng'):
        county_with_coords[c] += 1

print('=== drinks.csv 現況 ===')
for c in sorted(county_count.keys()):
    total = county_count[c]
    coords = county_with_coords[c]
    print(f'  {c}: {total} 家, 有座標 {coords}')

# Check what's in each city JSON - drink shops
json_files = {
    '桃園': 'taoyuan.json',
    '新竹': 'hsinchu.json',
    '苗栗': 'miaoli.json',
}

print('\n=== 各 JSON 飲料店現況 ===')
for county, fname in json_files.items():
    data = json.load(open(f'data/{fname}', 'r', encoding='utf-8'))
    foods = data.get('food', [])
    drink = [f for f in foods if any('飲品' in c for c in f.get('categories', []))]
    with_coords = [f for f in drink if f.get('lat') and f.get('lng')]
    print(f'  {county}: {len(foods)} 總餐飲, {len(drink)} 飲料, {len(with_coords)} 有座標')

# Check drinks.csv that are NOT in JSON yet
print('\n=== drinks.csv 有座標但 JSON 可能沒有的 ===')
for county, fname in json_files.items():
    data = json.load(open(f'data/{fname}', 'r', encoding='utf-8'))
    foods = data.get('food', [])
    json_names = set((f.get('name') or '').replace(' ', '').replace('#', '').replace('.', '') for f in foods)
    
    csv_for_county = [r for r in csv_rows if r.get('county', '') == county and r.get('lat') and r.get('lng')]
    not_in_json = []
    for r in csv_for_county:
        full = f"{r.get('brand','')} {r.get('store_name','')}".strip()
        normalized = full.replace(' ', '').replace('#', '').replace('.', '')
        if not any(normalized in jn or jn in normalized for jn in json_names):
            not_in_json.append(full)
    
    if not_in_json:
        print(f'  {county}: {len(not_in_json)} 家在 CSV 有座標但 JSON 裡沒有')
        for n in not_in_json[:10]:
            print(f'    - {n}')
        if len(not_in_json) > 10:
            print(f'    ... 還有 {len(not_in_json)-10} 家')
