import csv
f = open(r'C:\Users\USER\.openclaw\workspace\nova-pages\data\restaurants.csv', 'r', encoding='utf-8')
r = csv.DictReader(f)
rows = list(r)
fieldnames = r.fieldnames
print(f"Fields: {fieldnames}")
print(f"Total: {len(rows)}")
empty = sum(1 for x in rows if not x.get('business_hours', '').strip())
print(f"Empty hours: {empty}")
has = sum(1 for x in rows if x.get('business_hours', '').strip())
print(f"Has hours: {has}")
if has > 0:
    for x in rows:
        if x.get('business_hours', '').strip():
            print(f"Sample: {x['name']} -> {x['business_hours']}")
            break