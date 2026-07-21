import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])
drinks = [f for f in foods if any('飲品' in c for c in (f.get('categories') or []))]
for d in drinks[:5]:
    print(f'name: {d["name"]}')
    print(f'  lat: {d.get("lat")}, lng: {d.get("lng")}')
    print(f'  area: {d.get("area")}')
    print()
