import json, sys, io, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

# Fix wrong coordinates - these two got coords in 嘉義/台南
fixed = 0
for f in foods:
    if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or [])):
        lat = f.get('lat')
        lng = f.get('lng')
        if lat and lng:
            # Yangmei is around 24.9x, 121.1x
            if lat < 24.5 or lat > 25.1 or lng < 120.9 or lng > 121.3:
                print(f'Fixing: {f["name"]} ({lat},{lng}) -> removing wrong coords')
                f['lat'] = None
                f['lng'] = None
                fixed += 1

# Also fix addresses with leading newlines
for f in foods:
    if f.get('address'):
        f['address'] = f['address'].strip()

data['food'] = foods
with open('data/taoyuan.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\nFixed {fixed} wrong coordinates')

# Summary
user_lat, user_lng = 24.9133, 121.1858
yangmei = [f for f in foods if f.get('area')=='楊梅區' and any('飲品' in c for c in (f.get('categories') or []))]
has = [f for f in yangmei if f.get('lat') and f.get('lng')]
no = [f for f in yangmei if not f.get('lat') or not f.get('lng')]
print(f'有座標: {len(has)}, 無座標: {len(no)}')

print(f'\n=== 1km 內的店家 ===')
for f in has:
    d = math.sqrt((float(f['lat'])-user_lat)**2 + (float(f['lng'])-user_lng)**2) * 111
    if d <= 1.0:
        print(f'  {f["name"]:30s} | {f.get("rating",0):.1f}★ | {d:.2f}km')

print(f'\n=== 1-5km ===')
for f in has:
    d = math.sqrt((float(f['lat'])-user_lat)**2 + (float(f['lng'])-user_lng)**2) * 111
    if 1.0 < d <= 5.0:
        print(f'  {f["name"]:30s} | {f.get("rating",0):.1f}★ | {d:.2f}km')

print(f'\n=== 5km+ ===')
for f in has:
    d = math.sqrt((float(f['lat'])-user_lat)**2 + (float(f['lng'])-user_lng)**2) * 111
    if d > 5.0:
        print(f'  {f["name"]:30s} | {f.get("rating",0):.1f}★ | {d:.2f}km')
