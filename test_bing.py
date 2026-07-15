import urllib.request, urllib.parse, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

# Test Bing
query = '千巧谷牛樂園牧場 雲林 推薦菜 必吃'
url = f'https://www.bing.com/search?q={urllib.parse.quote(query)}&setlang=zh-TW'
req = urllib.request.Request(url, headers=headers)
r = urllib.request.urlopen(req, timeout=10)
html = r.read().decode('utf-8')
print(f'Bing: {len(html)} bytes, status {r.status}')

# Extract search result snippets - Bing uses <li class="b_algo">
results = re.findall(r'<li class="b_algo">(.*?)</li>', html, re.DOTALL)
print(f'Found {len(results)} results')
for i, snippet in enumerate(results[:5]):
    clean = re.sub(r'<[^>]+>', ' ', snippet).strip()
    clean = re.sub(r'\s+', ' ', clean)
    print(f'{i+1}. {clean[:300]}')
    print()

# Also test: can we fetch a food blog page?
print('=== Testing food blog fetch ===')
# Try fetching a blog post about the restaurant
blog_url = f'https://www.bing.com/search?q={urllib.parse.quote(query + " 食記")}'
req2 = urllib.request.Request(blog_url, headers=headers)
r2 = urllib.request.urlopen(req2, timeout=10)
html2 = r2.read().decode('utf-8')
results2 = re.findall(r'<li class="b_algo">(.*?)</li>', html2, re.DOTALL)
print(f'Blog search: {len(results2)} results')
for i, snippet in enumerate(results2[:3]):
    clean = re.sub(r'<[^>]+>', ' ', snippet).strip()
    clean = re.sub(r'\s+', ' ', clean)
    # Find links
    links = re.findall(r'href="(https?://[^"]+)"', snippet)
    print(f'{i+1}. {clean[:200]}')
    if links:
        print(f'   Links: {links[0]}')
    print()
