import json, glob, sys
sys.stdout.reconfigure(encoding='utf-8')

total = 0
no_coords = 0
for f in glob.glob('data/*.json'):
    if f.endswith('meta.json') or f.endswith('nightmarkets.json'): continue
    with open(f, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    for key in ['food','foods','restaurants','souvenirs','spots']:
        for item in data.get(key, []):
            total += 1
            lat = item.get('lat')
            lng = item.get('lng')
            if lat is None or lng is None:
                no_coords += 1

print(f'Total items: {total}')
print(f'Items without coords: {no_coords}')
print(f'Items with coords: {total - no_coords}')

# 檢查台北美食前10筆
with open('data/taipei.json', 'r', encoding='utf-8') as fh:
    d = json.load(fh)
food = d.get('food', [])
print(f'\nTaipei food items: {len(food)}')
for item in food[:5]:
    print(f'  {item.get("name","")}: lat={item.get("lat")}, lng={item.get("lng")}')