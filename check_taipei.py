import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Check these restaurants in Taipei
targets = ['金山鴨肉', '紅毛港海鮮', '阿霞飯店', '蓬萊餐廳']

for target in targets:
    print(f'\n=== {target} ===')
    for city in data:
        if not isinstance(data[city], dict):
            continue
        food = data[city].get('food', [])
        for i, r in enumerate(food):
            if target in r.get('name', ''):
                print(f'  {city} [{i}] {r["name"]}')
                print(f'    area={r.get("area","")} rating={r.get("rating","")} reviews={r.get("reviews","")}')
                print(f'    michelin={r.get("michelin","")} category={r.get("category","")}')
                print(f'    desc={r.get("description","")[:100]}')
