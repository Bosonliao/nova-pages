import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

# Add 麻古茶坊 楊梅文化店
new_shop = {
    "name": "麻古茶坊 楊梅文化店",
    "place_id": "",
    "lat": 24.9185,
    "lng": 121.1840,
    "rating": 4.3,
    "reviews": 258,
    "address": "桃園市楊梅區光華里文化街167號",
    "area": "楊梅區",
    "categories": ["飲品"],
    "description": ""
}

# Check if already exists by name+area
exists = any(f.get('name') == new_shop['name'] and f.get('area') == '楊梅區' for f in foods)
if not exists:
    foods.append(new_shop)
    data['food'] = foods
    with open('data/taoyuan.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'Added: {new_shop["name"]} ({new_shop["rating"]}★ {new_shop["reviews"]} reviews)')
    print(f'Total foods: {len(foods)}')
else:
    print('Already exists')
