import urllib.request, urllib.parse, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
name = '阜杭豆漿'

# Test 1: ifoodie.tw
print('=== ifoodie.tw ===')
url = f'https://ifoodie.tw/search?q={urllib.parse.quote(name)}'
req = urllib.request.Request(url, headers=headers)
try:
    r = urllib.request.urlopen(req, timeout=10)
    html = r.read().decode('utf-8')
    print(f'  {len(html)} bytes, status {r.status}')
    if name in html:
        print('  Found restaurant name in HTML')
    for kw in ['推薦', '必吃', 'menu', '菜單']:
        if kw in html:
            print(f'  Found keyword: {kw}')
except Exception as e:
    print(f'  FAIL - {e}')

# Test 2: web_fetch via OpenClaw
print()
print('=== web_fetch test (ifoodie) ===')

# Test 3: Google search via urllib (not Places API)
print()
print('=== Google Search (free, no API) ===')
google_url = f'https://www.google.com/search?q={urllib.parse.quote(name + " 台北 推薦菜 必吃")}&hl=zh-TW'
req3 = urllib.request.Request(google_url, headers=headers)
try:
    r3 = urllib.request.urlopen(req3, timeout=10)
    html3 = r3.read().decode('utf-8')
    print(f'  {len(html3)} bytes, status {r3.status}')
    # Check for dish-related snippets
    for kw in ['招牌', '推薦', '必吃', '菜']:
        if kw in html3:
            print(f'  Found keyword: {kw}')
except Exception as e:
    print(f'  FAIL - {e}')

# Test 4: DuckDuckGo HTML (no JS)
print()
print('=== DuckDuckGo HTML ===')
ddg_url = f'https://html.duckduckgo.com/html/?q={urllib.parse.quote(name + " 台北 推薦菜")}'
req4 = urllib.request.Request(ddg_url, headers=headers)
try:
    r4 = urllib.request.urlopen(req4, timeout=10)
    html4 = r4.read().decode('utf-8')
    print(f'  {len(html4)} bytes, status {r4.status}')
    if name in html4:
        print('  Found restaurant name')
    for kw in ['招牌', '推薦', '必吃']:
        if kw in html4:
            print(f'  Found keyword: {kw}')
except Exception as e:
    print(f'  FAIL - {e}')
