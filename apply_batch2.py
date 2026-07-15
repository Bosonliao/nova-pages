# -*- coding: utf-8 -*-
import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

updates = [
    # Batch 2 - 花蓮
    {"city":"花蓮","index":21,"dishes":[
        {"name":"月亮蝦餅","desc":"手工製作的泰式月亮蝦餅，外酥內Q無添加麵粉"},
        {"name":"冬蔭功酸辣海鮮湯","desc":"道地泰式酸辣海鮮湯，辛香十足"},
        {"name":"泰式檸檬蒸魚","desc":"新鮮魚肉搭配泰式檸檬醬汁，酸辣開胃"},
        {"name":"香茅打拋豬","desc":"招牌香茅打拋豬，下飯必點"}
    ]},
    {"city":"花蓮","index":22,"dishes":[
        {"name":"自選沙拉健康餐","desc":"12種特調醬料百種組合，原型食材營養滿分"},
        {"name":"大份量高質感沙拉","desc":"多樣食材醬料自己選，吃的健康無負擔"}
    ]},
    {"city":"花蓮","index":28,"dishes":[
        {"name":"韭菜臭豆腐","desc":"招牌韭菜堆成山的臭豆腐，外酥內嫩超涮嘴"},
        {"name":"炸豆包","desc":"獨特炸豆包，銅板價宵夜必點"}
    ]},
    {"city":"花蓮","index":29,"dishes":[
        {"name":"極上海鮮丼","desc":"豪華海鮮生食丼飯，新鮮豐富讓你從海上吃到陸上"},
        {"name":"生魚片丼飯","desc":"新鮮生魚片丼飯，平價高CP值"},
        {"name":"豬排丼","desc":"酥炸豬排丼飯，評價水準俱佳"}
    ]},
    {"city":"花蓮","index":32,"dishes":[
        {"name":"飲料無限暢飲","desc":"門票百元含咖啡果汁無限喝，360度看海景"},
        {"name":"景觀玻璃屋打卡","desc":"玫瑰月亮、白色鋼琴、浪漫鞦韆等打卡造景"}
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