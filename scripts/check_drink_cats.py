import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food',[])
drink = [f for f in foods if any('飲品' in c or '飲料' in c for c in f.get('categories',[]))]
yangmei = [f for f in drink if f.get('area')=='楊梅區']
has_coord = [f for f in yangmei if f.get('lat') and f.get('lng')]
print(f'楊梅區飲料店: {len(yangmei)}')
print(f'有座標: {len(has_coord)}')
print(f'全桃園飲料店: {len(drink)}')
for d in yangmei[:5]:
    n = d.get('name','')
    c = d.get('categories',[])
    la = d.get('lat','')
    lo = d.get('lng','')
    print(f'  {n} | cats={c} | lat={la} lng={lo}')

# Also check what categories exist
all_cats = set()
for f in yangmei:
    for c in f.get('categories',[]):
        all_cats.add(c)
print(f'\n楊梅飲料店 category 值: {all_cats}')
