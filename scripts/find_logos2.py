import urllib.request, re, sys, io, urllib.parse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sites = {
    'CoCo都可': 'https://www.coco-tea.com.cn/',
    '可不可熟成紅茶': 'https://kebuke.com/',
    '鮮茶道': 'https://www.presotea.com/',
    '麻古茶坊': 'https://www.macutea.com.tw/',
}

for brand, url in sites.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', 'ignore')
        imgs = re.findall(r'<img[^>]*src=["\']([^"\'>]+)["\'][^>]*>', html)
        favs = re.findall(r'rel=["\'](?:icon|shortcut icon)["\'][^>]*href=["\']([^"\'>]+)["\']', html)
        print(f'=== {brand} ({url}) ===')
        for f in favs:
            print(f'  favicon: {f}')
        for i in imgs[:10]:
            print(f'  img: {i}')
        # also look for logo in CSS or link tags
        logos = re.findall(r'href=["\']([^"\']*logo[^"\']*\.[a-z]{3,4})["\']', html, re.I)
        for l in logos:
            print(f'  logo-link: {l}')
        print()
    except Exception as e:
        print(f'{brand}: ERROR {e}\n')
