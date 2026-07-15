# -*- coding: utf-8 -*-
import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Batch 8 - 花蓮 remaining + some well-known ones
updates = [
    {"city":"花蓮","index":193,"dishes":[
        {"name":"燒餅加料","desc":"50年創始老店，蔥爆牛肉燒餅實在創意，0900前就賣光"},
        {"name":"鹹豆漿","desc":"北方早點招牌鹹豆漿，眷村味必點"}
    ]},
    {"city":"花蓮","index":221,"dishes":[
        {"name":"咖哩麵包","desc":"全台首創日式咖哩麵包專賣，外酥內軟微甜不辣","price":"45"},
        {"name":"炸咖哩麵包","desc":"天然發酵金黃炸香，500碗推薦必吃排隊小吃"}
    ]},
    {"city":"花蓮","index":415,"dishes":[
        {"name":"脆皮臭豆腐","desc":"三鍋油炸秘技，清爽蘿蔔絲與泡菜完美平衡，臭豆腐界天花板"}
    ]},
    {"city":"花蓮","index":417,"dishes":[
        {"name":"脆皮臭豆腐","desc":"不科學脆皮臭豆腐，玉里地標美食必吃"}
    ]},
    {"city":"花蓮","index":422,"dishes":[
        {"name":"咖哩飯","desc":"花蓮知名咖哩專賣，進駐將軍府日式老宅"},
        {"name":"飯醬吃到飽","desc":"學生最愛飯醬吃到飽，不用擔心份量"}
    ]},
    {"city":"花蓮","index":558,"dishes":[
        {"name":"黃金蜆料理","desc":"黃金蜆的故鄉，炒蜊仔清蒸貴妃魚必吃"},
        {"name":"鹽烤活力鯛","desc":"五餅二魚餐廳招牌鹽烤魚，平價大份量"},
        {"name":"蜆仔霜淇淋","desc":"獨特蜆仔霜淇淋，漁場特色甜點"},
        {"name":"摸蜆體驗","desc":"親自下水挖蜆體驗，憑票帶走一斤黃金蜆"}
    ]},
    {"city":"花蓮","index":564,"dishes":[
        {"name":"炸蛋蔥油餅","desc":"花蓮必吃炸蛋蔥油餅，藍車黃車都超有名"}
    ]},
    {"city":"花蓮","index":565,"dishes":[
        {"name":"炸蛋蔥油餅","desc":"花蓮必吃炸蛋蔥油餅黃車，人氣排隊美食"}
    ]},
    {"city":"花蓮","index":566,"dishes":[
        {"name":"扁食","desc":"液香扁食店花蓮老牌扁食，皮薄餡鮮"}
    ]},
    {"city":"花蓮","index":567,"dishes":[
        {"name":"扁食","desc":"戴記扁食花蓮名產，手工扁食皮薄餡多"}
    ]},
    {"city":"花蓮","index":568,"dishes":[
        {"name":"玉里麵","desc":"阿森麵店玉里麵，花蓮玉里必吃特色麵食"}
    ]},
    {"city":"花蓮","index":571,"dishes":[
        {"name":"055龍蝦海鮮","desc":"花蓮知名龍蝦海鮮餐廳，新鮮直送"}
    ]},
    {"city":"花蓮","index":495,"dishes":[
        {"name":"香扁食","desc":"花蓮香扁食，花蓮扁食名店之一"}
    ]},
    {"city":"花蓮","index":499,"dishes":[
        {"name":"平價壽司","desc":"田村壽司花蓮人氣壽司店，平價日式料理"}
    ]},
    {"city":"花蓮","index":506,"dishes":[
        {"name":"泰式燒烤","desc":"米噹泰式燒烤，花蓮泰式風味燒烤"}
    ]},
    {"city":"花蓮","index":478,"dishes":[
        {"name":"雞湯小卷米粉","desc":"單一純賣雞湯小卷米粉，鮮甜湯頭必點"}
    ]},
    {"city":"花蓮","index":481,"dishes":[
        {"name":"炸蛋蔥油餅","desc":"老牌炸蛋蔥油餅藍車，花蓮排隊必吃"}
    ]},
    {"city":"花蓮","index":529,"dishes":[
        {"name":"鵝肉","desc":"鵝肉先生花蓮人氣鵝肉店，鮮嫩多汁"}
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