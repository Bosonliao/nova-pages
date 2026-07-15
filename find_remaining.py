import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

target_cities = ['花蓮', '台東', '雲林', '澎湖', '金馬']
remaining = []

for city in target_cities:
    if city not in data:
        continue
    food = data[city].get('food', [])
    for i, r in enumerate(food):
        tags = r.get('tags', [])
        rating = r.get('rating', 0)
        reviews = r.get('reviews', 0)
        dishes = r.get('dishes', [])
        is_michelin = 'michelin' in tags
        is_popular = rating >= 4.0 and reviews >= 1000
        if (is_michelin or is_popular) and (not dishes or len(dishes) == 0):
            remaining.append({'city': city, 'index': i, 'name': r.get('name', ''), 'rating': rating, 'reviews': reviews})

with open('remaining.json', 'w', encoding='utf-8') as f:
    json.dump(remaining, f, ensure_ascii=False, indent=2)

print(f'Total remaining: {len(remaining)}')
# Write to file to avoid encoding issues
with open('remaining.txt', 'w', encoding='utf-8') as f:
    for r in remaining:
        f.write(f"{r['city']}[{r['index']}] {r['name']} (rating={r['rating']}, reviews={r['reviews']})\n")