import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])
yangmei = [f for f in foods if f.get('area') == '楊梅區']
breakfast = [f for f in yangmei if any('早餐' in c or '早午餐' in c for c in f.get('categories',[]))]
print(f'楊梅區總餐飲: {len(yangmei)}')
print(f'楊梅區早餐: {len(breakfast)}')
for b in breakfast:
    n = b.get('name','')
    r = b.get('rating',0)
    a = b.get('address','')
    lat = b.get('lat','')
    lng = b.get('lng','')
    print(f'  {n} | {r} | {a} | ({lat}, {lng})')

# Also check by keyword
kw_breakfast = [f for f in yangmei if '早餐' in f.get('name','') or '早午餐' in f.get('name','') or '晨晨' in f.get('name','') or '晨間' in f.get('name','')]
print(f'\n名稱含早餐關鍵字: {len(kw_breakfast)}')
for b in kw_breakfast:
    n = b.get('name','')
    r = b.get('rating',0)
    a = b.get('address','')
    print(f'  {n} | {r} | {a}')
