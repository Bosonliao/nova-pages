import json, sys, csv
sys.stdout = open(sys.stdout.fileno(), 'w', encoding='utf-8')

f = open('restaurants.csv', 'r', encoding='utf-8-sig')
r = csv.DictReader(f)
rows = list(r)
f.close()

print('Columns:', r.fieldnames)
print()

for row in rows[:5]:
    print(f"Name: {row['name']}, Rating: {row['rating']}, Hours: {row['business_hours']}, Source: {row['source']}")
print()

# Check data-zh.json
f2 = open('../data-zh.json', 'r', encoding='utf-8')
d = json.load(f2)
f2.close()
if isinstance(d, list):
    print(f"data-zh.json is a list, len: {len(d)}")
    if d:
        print(f"First item keys: {list(d[0].keys())}")
        print(f"First item: {dict(list(d[0].items())[:12])}")
elif isinstance(d, dict):
    print(f"data-zh.json is a dict, keys: {list(d.keys())[:10]}")
    first_key = list(d.keys())[0]
    print(f"First entry: {d[first_key]}")