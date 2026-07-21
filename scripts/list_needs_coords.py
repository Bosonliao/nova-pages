import json, sys, io, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

# Johnny's precise coords for reference
precise = {
    'UG': (24.91266, 121.14441),
    '自然湉': (24.91187, 121.14385),
    '茗茗究市': (24.91386, 121.14583),
    '茂昌': (24.91458, 121.14652),
    '花火禾茶': (24.91032, 121.15786),
    '功夫茶': (24.91523, 121.18042),
    '金茶伍': (24.91316, 121.17387),
    '吾奶王': (24.91892, 121.18231),
}

# All Yangmei drink shops
yangmei = [f for f in foods if f.get('area')=='楊梅區' and any('飲品' in c for c in (f.get('categories') or []))]

# 1. No coordinates
no_coords = [f for f in yangmei if not f.get('lat') or not f.get('lng')]
print(f'=== 無座標 ({len(no_coords)} 家) ===')
for f in no_coords:
    print(f'  {f["name"]}')

# 2. Suspect coordinates (from Playwright Google Maps, might be inaccurate)
# These are ones NOT in Johnny's precise list and NOT in the original data
# Group by coordinate to find duplicates
coord_groups = {}
for f in yangmei:
    lat = f.get('lat')
    lng = f.get('lng')
    if lat and lng:
        key = f'{round(lat,4)},{round(lng,4)}'
        if key not in coord_groups:
            coord_groups[key] = []
        coord_groups[key].append(f)

print(f'\n=== 重複座標（可能不準）===')
for key, shops in coord_groups.items():
    if len(shops) > 1:
        print(f'\n  座標 ({key}) — {len(shops)} 家：')
        for s in shops:
            print(f'    {s["name"]:30s} | addr: {s.get("address","無")}')

# 3. List all that have address but coords might be wrong
# (not in Johnny's precise list, and address doesn't match coords area)
print(f'\n=== 有地址但座標可能需要確認 ===')
exclude = list(precise.keys()) + ['50嵐', 'CoCo', '麻古', 'COMEBUY']  # these are from original data or Johnny
needs_check = []
for f in yangmei:
    name = f.get('name', '')
    lat = f.get('lat')
    lng = f.get('lng')
    addr = f.get('address', '')
    
    # Skip ones Johnny provided
    if any(k in name for k in precise.keys()):
        continue
    # Skip ones without coords
    if not lat or not lng:
        continue
    # Skip original data ones (50嵐, CoCo, 麻古, COMEBUY from original)
    if name in ['50嵐 楊梅大成店', 'CoCo都可 楊梅大成店', '麻古茶坊 楊梅文化店', 'COMEBUY 楊梅大成店']:
        continue
    
    needs_check.append(f)

# Sort by address
needs_check.sort(key=lambda f: f.get('address',''))
for f in needs_check:
    print(f'  {f["name"]:30s} | ({f.get("lat"):.5f}, {f.get("lng"):.5f}) | {f.get("address","無地址")}')

print(f'\n總計：{len(no_coords)} 無座標 + {len(needs_check)} 座標待確認')
