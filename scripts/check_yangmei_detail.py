import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])
drinks = [f for f in foods if any('飲品' in c for c in (f.get('categories') or [])) and f.get('area') == '楊梅區']

print(f'楊梅區飲料店: {len(drinks)} 家\n')
for i, d in enumerate(drinks):
    print(f'{i+1}. {d["name"]}')
    print(f'   lat:{d.get("lat")} lng:{d.get("lng")} | {d.get("rating","?")}★ ({d.get("reviews","?")}) | {d.get("address","無地址")}')
    print()
