import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

print('=== 楊梅區飲料店缺評分 ===')
no_rating = []
for f in foods:
    if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or [])):
        if not f.get('rating') or f.get('rating') == 0:
            no_rating.append(f)
            addr = f.get('address','')
            addr_s = addr.replace('桃園市楊梅區','') if addr else '無地址'
            print(f'  {f["name"]} | {addr_s}')

print(f'\nTotal: {len(no_rating)}')
