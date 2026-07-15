import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open('data-zh.json', encoding='utf-8') as f:
    data = json.load(f)

targets = ['復興路炸醬麵', '大麵章', '宜蘭廟口紅糟魷魚']
for city, d in data.items():
    if not isinstance(d, dict):
        continue
    for i, r in enumerate(d.get('food', [])):
        name = r.get('name', '')
        for t in targets:
            if t in name:
                dishes = r.get('dishes', [])
                desc = r.get('description', '')[:80]
                print(f'{city}[{i}] {name}')
                print(f'  desc: {desc}')
                print(f'  dishes: {len(dishes)}')
                for dish in dishes:
                    if isinstance(dish, dict):
                        dn = dish.get('name', '')
                        dd = dish.get('description', '')[:80]
                        print(f'    - {dn}: {dd}')
                    else:
                        print(f'    - {dish}')
                print()
