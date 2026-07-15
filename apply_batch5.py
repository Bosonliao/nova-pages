# -*- coding: utf-8 -*-
import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Batch 5 - 花蓮 46-90
updates = [
    {"city":"花蓮","index":46,"dishes":[
        {"name":"平價咖啡","desc":"隱身市區二樓的深夜咖啡廳，平價還能微醺"},
        {"name":"水餃拉麵","desc":"居然有賣水餃跟拉麵，深夜也能吃飽"}
    ]},
    {"city":"花蓮","index":50,"dishes":[
        {"name":"特盛丼","desc":"當日先撈生魚片特盛丼，鮭魚紅甘加拿大海膽"},
        {"name":"軍艦壽司","desc":"時令生魚握壽司軍艦，新鮮直送"},
        {"name":"炙燒起司鮭魚","desc":"炙燒起司鮭魚壽司，創意口味"}
    ]},
    {"city":"花蓮","index":56,"dishes":[
        {"name":"海陸無菜單燒烤","desc":"季節時令海陸燒烤饗宴，食材超級新鮮"},
        {"name":"窯烤披薩","desc":"中午限定輕食窯烤披薩，寵物友善餐廳"}
    ]},
    {"city":"花蓮","index":64,"dishes":[
        {"name":"羊駝雞蛋糕","desc":"意外好吃的羊駝雞蛋糕，門票可抵消費"},
        {"name":"免費和服租借","desc":"絕美海景裝置藝術，免費和服租借拍照"},
        {"name":"餵水豚草泥馬","desc":"免費牧草餵草泥馬笑笑羊水豚，親子最愛"}
    ]},
    {"city":"花蓮","index":85,"dishes":[
        {"name":"烤物串燒","desc":"花蓮No.1燒肉居酒屋，烤物串燒都有水準"},
        {"name":"和牛燒肉","desc":"特色和牛燒肉料理，價格親民零負評"},
        {"name":"熱炒料理","desc":"居酒屋熱炒料理，店員熱情氣氛好"}
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
        name = data[city]['food'][idx]['name']
        print(f"Updated {city}[{idx}]")

with open('data-zh.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nTotal updated: {count}")
print("Saved data-zh.json")