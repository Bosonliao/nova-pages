# -*- coding: utf-8 -*-
import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Batch 6 - 花蓮 87-102
updates = [
    {"city":"花蓮","index":87,"dishes":[
        {"name":"鹽烤台灣鯛","desc":"350元起無菜單原住民料理，巨無霸鹽烤台灣鯛","price":"350"},
        {"name":"馬告香腸","desc":"原住民風味馬告香腸，香氣獨特"},
        {"name":"情人的眼淚","desc":"原住民特色野菜料理，口感滑嫩"},
        {"name":"滷肉飯吃到飽","desc":"內用滷肉飯吃到飽，高CP值"}
    ]},
    {"city":"花蓮","index":88,"dishes":[
        {"name":"桶仔雞","desc":"必吃桶仔雞，雞肉不乾柴淋上雞油超無敵"},
        {"name":"烤台灣鯛","desc":"無菜單料理烤魚，魚肉鮮美"},
        {"name":"滷肉飯吃到飽","desc":"內用滷肉飯吃到飽，帶洋酒不收開瓶費","price":"420"}
    ]},
    {"city":"花蓮","index":89,"dishes":[
        {"name":"滷肉飯吃到飽","desc":"內用滷肉飯吃到飽，帶洋酒不收開瓶費"}
    ]},
    {"city":"花蓮","index":90,"dishes":[
        {"name":"蜜糖吐司","desc":"必點蜜糖吐司搭香草冰淇淋，價格超甜"},
        {"name":"和風白醬義大利麵","desc":"人氣和風白醬義大利麵，Creamy不膩"},
        {"name":"白酒蛤蜊義大利麵","desc":"超彈牙白酒蛤蜊義大利麵，加100元套餐很划算","price":"100"},
        {"name":"抹茶巴斯克","desc":"人氣甜點抹茶巴斯克，必點推薦"}
    ]},
    {"city":"花蓮","index":94,"dishes":[
        {"name":"我是龍蝦鍋","desc":"12種湯頭任選，龍蝦鍋超霸氣"},
        {"name":"黑魯飯","desc":"招牌黑滷飯，自助吧白飯滷肉飯霜淇淋無限取"},
        {"name":"蒙古天香湯底","desc":"特色蒙古天香湯底，寵物友善餐廳"}
    ]},
    {"city":"花蓮","index":96,"dishes":[
        {"name":"煙燻豬肉鍋","desc":"特色煙燻豬肉鍋，DIY料理體驗有趣"},
        {"name":"霜淇淋吃到飽","desc":"霜淇淋無限自取，親子友善有溜滑梯"}
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
        print(f"Updated {city}[{idx}]")

with open('data-zh.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nTotal updated: {count}")
print("Saved data-zh.json")