import json, sys, io, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

# Find all 麻古 entries
print('=== 所有麻古茶坊 entries ===')
for f in foods:
    if '麻古' in f.get('name', ''):
        print(f'  {f["name"]:30s} | area={f.get("area")} | {f.get("rating",0):.1f}★ | lat={f.get("lat")} lng={f.get("lng")} | addr={f.get("address","")}')

# Johnny's location from Google Maps
# He said he's near 文化街167號, 麻古茶坊 楊梅文化店
user_lat = 24.9133
user_lng = 121.1858

print(f'\n=== 距離 Johnny ({user_lat}, {user_lng}) ===')
def haversine(lat1,lng1,lat2,lng2):
    R=6371
    dLat=math.radians(lat2-lat1)
    dLng=math.radians(lng2-lng1)
    a=math.sin(dLat/2)**2+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dLng/2)**2
    return R*2*math.asin(math.sqrt(a))

for f in foods:
    if '麻古' in f.get('name', '') and f.get('lat'):
        d = haversine(user_lat, user_lng, f['lat'], f['lng'])
        print(f'  {f["name"]:30s} | {d:.3f}km | ({f["lat"]}, {f["lng"]})')

# Also check: what brands are in the 1km range?
print(f'\n=== 1km 內所有品牌（去重前）===')
yangmei_drinks = [f for f in foods if f.get('area')=='楊梅區' and any('飲品' in c for c in (f.get('categories') or [])) and f.get('lat') and f.get('lng')]
near = []
for f in yangmei_drinks:
    d = haversine(user_lat, user_lng, f['lat'], f['lng'])
    if d <= 1.0:
        near.append((f, d))
near.sort(key=lambda x: x[1])
for f, d in near:
    brand = f['name'].split(' ')[0].split('-')[0].split('（')[0].split('(')[0].strip()
    print(f'  {f["name"]:30s} | brand={brand} | {d:.3f}km')
