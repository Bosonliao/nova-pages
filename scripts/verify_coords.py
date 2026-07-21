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

# Verify the 8 shops Johnny provided
targets = ['UG', '自然湉', '茗茗究市', '茂昌', '花火禾茶', '功夫茶', '金茶伍', '吾奶王']
print('=== 驗證 Johnny 提供的 8 家座標 ===')
for f in foods:
    if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or [])):
        for t in targets:
            if t in f.get('name', ''):
                lat = f.get('lat')
                lng = f.get('lng')
                d = haversine(user_lat, user_lng, lat, lng) if lat and lng else 0
                print(f'  ✅ {f["name"]:30s} | ({lat}, {lng}) | {d:.2f}km | {f.get("address","")}')

# Count total with coords
total = sum(1 for f in foods if f.get('area')=='楊梅區' and any('飲品' in c for c in (f.get('categories') or [])) and f.get('lat') and f.get('lng'))
all_yangmei = sum(1 for f in foods if f.get('area')=='楊梅區' and any('飲品' in c for c in (f.get('categories') or [])))
print(f'\n楊梅區飲料店: {total}/{all_yangmei} 有座標')
