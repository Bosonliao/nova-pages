# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('data-zh.json','r',encoding='utf-8'))
foods = data['台北']['food']

# Clear wrongly applied dishes at 355-359
wrong = [355, 356, 357, 358, 359]
for i in wrong:
    if 'dishes' in foods[i]:
        nm = foods[i].get('name','?')[:30]
        del foods[i]['dishes']
        print(f'Cleared wrong dishes from idx={i}: {nm}')

# Now apply to correct indices
correct_updates = {
    449: [
        {"name": "麻辣魯肉飯", "desc": "招牌麻辣魯肉飯香辣夠味令人回味，雲鼎阿二麻辣食堂人氣必點超過鍋物"},
        {"name": "麻辣五花牛肉鍋", "desc": "個人麻辣鍋五花牛肉鮮嫩，四川風味辣度可調一人也能享受麻辣鍋"},
        {"name": "霜淇淋", "desc": "免費霜淇淋飲料小菜吃到飽，麻辣食堂超高CP值加碼甜點"}
    ],
    918: [
        {"name": "割包", "desc": "米其林必比登推薦割包可自選肥瘦比例，公館30年老店永遠排隊必吃招牌"},
        {"name": "玉米排骨湯", "desc": "被割包耽誤的玉米排骨湯超級鮮甜，藍家割包本體必點內行人二碗起跳"},
        {"name": "四神湯", "desc": "古早味四神湯搭配割包暖胃，台大公館夜市米其林推薦小吃絕配"}
    ]
}

for idx, dishes in correct_updates.items():
    if idx < len(foods) and not foods[idx].get('dishes'):
        foods[idx]['dishes'] = dishes
        print(f'Added {len(dishes)} dishes to idx={idx}: {foods[idx].get("name","?")[:30]}')

with open('data-zh.json','w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('\nSaved data-zh.json')