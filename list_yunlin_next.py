import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/yunlin.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

food = data.get('food', [])
need_dishes = [r for r in food if not r.get('dishes')]
need_dishes.sort(key=lambda x: x.get('reviews', 0), reverse=True)

print(f'Need dishes: {len(need_dishes)}')
print(f'\nNext 13 (rank 8-20):')
for i, r in enumerate(need_dishes[:13]):
    print(f'{i+8}. {r.get("name","")} ({r.get("reviews",0)} reviews, {r.get("area","")})')
