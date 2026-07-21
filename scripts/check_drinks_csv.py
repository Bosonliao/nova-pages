import csv, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/drinks.csv', 'r', encoding='utf-8-sig') as f:
    r = csv.DictReader(f)
    rows = list(r)

ty = [x for x in rows if x.get('county','') == '桃園']
print(f'桃園: {len(ty)} rows')
for x in ty[:5]:
    print(f'  {x["brand"]} {x["store_name"]} | {x["district"]} | lat={x["lat"]} lng={x["lng"]} | {x["address"]}')

has_coords = sum(1 for x in rows if x.get('lat') and x.get('lng'))
print(f'\nTotal drinks.csv: {len(rows)} rows')
print(f'有座標: {has_coords}/{len(rows)}')
print(f'無座標: {len(rows)-has_coords}/{len(rows)}')
