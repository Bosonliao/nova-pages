import csv
f = open(r'C:\Users\USER\.openclaw\workspace\nova-pages\data\restaurants.csv', 'r', encoding='utf-8')
r = csv.DictReader(f)
rows = [x for x in r if x.get('county','') == '桃園' and x.get('district','') == '楊梅區' and not x.get('business_hours','').strip()]
print(f'楊梅區缺營業時間: {len(rows)}筆')
for x in rows[:20]:
    print(f'  {x["name"]}')