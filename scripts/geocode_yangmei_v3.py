"""
Geocode via Playwright + Google Maps search using domcontentloaded + long sleep
"""
from playwright.sync_api import sync_playwright
import json, time, sys, io, re, os, math, urllib.parse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

def haversine(lat1,lng1,lat2,lng2):
    R=6371
    dLat=math.radians(lat2-lat1)
    dLng=math.radians(lng2-lng1)
    a=math.sin(dLat/2)**2+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dLng/2)**2
    return R*2*math.asin(math.sqrt(a))

need = []
for f in foods:
    if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or [])):
        if not f.get('lat') or not f.get('lng'):
            need.append(f)

print(f'Need coords for {len(need)} shops\n')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    found = 0
    for i, shop in enumerate(need):
        name = shop['name']
        q = f'{name} 楊梅區 桃園'
        print(f'[{i+1}/{len(need)}] {name}...', end=' ', flush=True)
        
        try:
            # Use google search instead of maps
            search_url = f'https://www.google.com/search?q={urllib.parse.quote(q + " google maps")}'
            page.goto(search_url, wait_until='domcontentloaded', timeout=15000)
            time.sleep(2)
            
            # Try to find a maps link in search results
            content = page.content()
            
            # Look for coordinates in the page
            # Google search results for businesses often have coords in data
            lat, lng = None, None
            
            # Pattern: data-url containing maps link with @lat,lng
            maps_links = re.findall(r'https://www\.google\.com/maps/place/[^"]+@(-?\d+\.\d+),(-?\d+\.\d+)', content)
            if maps_links:
                lat, lng = float(maps_links[0][0]), float(maps_links[0][1])
            
            if not lat:
                # Try finding in any link with @coords
                m = re.search(r'@(-?\d{2,3}\.\d{4,}),(-?\d{2,3}\.\d{4,})', content)
                if m:
                    lat, lng = float(m.group(1)), float(m.group(2))
            
            if not lat:
                # Try clicking the maps link
                try:
                    maps_link = page.query_selector('a[href*="maps/place"]') or page.query_selector('a[href*="maps.google"]')
                    if maps_link:
                        maps_link.click()
                        time.sleep(3)
                        current_url = page.url
                        m = re.search(r'@(-?\d{2,3}\.\d{4,}),(-?\d{2,3}\.\d{4,})', current_url)
                        if m:
                            lat, lng = float(m.group(1)), float(m.group(2))
                        if not lat:
                            m = re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', current_url)
                            if m:
                                lat, lng = float(m.group(1)), float(m.group(2))
                except:
                    pass
            
            if not lat:
                # Try direct maps search
                maps_url = f'https://www.google.com/maps/search/{urllib.parse.quote(q)}'
                page.goto(maps_url, wait_until='domcontentloaded', timeout=15000)
                time.sleep(4)
                current_url = page.url
                m = re.search(r'@(-?\d{2,3}\.\d{4,}),(-?\d{2,3}\.\d{4,})', current_url)
                if m:
                    lat, lng = float(m.group(1)), float(m.group(2))
                if not lat:
                    m = re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', current_url)
                    if m:
                        lat, lng = float(m.group(1)), float(m.group(2))
            
            if lat and lng and 20 < lat < 26 and 119 < lng < 123:
                shop['lat'] = lat
                shop['lng'] = lng
                print(f'✅ ({lat:.4f}, {lng:.4f})')
                found += 1
            else:
                print(f'❌')
        except Exception as e:
            print(f'❌ {str(e)[:50]}')
        
        time.sleep(1)
    
    browser.close()

# Save
data['food'] = foods
with open('data/taoyuan.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\nFound: {found}/{len(need)}')

# Show distances
user_lat, user_lng = 24.9133, 121.1858
print(f'\n=== Distance from Johnny ===')
yangmei = [f for f in foods if f.get('area')=='楊梅區' and any('飲品' in c for c in (f.get('categories') or [])) and f.get('lat') and f.get('lng')]
yangmei.sort(key=lambda f: haversine(user_lat,user_lng,f['lat'],f['lng']))
for f in yangmei:
    d = haversine(user_lat,user_lng,f['lat'],f['lng'])
    print(f'  {f["name"]:30s} | {f.get("rating",0):.1f}★ | {d:.2f}km')
