import json, sys, io, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

precise = ['UG', '自然湉', '茗茗究市', '茂昌', '花火禾茶', '功夫茶', '金茶伍', '吾奶王']
original = ['50嵐 楊梅大成店', 'CoCo都可 楊梅大成店', '麻古茶坊 楊梅文化店', 'COMEBUY 楊梅大成店']

yangmei = [f for f in foods if f.get('area')=='楊梅區' and any('飲品' in c for c in (f.get('categories') or []))]

# 1. No coords
no_coords = [f for f in yangmei if not f.get('lat') or not f.get('lng')]
print(f'=== 無座標 ({len(no_coords)} 家) ===')
for f in no_coords:
    print(f'  {f["name"]}')

# 2. Need verification (not from Johnny, not from original data)
needs = []
for f in yangmei:
    name = f.get('name', '')
    lat = f.get('lat')
    lng = f.get('lng')
    
    if not lat or not lng:
        continue
    if any(k in name for k in precise):
        continue
    if name in original:
        continue
    
    needs.append(f)

# Group by coordinate
coord_groups = {}
for f in needs:
    key = f'{round(f.get("lat"),4)},{round(f.get("lng"),4)}'
    if key not in coord_groups:
        coord_groups[key] = []
    coord_groups[key].append(f)

print(f'\n=== 座標待確認 ({len(needs)} 家) ===')
for f in sorted(needs, key=lambda x: x.get('address','')):
    addr = f.get('address','')
    # Check if duplicate
    key = f'{round(f.get("lat"),4)},{round(f.get("lng"),4)}'
    dup = '⚠️重複' if len(coord_groups.get(key,[])) > 1 else ''
    print(f'  {f["name"]:30s} | ({f.get("lat"):.5f}, {f.get("lng"):.5f}) | {addr or "無地址":20s} {dup}')

print(f'\n總計：{len(no_coords)} 無座標 + {len(needs)} 待確認 = {len(no_coords)+len(needs)} 家')
