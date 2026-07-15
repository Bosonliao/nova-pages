import json

# Fix both files
for fn in ['data-zh.json', 'data-ja.json']:
    with open(fn, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    removed = []
    fixed = []
    
    for city in data:
        if not isinstance(data[city], dict):
            continue
        food = data[city].get('food', [])
        new_food = []
        for r in food:
            name = r.get('name', '')
            if '民主火雞肉飯' in name:
                if city == '嘉義':
                    # Fix description - it's not a dessert shop!
                    r['description'] = '嘉義在地人氣火雞肉飯，鮮嫩火雞肉搭配香Q白飯，簡單美味'
                    # Fix area - 東區 is correct for 嘉義市
                    fixed.append(f'{city}: kept + fixed description')
                    new_food.append(r)
                else:
                    removed.append(f'{city}: removed')
            else:
                new_food.append(r)
        data[city]['food'] = new_food
    
    with open(fn, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f'=== {fn} ===')
    for r in removed:
        print(f'  {r}')
    for r in fixed:
        print(f'  {r}')
    print()
