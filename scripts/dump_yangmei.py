import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

print('=== 楊梅區飲料店全部 ===')
has = 0
no = 0
for f in foods:
    if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or [])):
        lat = f.get('lat')
        lng = f.get('lng')
        if lat and lng:
            has += 1
            print(f'  ✅ {f["name"]:30s} ({lat},{lng})')
        else:
            no += 1

print(f'\n有座標: {has}, 無座標: {no}, 總計: {has+no}')
