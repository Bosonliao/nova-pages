"""
Geocode Yangmei drink shops via Nominatim with cleaned addresses
Remove 里 names which Nominatim can't handle
"""
import json, sys, io, time, urllib.parse, urllib.request, ssl, math, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
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

def nominatim(q):
    url = f'https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(q)}&format=json&limit=1&countrycodes=tw'
    req = urllib.request.Request(url, headers={'User-Agent': 'NovaFoodRadar/1.0'})
    try:
        resp = urllib.request.urlopen(req, timeout=10, context=ctx)
        results = json.loads(resp.read().decode('utf-8'))
        if results:
            return float(results[0]['lat']), float(results[0]['lon'])
    except:
        pass
    return None, None

def clean_address(addr):
    """Remove 里 names and clean up address for Nominatim"""
    if not addr:
        return None
    # Remove 326, 桃園市楊梅區
    a = addr.replace('326', '').replace('桃園市', '').replace('楊梅區', '').strip()
    # Remove 里 names: pattern like 楊梅里, 埔心里, 中山里, etc
    a = re.sub(r'[\u4e00-\u9fff]+里', '', a)
    # Remove 號 suffix for better matching
    # Keep the road name + number
    a = a.strip()
    return a

need = []
for f in foods:
    if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or [])):
        if not f.get('lat') or not f.get('lng'):
            need.append(f)

print(f'Need coords for {len(need)} shops\n')

found = 0
for i, shop in enumerate(need):
    name = shop['name']
    addr = shop.get('address', '')
    cleaned = clean_address(addr)
    
    print(f'[{i+1}/{len(need)}] {name}...', end=' ', flush=True)
    
    lat, lng = None, None
    
    # Try 1: cleaned address + 楊梅
    if cleaned:
        q = f'{cleaned} 楊梅 台灣'
        lat, lng = nominatim(q)
        if lat:
            print(f'✅ ({lat:.4f}, {lng:.4f}) [addr]')
    
    # Try 2: just road name + number
    if not lat and cleaned:
        road_match = re.match(r'([\u4e00-\u9fff]+[路街][\d-]*號?)', cleaned)
        if road_match:
            q = f'{road_match.group(1)} 楊梅 台灣'
            lat, lng = nominatim(q)
            if lat:
                print(f'✅ ({lat:.4f}, {lng:.4f}) [road]')
    
    # Try 3: road name without number
    if not lat and cleaned:
        road_match = re.match(r'([\u4e00-\u9fff]+[路街])', cleaned)
        if road_match:
            q = f'{road_match.group(1)} 楊梅 台灣'
            lat, lng = nominatim(q)
            if lat:
                print(f'✅ ({lat:.4f}, {lng:.4f}) [road-only]')
    
    # Try 4: shop name + 楊梅
    if not lat:
        # Extract brand keywords from name
        q = f'{name} 楊梅 台灣'
        lat, lng = nominatim(q)
        if lat:
            print(f'✅ ({lat:.4f}, {lng:.4f}) [name]')
    
    # Try 5: for 埔心 area, try with 埔心
    if not lat and ('埔心' in name or (cleaned and '埔心' in cleaned)):
        q = f'埔心 楊梅 台灣'
        lat, lng = nominatim(q)
        if lat:
            print(f'✅ ({lat:.4f}, {lng:.4f}) [puxin]')
    
    if lat and lng and 20 < lat < 26 and 119 < lng < 123:
        shop['lat'] = lat
        shop['lng'] = lng
        found += 1
    else:
        print(f'❌ (addr={cleaned or "none"})')
    
    time.sleep(1.1)

# Save
data['food'] = foods
with open('data/taoyuan.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\nFound: {found}/{len(need)}')

# Show distances
user_lat, user_lng = 24.9133, 121.1858
print(f'\n=== Distance from Johnny ({user_lat}, {user_lng}) ===')
yangmei = [f for f in foods if f.get('area')=='楊梅區' and any('飲品' in c for c in (f.get('categories') or [])) and f.get('lat') and f.get('lng')]
yangmei.sort(key=lambda f: haversine(user_lat,user_lng,f['lat'],f['lng']))
for f in yangmei:
    d = haversine(user_lat,user_lng,f['lat'],f['lng'])
    print(f'  {f["name"]:30s} | {f.get("rating",0):.1f}★ | {d:.2f}km')
