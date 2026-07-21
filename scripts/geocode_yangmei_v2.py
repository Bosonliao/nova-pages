"""
Better Playwright script: search Google Maps, click first result, extract coords from URL
"""
from playwright.sync_api import sync_playwright
import json, time, sys, io, re, os, math

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
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    page = context.new_page()
    
    found = 0
    for i, shop in enumerate(need):
        name = shop['name']
        addr = shop.get('address', '')
        # Build search query
        q = f'{name} 楊梅區'
        if addr:
            # Extract just the road part
            q = f'{name} {addr.replace("桃園市","").replace("326","").strip()[:20]}'
        
        print(f'[{i+1}/{len(need)}] {name}...', end=' ', flush=True)
        
        try:
            # Search Google Maps
            url = f'https://www.google.com/maps/search/{q}'
            page.goto(url, wait_until='networkidle', timeout=20000)
            time.sleep(2)
            
            # Try clicking first result
            try:
                first = page.query_selector('a[role="article"]') or page.query_selector('div[role="article"]')
                if first:
                    first.click()
                    time.sleep(3)
            except:
                pass
            
            # Get current URL - should contain coords after clicking
            current_url = page.url
            
            # Try multiple patterns
            lat, lng = None, None
            
            # Pattern 1: @lat,lng in URL
            m = re.search(r'@(-?\d{1,3}\.\d+),(-?\d{1,3}\.\d+)', current_url)
            if m:
                lat, lng = float(m.group(1)), float(m.group(2))
            
            # Pattern 2: !3dlat!4dlng
            if not lat:
                m = re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', current_url)
                if m:
                    lat, lng = float(m.group(1)), float(m.group(2))
            
            # Pattern 3: Look in page content for coordinates
            if not lat:
                # Try to find a Place ID and use that
                text = page.content()
                # Look for coordinate-like patterns in data attributes
                m = re.search(r'"(-?\d{2,3}\.\d{4,})"\s*,\s*"(-?\d{2,3}\.\d{4,})"', text)
                if m:
                    lat, lng = float(m.group(1)), float(m.group(2))
            
            # Pattern 4: Try JavaScript evaluation
            if not lat:
                try:
                    coords = page.evaluate('''() => {
                        const url = window.location.href;
                        const m1 = url.match(/@(-?\\d+\\.\\d+),(-?\\d+\\.\\d+)/);
                        if (m1) return [parseFloat(m1[1]), parseFloat(m1[2])];
                        const m2 = url.match(/!3d(-?\\d+\\.\\d+)!4d(-?\\d+\\.\\d+)/);
                        if (m2) return [parseFloat(m2[1]), parseFloat(m2[2])];
                        return null;
                    }''')
                    if coords:
                        lat, lng = coords[0], coords[1]
                except:
                    pass
            
            if lat and lng and 20 < lat < 26 and 119 < lng < 123:
                shop['lat'] = lat
                shop['lng'] = lng
                
                # Also try to get rating/reviews while we're here
                try:
                    text = page.inner_text('body')
                    if not shop.get('rating') or shop.get('rating') == 0:
                        m_r = re.search(r'(\d\.\d)\s*(?:顆星|星|stars)', text)
                        if m_r:
                            shop['rating'] = float(m_r.group(1))
                except:
                    pass
                
                print(f'✅ ({lat:.4f}, {lng:.4f})')
                found += 1
            else:
                print(f'❌ url={current_url[:80]}')
        except Exception as e:
            print(f'❌ error: {str(e)[:60]}')
        
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
