"""
Extract coordinates from Google Maps using Playwright
Strategy: search, click result, extract coords from URL
"""
from playwright.sync_api import sync_playwright
import json, time, sys, io, re, math, urllib.parse

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
        addr = shop.get('address', '')
        
        # Build search query - just shop name + 楊梅
        q = f'{name} 楊梅'
        print(f'[{i+1}/{len(need)}] {name}...', end=' ', flush=True)
        
        try:
            # Go to Google Maps search
            page.goto(f'https://www.google.com/maps/search/{urllib.parse.quote(q)}',
                      wait_until='domcontentloaded', timeout=15000)
            time.sleep(4)
            
            # Try to extract coords from URL
            current_url = page.url
            lat, lng = None, None
            
            # Pattern: @lat,lng
            m = re.search(r'@(-?\d{1,3}\.\d+),(-?\d{1,3}\.\d+)', current_url)
            if m:
                lat, lng = float(m.group(1)), float(m.group(2))
            
            # Pattern: !3dlat!4dlng (place coords)
            if not lat:
                m = re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', current_url)
                if m:
                    lat, lng = float(m.group(1)), float(m.group(2))
            
            # Try: evaluate JS to find coords in page
            if not lat:
                try:
                    result = page.evaluate('''() => {
                        // Try to find coords in the page's script data
                        const scripts = document.querySelectorAll('script');
                        for (const s of scripts) {
                            const text = s.textContent || '';
                            // Look for coordinates in JSON-like data
                            const m = text.match(/"(-?\\d{2,3}\\.\\d{5,})"\\s*,\\s*"(-?\\d{2,3}\\.\\d{5,})"/);
                            if (m) return [parseFloat(m[1]), parseFloat(m[2])];
                        }
                        // Also check meta tags
                        const meta = document.querySelector('meta[property="og:image"]');
                        if (meta) {
                            const url = meta.content || '';
                            const m = url.match(/center=(-?\\d+\\.\\d+),(-?\\d+\\.\\d+)/);
                            if (m) return [parseFloat(m[1]), parseFloat(m[2])];
                        }
                        // Check for APP_INITIALIZATION_STATE
                        for (const s of scripts) {
                            const text = s.textContent || '';
                            if (text.includes('APP_INITIALIZATION_STATE')) {
                                // Find lat/lng in the initialization data
                                const m = text.match(/\\[(-?\\d{2,3}\\.\\d+),(-?\\d{2,3}\\.\\d+)\\]/);
                                if (m) return [parseFloat(m[1]), parseFloat(m[2])];
                            }
                        }
                        return null;
                    }''')
                    if result and len(result) == 2:
                        lat, lng = result[0], result[1]
                except:
                    pass
            
            # Try: look for any link with coordinates
            if not lat:
                try:
                    links = page.query_selector_all('a[href]')
                    for link in links[:20]:
                        href = link.get_attribute('href') or ''
                        m = re.search(r'@(-?\d{2,3}\.\d+),(-?\d{2,3}\.\d+)', href)
                        if m:
                            lat, lng = float(m.group(1)), float(m.group(2))
                            break
                        m = re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', href)
                        if m:
                            lat, lng = float(m.group(1)), float(m.group(2))
                            break
                except:
                    pass
            
            if lat and lng and 24.5 < lat < 25.2 and 120.8 < lng < 121.4:
                shop['lat'] = lat
                shop['lng'] = lng
                d = haversine(24.9133, 121.1858, lat, lng)
                print(f'✅ ({lat:.5f}, {lng:.5f}) {d:.2f}km')
                found += 1
            else:
                print(f'❌')
        except Exception as e:
            print(f'❌ {str(e)[:40]}')
        
        time.sleep(1)
    
    browser.close()

# Save
data['food'] = foods
with open('data/taoyuan.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\nFound: {found}/{len(need)}')

# Show all
user_lat, user_lng = 24.9133, 121.1858
all_yangmei = [f for f in foods if f.get('area')=='楊梅區' and any('飲品' in c for c in (f.get('categories') or [])) and f.get('lat') and f.get('lng')]
all_yangmei.sort(key=lambda f: haversine(user_lat,user_lng,f['lat'],f['lng']))
print(f'\n=== All {len(all_yangmei)} shops with coords ===')
for f in all_yangmei:
    d = haversine(user_lat,user_lng,f['lat'],f['lng'])
    print(f'  {f["name"]:30s} | {f.get("rating",0):.1f}★ | {d:.2f}km')
