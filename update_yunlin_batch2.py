import json

path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/yunlin.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

food = data.get('food', [])

dish_map = {
    "阿國獅魷魚羹": [
        {"name": "魷魚嘴羹", "description": "招牌必吃，斗六美食票選第一名，近80年老店"},
        {"name": "肉羹", "description": "瘦肉口感不錯，湯頭勾芡濃厚度剛好"},
        {"name": "滷魷魚嘴", "description": "人氣必點，慢火熬煮入味，醬汁鹹甜，郭台銘都來吃過"},
        {"name": "滷肉飯", "description": "鄉民推薦必吃，搭配羹湯一起點"},
        {"name": "白菜滷", "description": "鄉民推薦配菜"}
    ],
    "彭家飯湯": [
        {"name": "海鮮飯湯", "description": "招牌必吃，澎派海鮮配料，傳承阿嬤的古早味"},
        {"name": "五色生魚片", "description": "超人氣，新鮮生魚片"},
        {"name": "古早味割稻飯", "description": "古早味再現，飽滿海鮮平價上桌"}
    ],
    "青松餐廳": [
        {"name": "金瓜米粉", "description": "激推必點，在地人強力推薦"},
        {"name": "焗烤海鮮", "description": "桌菜推薦，海鮮料多"},
        {"name": "蟹黃海鮮粥", "description": "招牌必吃，蟹黃鮮甜搭配海鮮粥"}
    ]
}

updated = 0
for r in food:
    name = r.get('name', '')
    if name in dish_map and not r.get('dishes'):
        r['dishes'] = dish_map[name]
        updated += 1
        print(f'Updated: {name} ({len(dish_map[name])} dishes)')

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\nTotal updated: {updated}')
print(f'File saved')
