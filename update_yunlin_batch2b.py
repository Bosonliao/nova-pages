import json

path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/yunlin.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

food = data.get('food', [])

# Updated dishes based on real blog posts
dish_map = {
    "彭家飯湯": [
        {"name": "海鮮湯飯", "description": "招牌必吃$120，有鮮蝦、花枝、蚵仔、筍子、魚丸，沙茶湯頭"},
        {"name": "綜合五色生魚片拼盤", "description": "超人氣$500，五種生魚片，新鮮肥美"},
        {"name": "黑鮪魚燥飯", "description": "$50，下飯好吃，附半熟蛋"},
        {"name": "川燙鮮蚵", "description": "$100，肥美蚵仔川燙"}
    ],
    "青松餐廳": [
        {"name": "蟹黃海鮮粥", "description": "餐廳靈魂菜，粥配魚翅羹，每一口都有蟹肉跟魚翅"},
        {"name": "蟹肉魚翅羹", "description": "超級好吃，滑順甜鹹口感，蟹肉加魚翅"},
        {"name": "佛跳牆", "description": "需預訂，宴席菜"},
        {"name": "清蒸魚類", "description": "龍膽、海鱸、石斑都好吃，蒸魚湯汁一流"},
        {"name": "橙汁排骨", "description": "好吃到會重複點兩盤"}
    ]
}

updated = 0
for r in food:
    name = r.get('name', '')
    if name in dish_map:
        r['dishes'] = dish_map[name]
        updated += 1
        print(f'Updated: {name} ({len(dish_map[name])} dishes)')

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\nTotal updated: {updated}')
