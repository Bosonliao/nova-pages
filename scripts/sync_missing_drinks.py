"""
Sync missing drink shops from drinks.csv (with coords) into city JSONs
"""
import json, csv, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')

now = '2026-07-19'

# Load drinks.csv
with open('data/drinks.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    all_drinks = list(reader)

# Group by county
county_map = {'桃園': 'taoyuan.json', '新竹': 'hsinchu.json', '苗栗': 'miaoli.json'}

for county, fname in county_map.items():
    drinks = [r for r in all_drinks if r.get('county') == county and r.get('lat') and r.get('lng')]
    
    data = json.load(open(f'data/{fname}', 'r', encoding='utf-8'))
    foods = data.get('food', [])
    json_names_norm = set()
    for f in foods:
        n = (f.get('name') or '').replace(' ', '').replace('#', '').replace('.', '').replace('-', '')
        json_names_norm.add(n)
    
    added = 0
    for r in drinks:
        full_name = f"{r.get('brand','')} {r.get('store_name','')}".strip()
        normalized = full_name.replace(' ', '').replace('#', '').replace('.', '').replace('-', '')
        
        # Check if already in JSON
        found = any(normalized in jn or jn in normalized for jn in json_names_norm)
        if not found:
            district = r.get('district', '')
            foods.append({
                "name": full_name,
                "place_id": "",
                "lat": float(r['lat']),
                "lng": float(r['lng']),
                "rating": 0,
                "reviews": 0,
                "address": r.get('address', ''),
                "area": district,
                "categories": ["飲品"],
                "description": ""
            })
            added += 1
            print(f'  + {full_name} | {district}')
    
    if added > 0:
        data['food'] = foods
        with open(f'data/{fname}', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f'{county}: added {added}')
    else:
        print(f'{county}: nothing to add')
