import json

# Fix both files - move restaurants to correct cities
moves = [
    {'name': '金山鴨肉', 'from': '台北', 'to': '新北', 'area': '金山'},
    {'name': '紅毛港海鮮餐廳', 'from': '台北', 'to': '高雄', 'area': '小港'},
    {'name': '阿霞飯店', 'from': '台北', 'to': '台南', 'area': '中西'},
]

for fn in ['data-zh.json', 'data-ja.json']:
    with open(fn, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for move in moves:
        name = move['name']
        from_city = move['from']
        to_city = move['to']
        area = move['area']
        
        # Find and remove from original city
        if from_city not in data or not isinstance(data[from_city], dict):
            continue
        food = data[from_city].get('food', [])
        found = None
        new_food = []
        for r in food:
            if name in r.get('name', ''):
                found = r
                found['area'] = area
            else:
                new_food.append(r)
        data[from_city]['food'] = new_food
        
        # Add to correct city
        if to_city in data and isinstance(data[to_city], dict):
            if found:
                data[to_city]['food'].append(found)
                print(f'[{fn}] {name}: {from_city} -> {to_city} (area={area})')
    
    with open(fn, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print('Done. Both files saved.')
