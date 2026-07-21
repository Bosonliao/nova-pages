"""
Geocode Yangmei drink shop addresses using Nominatim (free)
"""
import json, sys, io, time, urllib.parse, urllib.request, ssl, math

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATA_DIR = 'data'
data = json.load(open(f'{DATA_DIR}/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def haversine(lat1,lng1,lat2,lng2):
    R=6371
    dLat=math.radians(lat2-lat1)
    dLng=math.radians(lng2-lng1)
    a=math.sin(dLat/2)**2+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dLng/2)**2
    return R*2*math.asin(math.sqrt(a))

def nominatim_geocode(address):
    """Geocode using Nominatim"""
    url = f'https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(address)}&format=json&limit=1&countrycodes=tw'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'NovaFoodRadar/1.0 (nova.ai0525@gmail.com)'
    })
    try:
        resp = urllib.request.urlopen(req, timeout=10, context=ctx)
        results = json.loads(resp.read().decode('utf-8'))
        if results:
            return float(results[0]['lat']), float(results[0]['lon'])
    except:
        pass
    return None, None

# Get shops needing coordinates
need_coords = []
for f in foods:
    if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or [])):
        if not f.get('lat') or not f.get('lng'):
            need_coords.append(f)

print(f'Need coordinates for {len(need_coords)} shops\n')

found = 0
for i, shop in enumerate(need_coords):
    name = shop['name']
    addr = shop.get('address', '')
    
    # Clean address - remove leading 326 etc
    if addr:
        clean_addr = addr.replace('326', '').strip()
        # If address doesn't start with 桃園, add it
        if '桃園' not in clean_addr:
            clean_addr = '桃園市' + clean_addr
    else:
        # Use name + area as fallback
        clean_addr = f'{name} 楊梅區 桃園市'
    
    print(f'[{i+1}/{len(need_coords)}] {name}...', end=' ', flush=True)
    
    lat, lng = nominatim_geocode(clean_addr)
    
    if lat and lng:
        shop['lat'] = lat
        shop['lng'] = lng
        print(f'✅ ({lat:.4f}, {lng:.4f})')
        found += 1
    else:
        # Try with just the road name
        if addr:
            # Extract road + number
            import re
            road_match = re.search(r'([\u4e00-\u9fff]+路|[\u4e00-\u9fff]+街|[\u4e00-\u9fff]+村)[\d-]*號?', clean_addr)
            if road_match:
                road = road_match.group(0)
                lat, lng = nominatim_geocode(f'{road} 楊梅區 桃園市')
                if lat and lng:
                    shop['lat'] = lat
                    shop['lng'] = lng
                    print(f'✅ ({lat:.4f}, {lng:.4f}) [road fallback]')
                    found += 1
                    time.sleep(1)
                    continue
        print(f'❌ ({clean_addr[:30]})')
    
    time.sleep(1)  # Nominatim rate limit

# Save
data['food'] = foods
with open(f'{DATA_DIR}/taoyuan.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\nFound: {found}/{len(need_coords)}')

# Show distance from Johnny
user_lat, user_lng = 24.9133, 121.1858
print(f'\n=== Distance from Johnny ({user_lat}, {user_lng}) ===')
yangmei = [f for f in foods if f.get('area')=='楊梅區' and any('飲品' in c for c in (f.get('categories') or [])) and f.get('lat') and f.get('lng')]
yangmei.sort(key=lambda f: haversine(user_lat,user_lng,f['lat'],f['lng']))
for f in yangmei[:20]:
    d = haversine(user_lat,user_lng,f['lat'],f['lng'])
    print(f'  {f["name"]:30s} | {f.get("rating",0):.1f}★ | {d:.2f}km')
