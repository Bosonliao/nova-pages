"""
Find Yangmei drink shop coordinates using Overpass API (OpenStreetMap)
Search for nodes by name in the Yangmei area
"""
import json, sys, io, urllib.parse, urllib.request, ssl, math, re, time

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

def overpass_search(name, area='24.85,121.05,25.0,121.25'):
    """Search OpenStreetMap for a shop by name in Yangmei area"""
    # Clean name for regex
    clean = name.split(' ')[0].split('-')[0].split('（')[0].split('(')[0].strip()
    
    query = f'''
    [out:json][timeout:10];
    (
      node["name"~"{clean}"]["amenity"~"cafe|fast_food|restaurant"]({area});
      node["name"~"{clean}"]["shop"~"beverages|tea|coffee"]({area});
      node["brand"~"{clean}"]({area});
    );
    out center;
    '''
    
    url = 'https://overpass-api.de/api/interpreter'
    data_bytes = urllib.parse.urlencode({'data': query}).encode('utf-8')
    req = urllib.request.Request(url, data=data_bytes, headers={
        'User-Agent': 'NovaFoodRadar/1.0'
    })
    
    try:
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        result = json.loads(resp.read().decode('utf-8'))
        return result.get('elements', [])
    except Exception as e:
        return []

# Get shops needing coordinates
need = []
for f in foods:
    if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or [])):
        if not f.get('lat') or not f.get('lng'):
            need.append(f)

print(f'Need coords for {len(need)} shops\n')

# Also search for shops that HAVE coords but might be inaccurate (road-only geocodes)
# We'll search all Yangmei drinks and match

# First, bulk search for all major brands at once
brands_to_search = set()
for shop in need:
    brand = shop['name'].split(' ')[0].split('-')[0].split('（')[0].split('(')[0].strip()
    brands_to_search.add(brand)

print(f'Unique brands to search: {len(brands_to_search)}')
print(f'Brands: {", ".join(sorted(brands_to_search))}\n')

# Search Overpass for each brand
all_osm_results = []
for brand in sorted(brands_to_search):
    elements = overpass_search(brand)
    if elements:
        print(f'  {brand}: {len(elements)} results')
        for el in elements:
            lat = el.get('lat') or el.get('center',{}).get('lat')
            lng = el.get('lon') or el.get('center',{}).get('lon')
            name = el.get('tags',{}).get('name','')
            if lat and lng:
                all_osm_results.append({
                    'brand': brand,
                    'name': name,
                    'lat': lat,
                    'lng': lng,
                    'tags': el.get('tags',{})
                })
    time.sleep(0.5)

print(f'\nTotal OSM results: {len(all_osm_results)}')

# Match OSM results to our shops
user_lat, user_lng = 24.9133, 121.1858
matched = 0
for shop in need:
    shop_name = shop['name']
    brand = shop_name.split(' ')[0].split('-')[0].split('（')[0].split('(')[0].strip()
    addr = shop.get('address', '')
    
    # Try to find matching OSM result
    best_match = None
    best_dist = 999
    
    for r in all_osm_results:
        if r['brand'] != brand:
            continue
        
        # Check if the OSM name contains branch info that matches
        osm_name = r['name']
        
        # Try to match by area/branch keywords in shop name
        shop_lower = shop_name.lower()
        osm_lower = osm_name.lower()
        
        # If shop name contains 楊梅 or 埔心, try to match
        branch_keywords = []
        if '楊梅' in shop_name:
            branch_keywords.append('楊梅')
        if '埔心' in shop_name:
            branch_keywords.append('埔心')
        if '富岡' in shop_name:
            branch_keywords.append('富岡')
        if '大成' in shop_name:
            branch_keywords.append('大成')
        if '文化' in shop_name:
            branch_keywords.append('文化')
        if '環南' in shop_name:
            branch_keywords.append('環南')
        if '環東' in shop_name:
            branch_keywords.append('環東')
        if '青山' in shop_name:
            branch_keywords.append('青山')
        if '中山' in shop_name:
            branch_keywords.append('中山')
        if '永美' in shop_name:
            branch_keywords.append('永美')
        if '四維' in shop_name:
            branch_keywords.append('四維')
        if '新農' in shop_name:
            branch_keywords.append('新農')
        if '金溪' in shop_name:
            branch_keywords.append('金溪')
        if '梅獅' in shop_name:
            branch_keywords.append('梅獅')
        
        score = 0
        for kw in branch_keywords:
            if kw in osm_name:
                score += 1
        
        # Check address match
        if addr:
            addr_clean = addr.replace('桃園市','').replace('楊梅區','').replace('326','').strip()
            # Extract road name
            road_match = re.search(r'([\u4e00-\u9fff]+[路街])', addr_clean)
            if road_match:
                road = road_match.group(1)
                if road in osm_name or road in str(r.get('tags',{}).get('addr:street','')):
                    score += 2
        
        if score > 0 and score > best_dist:
            best_dist = score
            best_match = r
    
    if best_match:
        shop['lat'] = best_match['lat']
        shop['lng'] = best_match['lng']
        d = haversine(user_lat, user_lng, best_match['lat'], best_match['lng'])
        print(f'✅ {shop_name:30s} -> ({best_match["lat"]:.4f}, {best_match["lng"]:.4f}) {d:.2f}km [{best_match["name"]}]')
        matched += 1
    else:
        # If no keyword match, use nearest OSM result for this brand
        brand_results = [r for r in all_osm_results if r['brand'] == brand]
        if brand_results:
            # Sort by distance from user
            brand_results.sort(key=lambda r: haversine(user_lat, user_lng, r['lat'], r['lng']))
            nearest = brand_results[0]
            d = haversine(user_lat, user_lng, nearest['lat'], nearest['lng'])
            if d < 15:  # Only accept if within 15km
                shop['lat'] = nearest['lat']
                shop['lng'] = nearest['lng']
                print(f'  {shop_name:30s} -> ({nearest["lat"]:.4f}, {nearest["lng"]:.4f}) {d:.2f}km [nearest {nearest["name"][:20]}]')
                matched += 1
            else:
                print(f'❌ {shop_name:30s} (nearest too far: {d:.2f}km)')
        else:
            print(f'❌ {shop_name:30s} (no OSM result)')

# Save
data['food'] = foods
with open('data/taoyuan.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\nMatched: {matched}/{len(need)}')

# Show all with coords
print(f'\n=== All Yangmei drinks with coords (sorted by distance) ===')
yangmei = [f for f in foods if f.get('area')=='楊梅區' and any('飲品' in c for c in (f.get('categories') or [])) and f.get('lat') and f.get('lng')]
yangmei.sort(key=lambda f: haversine(user_lat,user_lng,f['lat'],f['lng']))
for f in yangmei:
    d = haversine(user_lat,user_lng,f['lat'],f['lng'])
    print(f'  {f["name"]:30s} | {f.get("rating",0):.1f}★ | {d:.2f}km')
