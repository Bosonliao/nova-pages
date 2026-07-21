import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data['food']
ym = [x for x in foods if x.get('area')=='楊梅區' and any('飲品' in c for c in (x.get('categories') or []))]
print(f'Total: {len(ym)}')
for x in ym:
    print(f'  {x["name"]} | {x.get("rating","?")}★ ({x.get("reviews","?")})')
