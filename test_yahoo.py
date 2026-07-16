import urllib.request, urllib.parse, re, html, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

query = urllib.parse.quote('阿三肉圓 彰化 推薦菜')
url = f'https://search.yahoo.com/search?p={query}'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'zh-TW,zh;q=0.9'
})
resp = urllib.request.urlopen(req, timeout=15)
content = resp.read().decode('utf-8', errors='replace')

# Find all links and nearby text
links = re.findall(r'<a[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', content)
for link, title in links[:20]:
    title_clean = html.unescape(re.sub(r'<[^>]+>', '', title))
    if title_clean.strip() and 'yahoo' not in link.lower():
        print(f'  {title_clean.strip()} -> {link}')

# Also extract text snippets
print("\n--- Text snippets ---")
text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = html.unescape(text)
# Find lines mentioning 肉圓 or 推薦
for line in text.split('.'):
    line = line.strip()
    if len(line) > 20 and ('肉圓' in line or '推薦' in line or '必點' in line):
        print(f'  {line[:200]}')