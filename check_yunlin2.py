import json

path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/yunlin.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

restaurants = data.get('restaurants', [])
need_dishes = []
have_dishes = []

for r in restaurants:
    dishes = r.get('dishes', [])
    if dishes and len(dishes) > 0:
        have_dishes.append(r)
    else:
        need_dishes.append(r)

# Sort by reviews count (most popular first)
need_dishes.sort(key=lambda x: x.get('reviews', 0), reverse=True)

print(f'Yunlin total: {len(restaurants)}')
print(f'Have dishes: {len(have_dishes)}')
print(f'Need dishes: {len(need_dishes)}')
print(f'\nTop 10 to process:')
for i, r in enumerate(need_dishes[:10]):
    print(f'  [{r.get("id")}] {r.get("name")} ({r.get("reviews",0)} reviews, {r.get("city","")})')
