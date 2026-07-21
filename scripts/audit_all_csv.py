import csv, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

files = ['restaurants.csv', 'drinks.csv', 'spots.csv', 'souvenirs.csv', 'nightmarkets.csv', 'routes.csv']
for fn in files:
    path = os.path.join('data', fn)
    if not os.path.exists(path):
        print(f'{fn}: NOT FOUND')
        continue
    with open(path, 'r', encoding='utf-8-sig') as f:
        r = csv.DictReader(f)
        rows = list(r)
        cols = list(r.fieldnames)
        lat_col = 'lat' if 'lat' in cols else ('latitude' if 'latitude' in cols else None)
        lng_col = 'lng' if 'lng' in cols else ('longitude' if 'longitude' in cols else None)
        
        has_coords = 0
        if lat_col and lng_col:
            has_coords = sum(1 for x in rows if x.get(lat_col) and x.get(lng_col))
        
        total = len(rows)
        pct = f' ({100*has_coords//total}%)' if total else ''
        print(f'{fn:25s} | {total:5d} rows | coords: {has_coords}/{total}{pct}')
        print(f'  columns: {cols}')
        print()
