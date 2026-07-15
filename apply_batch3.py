# -*- coding: utf-8 -*-
import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Batch 3 - 花蓮 34-45
updates = [
    {"city":"花蓮","index":34,"dishes":[
        {"name":"龍蝦海鮮拼盤","desc":"超霸氣龍蝦海鮮拼盤，附設停車場超方便"},
        {"name":"自助吧吃到飽","desc":"蔬菜麵食滷肉飯飲料冰淇淋無限量供應"}
    ]},
    {"city":"花蓮","index":35,"dishes":[
        {"name":"新鮮海鮮鍋","desc":"滿滿的蝦子超級爽，雞蛋自助吧免費取用"},
        {"name":"明治冰淇淋吃到飽","desc":"花蓮最強火鍋自助吧台，十多種飲料無限享用"}
    ]},
    {"city":"花蓮","index":36,"dishes":[
        {"name":"頂級肉品熟食吃到飽","desc":"千萬裝潢高質感鍋物店，熟食火鍋料自助無限"},
        {"name":"雪花牛鍋","desc":"高品質雪花牛，搭配豐盛自助吧"}
    ]},
    {"city":"花蓮","index":37,"dishes":[
        {"name":"鯛魚鍋","desc":"魚片份量充足，目前吃過最好吃的鯛魚鍋","price":"400"},
        {"name":"雪花牛鍋","desc":"雪花牛肉質優良，環境超乾淨"},
        {"name":"北海道冰淇淋","desc":"每種口味都好吃，研磨咖啡也不錯"}
    ]},
    {"city":"花蓮","index":38,"dishes":[
        {"name":"麻辣鴛鴦鍋","desc":"帶有牛油香氣的麻辣鍋，鴨血豆腐不限量"},
        {"name":"滷肉飯吃到飽","desc":"醬料白飯滷肉飯自取無限量供應"}
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