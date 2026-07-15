# -*- coding: utf-8 -*-
import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Final batch - remaining 12 restaurants
updates = [
    {"city":"花蓮","index":95,"dishes":[
        {"name":"涮涮鍋","desc":"肉出微笑涮涮鍋花蓮店，花蓮人氣微笑涮涮鍋"}
    ]},
    {"city":"花蓮","index":104,"dishes":[
        {"name":"健康餐沙拉","desc":"實季Seedson cafe花蓮店，花蓮人氣健康餐咖啡廳"}
    ]},
    {"city":"花蓮","index":222,"dishes":[
        {"name":"金針山產","desc":"玉里金針山周邊山產，花蓮玉里金針山特色山產料理"}
    ]},
    {"city":"台東","index":189,"dishes":[
        {"name":"海景餐廳","desc":"小魚兒的家，台東都蘭海景餐廳必去"}
    ]},
    {"city":"台東","index":272,"dishes":[
        {"name":"蝴蝶谷秘境","desc":"延平蝴蝶谷秘境，台東延平自然景觀體驗"}
    ]},
    {"city":"台東","index":275,"dishes":[
        {"name":"芋頭冰","desc":"雯雯芋頭冰沒賣飯，台東必吃芋頭冰品"}
    ]},
    {"city":"台東","index":507,"dishes":[
        {"name":"早餐","desc":"明奎早餐店，台東排隊早餐名店必吃"}
    ]},
    {"city":"雲林","index":233,"dishes":[
        {"name":"麵館","desc":"烹小鮮麵館，雲林斗六人氣麵館"}
    ]},
    {"city":"雲林","index":480,"dishes":[
        {"name":"海產","desc":"明湖海產，雲林口湖海產餐廳人氣"}
    ]},
    {"city":"雲林","index":486,"dishes":[
        {"name":"鴨肉羹","desc":"北港李記鴨肉羹，雲林北港必吃鴨肉羹"}
    ]},
    {"city":"澎湖","index":150,"dishes":[
        {"name":"海鮮紫菜冬粉","desc":"清峰海鮮紫菜冬粉，澎湖必吃紫菜冬粉海鮮"}
    ]},
    {"city":"澎湖","index":249,"dishes":[
        {"name":"炸粿","desc":"澎湖回家炸粿，澎湖馬公必吃炸粿"}
    ]}
]

count = 0
for u in updates:
    city = u['city']
    idx = u['index']
    dishes = u['dishes']
    if city in data and idx < len(data[city]['food']):
        existing = data[city]['food'][idx].get('dishes', [])
        if not existing:
            data[city]['food'][idx]['dishes'] = dishes
            count += 1

with open('data-zh.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Total updated: {count}")
print("Saved data-zh.json")