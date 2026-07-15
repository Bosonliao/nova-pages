# -*- coding: utf-8 -*-
import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Batch 4 - 花蓮 39-45
updates = [
    {"city":"花蓮","index":39,"dishes":[
        {"name":"個人獨享鴛鴦鍋","desc":"六種湯頭任意組合，不加收鍋底費","price":"399"},
        {"name":"牛豚9宮格","desc":"必點牛豚9宮格肉品組合，厚切品質佳"},
        {"name":"泰國明果冰淇淋","desc":"吃到飽含榴槤冰淇淋，平日午餐399免服務費"}
    ]},
    {"city":"花蓮","index":41,"dishes":[
        {"name":"熟成牛豬雞鴨羊肉","desc":"多款肉品選擇多品質佳，自助吧豐盛"},
        {"name":"自助吧吃到飽","desc":"蔬菜菇類火鍋料應有盡有，王子麵雞蛋無限自取"}
    ]},
    {"city":"花蓮","index":43,"dishes":[
        {"name":"經濟鍋","desc":"平日午餐150元就有，加一元送好料","price":"150"},
        {"name":"即食熟食鍋","desc":"外送招牌即食熟食鍋，營業至凌晨2點"}
    ]},
    {"city":"花蓮","index":44,"dishes":[
        {"name":"胡椒豬肚鍋","desc":"港式特色鍋底，胡椒香氣濃郁的豬肚湯頭"},
        {"name":"港式花雕雞","desc":"花雕酒香浸入雞肉，港式獨特湯頭"},
        {"name":"香菜皮蛋鍋","desc":"香港才有的特色湯頭，香菜皮蛋風味獨特"}
    ]},
    {"city":"花蓮","index":45,"dishes":[
        {"name":"現撈海鮮燒烤","desc":"花蓮現撈海鮮搭配炭烤，食尚玩家推薦"},
        {"name":"烤鮮蚵","desc":"新鮮肥美的烤鮮蚵，海鮮控必點"}
    ]}
]

count = 0
for u in updates:
    city = u['city']
    idx = u['index']
    dishes = u['dishes']
    if city in data and idx < len(data[city]['food']):
        data[city]['food'][idx]['dishes'] = dishes
        count += 1
        print(f"Updated {city}[{idx}] {data[city]['food'][idx]['name']}")

with open('data-zh.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nTotal updated: {count}")
print("Saved data-zh.json")