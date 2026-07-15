import urllib.request, urllib.parse, json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Test with ifoodie restaurant page directly
print('=== ifoodie.tw restaurant page ===')
# First search for the restaurant
search_url = f'https://ifoodie.tw/search?q={urllib.parse.quote("阜杭豆漿")}'
req = urllib.request.Request(search_url, headers=headers)
r = urllib.request.urlopen(req, timeout=10)
html = r.read().decode('utf-8')

# Find restaurant page links
links = re.findall(r'href="(/place/[^"]+)"', html)
print(f'  Found {len(links)} restaurant links')
if links:
    for link in links[:3]:
        print(f'  Link: {link}')
    
    # Visit the first restaurant page
    rest_url = f'https://ifoodie.tw{links[0]}'
    req2 = urllib.request.Request(rest_url, headers=headers)
    r2 = urllib.request.urlopen(req2, timeout=10)
    rest_html = r2.read().decode('utf-8')
    print(f'  Restaurant page: {len(rest_html)} bytes')
    
    # Look for dish/menu content
    for kw in ['推薦', '必吃', '招牌', '菜單', 'menu']:
        if kw in rest_html:
            # Find surrounding text
            idx = rest_html.find(kw)
            context = rest_html[max(0,idx-50):idx+100]
            # Clean HTML tags
            clean = re.sub(r'<[^>]+>', ' ', context).strip()
            print(f'  [{kw}]: {clean[:100]}')

# Test DuckDuckGo for dish extraction
print()
print('=== DuckDuckGo dish search ===')
ddg_url = f'https://html.duckduckgo.com/html/?q={urllib.parse.quote("阜杭豆漿 台北 推薦菜 必吃")}'
req3 = urllib.request.Request(ddg_url, headers=headers)
r3 = urllib.request.urlopen(req3, timeout=10)
ddg_html = r3.read().decode('utf-8')

# Extract result snippets
results = re.findall(r'class="result__snippet">(.*?)</a>', ddg_html, re.DOTALL)
print(f'  Found {len(results)} result snippets')
for i, snippet in enumerate(results[:5]):
    clean = re.sub(r'<[^>]+>', ' ', snippet).strip()
    print(f'  {i+1}. {clean[:120]}')
