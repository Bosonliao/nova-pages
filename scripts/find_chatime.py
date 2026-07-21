import urllib.request, re, sys, io, ssl
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Check Chatime official website for logo
url = 'https://www.chatime.com.tw/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
html = urllib.request.urlopen(req, timeout=10, context=ctx).read().decode('utf-8', 'ignore')

# Find all images
imgs = re.findall(r'<img[^>]*src=["\']([^"\'>]+)["\'][^>]*>', html)
print('=== Chatime images ===')
for i in imgs[:15]:
    print(f'  {i}')

# Find favicon
favs = re.findall(r'rel=["\'](?:icon|shortcut icon)["\'][^>]*href=["\']([^"\'>]+)["\']', html)
for f in favs:
    print(f'  favicon: {f}')

# Find logo references
logos = re.findall(r'["\']([^"\']*logo[^"\']*\.[a-z]{3,4})["\']', html, re.I)
for l in logos:
    print(f'  logo-ref: {l}')
