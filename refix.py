import json

# Re-apply the 民主火雞肉飯 fix
for fn in ['data-zh.json', 'data-ja.json']:
    with open(fn, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for city in list(data.keys()):
        if not isinstance(data[city], dict):
            continue
        food = data[city].get('food', [])
        new_food = []
        for r in food:
            name = r.get('name', '')
            if '民主火雞肉飯' in name:
                if city == '嘉義':
                    r['description'] = '嘉義在地人氣火雞肉飯，鮮嫩火雞肉搭配香Q白飯，簡單美味'
                    new_food.append(r)
                # else: skip (remove from wrong cities)
            else:
                new_food.append(r)
        data[city]['food'] = new_food
    
    with open(fn, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print('Re-applied 民主火雞肉飯 fix')
