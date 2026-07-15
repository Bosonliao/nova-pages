import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

target_cities = ['花蓮', '台東', '雲林', '澎湖', '金馬']
total_remaining = 0

for city in target_cities:
    if city not in data:
        continue
    food = data[city].get('food', [])
    remaining = 0
    for r in food:
        tags = r.get('tags', [])
        rating = r.get('rating', 0)
        reviews = r.get('reviews', 0)
        dishes = r.get('dishes', [])
        is_michelin = 'michelin' in tags
        is_popular = rating >= 4.0 and reviews >= 1000
        if (is_michelin or is_popular) and (not dishes or len(dishes) == 0):
            remaining += 1
    total_remaining += remaining
    print(f'{city}: {remaining} still need dishes')

print(f'\nTotal remaining: {total_remaining}')