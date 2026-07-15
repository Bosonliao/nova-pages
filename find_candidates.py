import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

target_cities = ['花蓮', '台東', '雲林', '澎湖', '金馬']
total = 0
output_lines = []

for city in target_cities:
    if city not in data:
        output_lines.append(f'{city}: NOT FOUND in data')
        continue
    food = data[city].get('food', [])
    candidates = []
    for i, r in enumerate(food):
        tags = r.get('tags', [])
        rating = r.get('rating', 0)
        reviews = r.get('reviews', 0)
        dishes = r.get('dishes', [])
        is_michelin = 'michelin' in tags
        is_popular = rating >= 4.0 and reviews >= 1000
        if (is_michelin or is_popular) and (not dishes or len(dishes) == 0):
            candidates.append({
                'index': i,
                'name': r.get('name', ''),
                'tags': tags,
                'rating': rating,
                'reviews': reviews,
                'is_michelin': is_michelin,
                'is_popular': is_popular
            })
    total += len(candidates)
    output_lines.append(f'{city}: {len(food)} total, {len(candidates)} candidates')
    for c in candidates:
        label = 'michelin' if c['is_michelin'] else 'popular'
        idx = c['index']
        name = c['name']
        rt = c['rating']
        rv = c['reviews']
        output_lines.append(f'  [{idx}] {name} (rating={rt}, reviews={rv}, {label})')

output_lines.append(f'\nTotal candidates: {total}')

with open('candidates_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print('Done. Written to candidates_output.txt')