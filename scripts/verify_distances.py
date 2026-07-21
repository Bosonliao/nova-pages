import json, sys, io, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Haversine formula
def haversine(lat1, lng1, lat2, lng2):
    R = 6371
    dLat = math.radians(lat2-lat1)
    dLng = math.radians(lng2-lng1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dLng/2)**2
    return R * 2 * math.asin(math.sqrt(a))

# Your GPS from earlier screenshot: 24.9348, 121.1500
# Also try 楊梅大成路 area
user_lat = 24.91254
user_lng = 121.14591

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food',[])
drink = [f for f in foods if any('飲品' in c for c in f.get('categories',[])) and f.get('area')=='楊梅區' and f.get('lat') and f.get('lng')]

print(f'GPS: ({user_lat}, {user_lng}) - 楊梅大成路50嵐附近')
print(f'楊梅飲料店: {len(drink)} 家\n')

results = []
for f in drink:
    dist = haversine(user_lat, user_lng, f['lat'], f['lng'])
    results.append((f['name'], dist, f['lat'], f['lng'], f.get('address','')))

results.sort(key=lambda x: x[1])

for name, dist, lat, lng, addr in results[:20]:
    dm = dist * 1000
    if dm < 1000:
        print(f'  {name:30s} {dm:6.0f}m  ({lat}, {lng})  {addr}')
    else:
        print(f'  {name:30s} {dist:5.1f}km ({lat}, {lng})  {addr}')
