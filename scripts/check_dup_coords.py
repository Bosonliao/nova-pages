import json, sys, io, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

user_lat, user_lng = 24.9133, 121.1858

def haversine(lat1,lng1,lat2,lng2):
    R=6371
    dLat=math.radians(lat2-lat1)
    dLng=math.radians(lng2-lng1)
    a=math.sin(dLat/2)**2+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dLng/2)**2
    return R*2*math.asin(math.sqrt(a))

print('=== 楊梅飲料店座標重複檢查 ===')
# Group by coordinates
coord_groups = {}
for f in foods:
    if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or [])):
        lat = f.get('lat')
        lng = f.get('lng')
        if lat and lng:
            key = f'{lat:.4f},{lng:.4f}'
            if key not in coord_groups:
                coord_groups[key] = []
            coord_groups[key].append(f)

print('重複座標的組：')
for key, shops in coord_groups.items():
    if len(shops) > 1:
        d = haversine(user_lat, user_lng, shops[0]['lat'], shops[0]['lng'])
        print(f'\n  座標 {key} (距離 {d:.2f}km) — {len(shops)} 家：')
        for s in shops:
            print(f'    {s["name"]:30s} | {s.get("rating",0):.1f}★ | addr={s.get("address","無")}')

print('\n\n=== 全部有座標的（按距離排序）===')
has = [f for f in foods if f.get('area')=='楊梅區' and any('飲品' in c for c in (f.get('categories') or [])) and f.get('lat') and f.get('lng')]
has.sort(key=lambda f: haversine(user_lat,user_lng,f['lat'],f['lng']))
for f in has:
    d = haversine(user_lat,user_lng,f['lat'],f['lng'])
    print(f'  {f["name"]:30s} | {f.get("rating",0):.1f}★ | {d:.2f}km | ({f["lat"]:.4f},{f["lng"]:.4f}) | {f.get("address","")}')
