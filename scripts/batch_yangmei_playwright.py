"""
Batch scrape ratings for Yangmei drink shops using Playwright + Google Maps
"""
from playwright.sync_api import sync_playwright
import json, time, sys, io, re, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# Load data
data = json.load(open(os.path.join(DATA_DIR, 'taoyuan.json'), 'r', encoding='utf-8'))
foods = data.get('food', [])

# Get shops needing ratings
need_rating = []
for f in foods:
    if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or [])):
        if not f.get('rating') or f.get('rating') == 0:
            need_rating.append(f)

print(f'Need ratings for {len(need_rating)} shops\n')

def scrape_rating(page, shop_name, area='楊梅區'):
    """Search Google Maps and extract rating from first result"""
    query = f'{shop_name} {area}'
    url = f'https://www.google.com/maps/search/{query}'
    
    try:
        page.goto(url, wait_until='domcontentloaded', timeout=20000)
        time.sleep(3)
        
        # Try to get rating from the page
        # Google Maps shows rating like "4.3" with star icon
        rating_el = page.query_selector('span[role="img"][aria-label*="星"]') or \
                    page.query_selector('span[role="img"][aria-label*="star"]') or \
                    page.query_selector('div.F7nice span')  # Alternative selector
        
        rating = None
        reviews = None
        
        if rating_el:
            aria = rating_el.get_attribute('aria-label') or ''
            m = re.search(r'(\d\.?\d?)', aria)
            if m:
                rating = float(m.group(1))
        
        # Try alternative: look for rating in text
        if not rating:
            text = page.inner_text('body')
            # Pattern: "4.3 顆星" or "4.3 stars" or "評分 4.3"
            m = re.search(r'(\d\.\d)\s*(?:顆星|星|stars)', text)
            if m:
                rating = float(m.group(1))
        
        # Get reviews count
        if rating:
            text = page.inner_text('body')
            m2 = re.search(r'(\d+)\s*(?:則評論|則評等|reviews)', text)
            if m2:
                reviews = int(m2.group(1))
        
        # Get coordinates from URL
        current_url = page.url
        coord_match = re.search(r'@(-?[\d.]+),(-?[\d.]+)', current_url)
        lat = float(coord_match.group(1)) if coord_match else None
        lng = float(coord_match.group(2)) if coord_match else None
        
        # Get address
        address = None
        addr_el = page.query_selector('button[data-item-id="address"]')
        if addr_el:
            address = addr_el.inner_text().strip()
        
        return rating, reviews, lat, lng, address
    except Exception as e:
        print(f'    Error: {str(e)[:80]}')
        return None, None, None, None, None

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    found = 0
    for i, shop in enumerate(need_rating):
        name = shop['name']
        print(f'[{i+1}/{len(need_rating)}] {name}...', end=' ', flush=True)
        
        rating, reviews, lat, lng, address = scrape_rating(page, name)
        
        if rating and rating > 0:
            shop['rating'] = rating
            if reviews:
                shop['reviews'] = reviews
            if lat and not shop.get('lat'):
                shop['lat'] = lat
            if lng and not shop.get('lng'):
                shop['lng'] = lng
            if address and not shop.get('address'):
                shop['address'] = address
            print(f'✅ {rating}★ ({reviews or "?"})')
            found += 1
        else:
            print('❌')
        
        time.sleep(2)
    
    browser.close()

# Save
data['food'] = foods
with open(os.path.join(DATA_DIR, 'taoyuan.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\nFound: {found}/{len(need_rating)}')
