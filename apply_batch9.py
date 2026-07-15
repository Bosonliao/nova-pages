# -*- coding: utf-8 -*-
import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Batch 9 - 花蓮 remaining + 台東 start
updates = [
    # 花蓮 remaining
    {"city":"花蓮","index":281,"dishes":[
        {"name":"牛骨牛肉麵","desc":"一碗兩根牛骨肉超霸氣，清燉湯頭回甘不膩，CP值爆表"},
        {"name":"滷肉飯","desc":"膠質滿滿必點滷肉飯，郊區排隊名店"}
    ]},
    {"city":"花蓮","index":282,"dishes":[
        {"name":"牛骨牛肉麵","desc":"超大塊帶骨牛肉，每日現熬湯頭，Google 4.5星"}
    ]},
    {"city":"花蓮","index":345,"dishes":[
        {"name":"花生豆腐","desc":"鳳林特產花生豆腐，綿密滑嫩特殊口感"}
    ]},
    {"city":"花蓮","index":349,"dishes":[
        {"name":"合菜","desc":"闔家歡南北餚餐館，花蓮老牌合菜餐廳"}
    ]},
    {"city":"花蓮","index":354,"dishes":[
        {"name":"小和山谷","desc":"小和山谷花蓮質感餐廳，打卡熱點"}
    ]},
    {"city":"花蓮","index":364,"dishes":[
        {"name":"米粉湯","desc":"歐桑米粉湯花蓮人氣米粉湯，浴火重生"}
    ]},
    {"city":"花蓮","index":418,"dishes":[
        {"name":"慶豐麵店","desc":"慶豐麵店花蓮壽豐必吃，乾麵小菜超推"}
    ]},
    {"city":"花蓮","index":485,"dishes":[
        {"name":"玉里麵","desc":"馬蓋先美食玉里麵，花蓮玉里必吃特色麵食"}
    ]},
    {"city":"花蓮","index":486,"dishes":[
        {"name":"玉里麵","desc":"小木屋玉里麵，花蓮玉里必吃麵店"}
    ]},
    {"city":"花蓮","index":531,"dishes":[
        {"name":"玉里麵","desc":"璞石閣玉里麵，花蓮玉里經典麵食"}
    ]},
    {"city":"花蓮","index":570,"dishes":[
        {"name":"玉里麵","desc":"傳統美食玉里麵，花蓮玉里老牌麵店"}
    ]},
    # 台東 start
    {"city":"台東","index":29,"dishes":[
        {"name":"無菜單海鮮料理","desc":"高CP值無菜單海鮮料理，新鮮精緻很飽足"},
        {"name":"龍蝦痛風粥","desc":"波士頓龍蝦松露痛風粥，鮮美提升一個層次"}
    ]},
    {"city":"台東","index":408,"dishes":[
        {"name":"柴魚米苔目","desc":"60年經典柴魚米苔目，肉燥柴魚烏醋三大靈魂缺一不可"},
        {"name":"滷味小菜","desc":"菜單滷味小菜也好好吃，台東必吃美食"}
    ]},
    {"city":"台東","index":412,"dishes":[
        {"name":"柴魚米苔目","desc":"榕樹下米苔目小滿雨生，50年老店破萬網友推薦"}
    ]},
    {"city":"台東","index":415,"dishes":[
        {"name":"炸雞腿","desc":"薄脆外皮肉汁噴水池湧出，500碗推薦必點","price":"120"},
        {"name":"炸雞餐","desc":"加15元雞翅升級雞腿，老饕隱藏版點餐法"}
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