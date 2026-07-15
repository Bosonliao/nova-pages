# -*- coding: utf-8 -*-
import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Batch 7 - 花蓮 100-185
updates = [
    {"city":"花蓮","index":100,"dishes":[
        {"name":"燒肉吃到飽","desc":"種類超多CP值高燒肉鍋物吃到飽，哈根達斯吃到飽","price":"499"},
        {"name":"炙燒握壽司","desc":"炙燒握壽司吃到飽，壽星有優惠"}
    ]},
    {"city":"花蓮","index":101,"dishes":[
        {"name":"無菜單料理","desc":"三十年主廚經驗，當季新鮮食材變化出藝術品般料理"},
        {"name":"帝王蟹牛奶鍋","desc":"必吃帝王蟹牛奶鍋，追火車秘境餐廳"},
        {"name":"庭園景觀","desc":"四千坪場地，水豚羊駝笑笑羊，邊用餐邊看火車"}
    ]},
    {"city":"花蓮","index":102,"dishes":[
        {"name":"麻糬鬆餅","desc":"招牌蒸籠QQ麻糬鬆餅，鬆軟Q彈必點"},
        {"name":"鮮蝦義大利麵","desc":"鮮蝦義大利麵，美式風格複合式咖啡"},
        {"name":"燻鮭魚法式蛋捲","desc":"法式蛋捲系列，寵物友善有店狗"}
    ]},
    {"city":"花蓮","index":112,"dishes":[
        {"name":"自選餐盒","desc":"升級版爭鮮迴轉壽司，列車送餐小孩最愛"},
        {"name":"迴轉壽司","desc":"多元餐點可以吃得很滿足，大排長龍"}
    ]},
    {"city":"花蓮","index":121,"dishes":[
        {"name":"法式香煎鴨胸","desc":"超美味軟嫩法式鴨胸，單推這一項必點"},
        {"name":"原塊牛排套餐","desc":"西堤特選套餐，晚間最熱門"},
        {"name":"松露牛排套餐","desc":"松露牛排特選套餐，人氣選擇"}
    ]},
    {"city":"花蓮","index":117,"dishes":[
        {"name":"個人燒肉plus+","desc":"個人燒肉套餐，直火炙燒丼飯"}
    ]},
    {"city":"花蓮","index":140,"dishes":[
        {"name":"炭火乾式熟成牛排","desc":"40人包場空間，炭火乾式熟成牛排館"}
    ]},
    {"city":"花蓮","index":143,"dishes":[
        {"name":"壽豐小吃","desc":"壽豐在地小吃，慶豐店人氣美食"}
    ]},
    {"city":"花蓮","index":159,"dishes":[
        {"name":"家常料理","desc":"陳家食堂家常菜，溫馨口味"}
    ]},
    {"city":"花蓮","index":160,"dishes":[
        {"name":"麵食專家","desc":"六里屯麵食專家美崙旗艦店，北方麵食"}
    ]},
    {"city":"花蓮","index":165,"dishes":[
        {"name":"燒肉套餐","desc":"石屋燒肉人氣火鍋燒肉，花蓮必吃"}
    ]},
    {"city":"花蓮","index":168,"dishes":[
        {"name":"手沖咖啡","desc":"珈琲花手沖咖啡，花蓮文青咖啡店"}
    ]},
    {"city":"花蓮","index":174,"dishes":[
        {"name":"壽司生魚片","desc":"櫻花壽司日本料理，新鮮生魚片壽司"}
    ]},
    {"city":"花蓮","index":181,"dishes":[
        {"name":"麻糬甜點","desc":"杜倫先生花蓮名產麻糬蛋糕，伴手禮必買"}
    ]},
    {"city":"花蓮","index":182,"dishes":[
        {"name":"八百里燒肉","desc":"八百里燒肉套餐，炭火燒肉"}
    ]},
    {"city":"花蓮","index":185,"dishes":[
        {"name":"牛排套餐","desc":"歐鄉牛排館花蓮店，平價牛排西餐"}
    ]},
    {"city":"花蓮","index":186,"dishes":[
        {"name":"牛排套餐","desc":"來來牛排花蓮店，在地老牌牛排館"}
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