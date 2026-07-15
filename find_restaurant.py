import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for city in data:
    if not isinstance(data[city], dict):
        continue
    food = data[city].get('food', [])
    for i, r in enumerate(food):
        n = r.get('name', '')
        if '民主火雞肉飯' in n:
            a = r.get('area', '')
            rating = r.get('rating', '')
            reviews = r.get('reviews', '')
            cat = r.get('category', '') or r.get('categories', '')
            desc = r.get('description', '')[:100]
            print(f'{city} [{i}] {n}')
            print(f'  area={a} rating={rating} reviews={reviews} cat={cat}')
            print(f'  desc={desc}')
            print()
