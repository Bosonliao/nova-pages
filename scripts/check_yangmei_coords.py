import json, sys, io, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

user_lat = 24.9133
user_lng = 121.1858

def haversine(lat1,lng1,lat2,lng2):
    R=6371
    dLat=math.radians(lat2-lat1)
    dLng=math.radians(lng2-lng1)
    a=math.sin(dLat/2)**2+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dLng/2)**2
    return R*2*math.asin(math.sqrt(a))

print('=== 楊梅區飲料店座標檢查 ===')
has_coords = 0
no_coords = 0
no_coord_list = []
with_dist = []
for f in foods:
    if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or [])):
        lat = f.get('lat')
        lng = f.get('lng')
        if lat and lng:
            has_coords += 1
            d = haversine(user_lat, user_lng, lat, lng)
            with_dist.append((f, d))
        else:
            no_coords += 1
            no_coord_list.append(f)

print(f'有座標: {has_coords}, 無座標: {no_coords}')
print(f'\n=== 有座標的（按距離排序）===')
with_dist.sort(key=lambda x: x[1])
for f, d in with_dist:
    print(f'  {f["name"]:30s} | {f.get("rating",0):.1f}★ | {d:.2f}km')

print(f'\n=== 無座標的 ===')
for f in no_coord_list:
    print(f'  {f["name"]:30s} | {f.get("rating",0):.1f}★ | {f.get("address","無地址")}')
