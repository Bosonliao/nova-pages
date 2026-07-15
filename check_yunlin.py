import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open('data/yunlin.json', encoding='utf-8') as f:
    d = json.load(f)
food = d.get('food', [])
has = sum(1 for r in food if r.get('dishes'))
no = len(food) - has
print(f'雲林總餐廳: {len(food)}, 已有菜色: {has}, 待補: {no}')
need = [(i, r) for i, r in enumerate(food) if not r.get('dishes')]
need.sort(key=lambda x: x[1].get('reviews', 0), reverse=True)
print('\n前10家待補:')
for i, r in need[:10]:
    name = r.get('name', '')
    rev = r.get('reviews', 0)
    area = r.get('area', '')
    print(f'  [{i}] {name} ({rev} reviews, {area})')
