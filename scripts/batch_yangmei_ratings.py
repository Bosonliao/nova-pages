import json, sys, io, re, time, urllib.parse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

need_rating = []
for f in foods:
    if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or [])):
        if not f.get('rating') or f.get('rating') == 0:
            need_rating.append(f)

print(f'Need ratings for {len(need_rating)} shops\n')

# Use DuckDuckGo HTML search (less likely to be blocked than Google)
import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

for i, shop in enumerate(need_rating):
    name = shop['name']
    addr = shop.get('address', '')
    q = f'{name} 楊梅 Google Maps 評分'
    url = f'https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}'
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        html = resp.read().decode('utf-8', errors='ignore')
        
        rating = None
        reviews = None
        
        # DuckDuckGo snippet often contains "4.3 (258)" pattern
        snippets = re.findall(r'result__snippet[^>]*>(.*?)</a>', html, re.DOTALL)
        for sn in snippets:
            # Look for rating patterns
            m = re.search(r'(\d\.\d)\s*(?:★|星|stars)', sn)
            if m:
                rating = float(m.group(1))
            m2 = re.search(r'\((\d+)\s*(?:則)?\s*(?:評論|評等|reviews)\)', sn)
            if m2:
                reviews = int(m2.group(1))
        
        # Also try finding in raw HTML
        if not rating:
            m = re.search(r'(\d\.\d)\s*(?:★|顆星|星)', html)
            if m:
                rating = float(m.group(1))
        if not reviews:
            m2 = re.search(r'(\d+)\s*(?:則評論|則評等|reviews)', html)
            if m2:
                reviews = int(m2.group(1))
        
        if rating and rating > 0:
            shop['rating'] = rating
            if reviews:
                shop['reviews'] = reviews
            print(f'[{i+1}/{len(need_rating)}] ✅ {name}: {rating}★ ({reviews or "?"})')
        else:
            print(f'[{i+1}/{len(need_rating)}] ❌ {name}: not found')
    except Exception as e:
        print(f'[{i+1}/{len(need_rating)}] ❌ {name}: error {str(e)[:60]}')
    
    time.sleep(3)

# Save
data['food'] = foods
with open('data/taoyuan.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

found = sum(1 for f in need_rating if f.get('rating', 0) > 0)
print(f'\nFound: {found}/{len(need_rating)}')
