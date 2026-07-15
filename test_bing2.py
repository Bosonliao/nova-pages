import urllib.request, urllib.parse, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

query = '千巧谷牛樂園牧場 雲林 推薦菜 必吃'
url = 'https://www.bing.com/search?q=' + urllib.parse.quote(query) + '&setlang=zh-TW'
req = urllib.request.Request(url, headers=headers)
r = urllib.request.urlopen(req, timeout=10)
html = r.read().decode('utf-8')

# Strip HTML tags and find text content
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text).strip()

# Find mentions of the restaurant and surrounding context
idx = text.find('千巧谷')
if idx >= 0:
    start = max(0, idx - 100)
    end = min(len(text), idx + 400)
    print('Context:')
    print(text[start:end])
else:
    print('Restaurant name not found in text')
    # Show first 500 chars of text
    print(text[:500])
