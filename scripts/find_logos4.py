import urllib.request, ssl, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

sites = {
    '八曜和茶': 'https://www.8yao.com/',
    '老虎堂': 'https://www.tigersugar.com/',
}

for brand, url in sites.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        html = urllib.request.urlopen(req, timeout=10, context=ctx).read().decode('utf-8', 'ignore')
        imgs = re.findall(r'<img[^>]*src=["\']([^"\'>]+)["\'][^>]*>', html)
        favs = re.findall(r'rel=["\'](?:icon|shortcut icon)["\'][^>]*href=["\']([^"\'>]+)["\']', html)
        print(f'=== {brand} ({url}) ===')
        for f in favs[:3]:
            print(f'  favicon: {f}')
        for i in imgs[:8]:
            print(f'  img: {i}')
        print()
    except Exception as e:
        print(f'{brand}: ERROR {e}\n')
