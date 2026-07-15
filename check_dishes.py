import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

total = 0
with_dishes = 0
by_city = {}

for city in data:
    if not isinstance(data[city], dict):
        continue
    food = data[city].get('food', [])
    city_total = len(food)
    city_with = 0
    for r in food:
        if r.get('dishes') and len(r['dishes']) > 0:
            city_with += 1
    by_city[city] = (city_with, city_total)
    total += city_total
    with_dishes += city_with

pct = with_dishes*100//total if total else 0
print(f'{with_dishes}/{total} ({pct}%)')
