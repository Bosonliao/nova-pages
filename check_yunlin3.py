import json

path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/yunlin.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

food = data.get('food', [])
need_dishes = [r for r in food if not r.get('dishes')]
have_dishes = [r for r in food if r.get('dishes')]

need_dishes.sort(key=lambda x: x.get('reviews', 0), reverse=True)

print(f'Yunlin total: {len(food)}')
print(f'Have dishes: {len(have_dishes)}')
print(f'Need dishes: {len(need_dishes)}')
print(f'\nTop 10 to process:')
for i, r in enumerate(need_dishes[:10]):
    print(f'  [{r.get("name","")}] ({r.get("reviews",0)} reviews, {r.get("area","")})')
