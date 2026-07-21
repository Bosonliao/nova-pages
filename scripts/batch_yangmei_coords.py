"""
Batch scrape coordinates and ratings for Yangmei drink shops using Playwright + Google Maps
"""
from playwright.sync_api import sync_playwright
import json, time, sys, io, re, os, math

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

data = json.load(open(os.path.join(DATA_DIR, 'taoyuan.json'), 'r', encoding='utf-8'))
foods = data.get('food', [])

# Get shops needing coordinates
need_coords = []
for f in foods:
    if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or [])):
        if not f.get('lat') or not f.get('lng'):
            need_coords.append(f)

print(f'Need coordinates for {len(need_coords)} shops\n')

def haversine(lat1,lng1,lat2,lng2):
    R=6371
    dLat=math.radians(lat2-lat1)
    dLng=math.radians(lng2-lng1)
    a=math.sin(dLat/2)**2+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dLng/2)**2
    return R*2*math.asin(math.sqrt(a))

def scrape_coords(page, shop_name, area='楊梅區', address=None):
    """Search Google Maps and extract coordinates + rating + reviews + address"""
    q = f'{shop_name} {area}' + (f' {address}' if address else '')
    url = f'https://www.google.com/maps/search/{q}'
    
    try:
        page.goto(url, wait_until='domcontentloaded', timeout=20000)
        time.sleep(3)
        
        current_url = page.url
        # Try multiple patterns for coordinates
        coord_match = re.search(r'@(-?[\d.]+),(-?[\d.]+)', current_url)
        if not coord_match:
            coord_match = re.search(r'!3d(-?[\d.]+)!4d(-?[\d.]+)', current_url)
        if not coord_match:
            # Try finding in page content
            text = page.inner_text('body')
            coord_match = re.search(r'(-?\d{2,3}\.\d{4,})[,\s]+(-?\d{2,3}\.\d{4,})', text)
        
        lat = float(coord_match.group(1)) if coord_match else None
        lng = float(coord_match.group(2)) if coord_match else None
        
        # Also try to get rating and reviews
        rating = None
        reviews = None
        
        rating_el = page.query_selector('span[role="img"][aria-label*="星"]') or \
                    page.query_selector('span[role="img"][aria-label*="star"]') or \
                    page.query_selector('div.F7nice span')
        if rating_el:
            text = rating_el.inner_text() or rating_el.get_attribute('aria-label') or ''
            m = re.search(r'(\d\.?\d?)', text)
            if m:
                rating = float(m.group(1))
        
        if not rating:
            text = page.inner_text('body')
            m = re.search(r'(\d\.\d)\s*(?:顆星|星|stars)', text)
            if m:
                rating = float(m.group(1))
            m2 = re.search(r'(\d+)\s*(?:則評論|則評等|reviews)', text)
            if m2:
                reviews = int(m2.group(1))
        
        # Get address
        address = None
        addr_el = page.query_selector('button[data-item-id="address"]')
        if addr_el:
            address = addr_el.inner_text().strip()
        
        return lat, lng, rating, reviews, address
    except Exception as e:
        print(f'    Error: {str(e)[:80]}')
        return None, None, None, None, None

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    found = 0
    for i, shop in enumerate(need_coords):
        name = shop['name']
        addr = shop.get('address', '')
        print(f'[{i+1}/{len(need_coords)}] {name}...', end=' ', flush=True)
        
        lat, lng, rating, reviews, address = scrape_coords(page, name, '楊梅區', addr)
        
        if lat and lng:
            shop['lat'] = lat
            shop['lng'] = lng
            if rating and rating > 0 and (not shop.get('rating') or shop.get('rating') == 0):
                shop['rating'] = rating
            if reviews:
                shop['reviews'] = reviews
            if address and not shop.get('address'):
                shop['address'] = address
            print(f'✅ ({lat:.4f}, {lng:.4f}) {rating or ""}★')
            found += 1
        else:
            print('❌')
        
        time.sleep(2)
    
    browser.close()

# Save
data['food'] = foods
with open(os.path.join(DATA_DIR, 'taoyuan.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\nFound coords: {found}/{len(need_coords)}')

# Show distance from Johnny's location
user_lat, user_lng = 24.9133, 121.1858
print(f'\n=== Distance from Johnny ({user_lat}, {user_lng}) ===')
yangmei_drinks = [f for f in foods if f.get('area')=='楊梅區' and any('飲品' in c for c in (f.get('categories') or [])) and f.get('lat') and f.get('lng')]
yangmei_drinks.sort(key=lambda f: haversine(user_lat,user_lng,f['lat'],f['lng']))
for f in yangmei_drinks[:15]:
    d = haversine(user_lat,user_lng,f['lat'],f['lng'])
    print(f'  {f["name"]:30s} | {f.get("rating",0):.1f}★ | {d:.2f}km')
