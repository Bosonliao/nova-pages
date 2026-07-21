import urllib.request, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sites = {
    '龜記茗品': 'https://www.guiji.com.tw/',
    '一沐日': 'https://www.yimoriz.com/',
    '五桐號': 'https://www.wutonghao.com/',
    '八曜和茶': 'https://www.8yao.com/',
    '茶聚': 'https://www.teagather.com.tw/',
    '老虎堂': 'https://www.tiger sugar.com/',
}

for brand, url in sites.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', 'ignore')
        imgs = re.findall(r'<img[^>]*src=["\']([^"\'>]+)["\'][^>]*>', html)
        favs = re.findall(r'rel=["\'](?:icon|shortcut icon)["\'][^>]*href=["\']([^"\'>]+)["\']', html)
        print(f'=== {brand} ({url}) ===')
        for f in favs[:3]:
            print(f'  favicon: {f}')
        for i in imgs[:5]:
            if 'logo' in i.lower() or 'icon' in i.lower() or 'brand' in i.lower() or 'title' in i.lower() or '.png' in i or '.svg' in i or '.jpg' in i:
                print(f'  img: {i}')
        print()
    except Exception as e:
        print(f'{brand}: ERROR {e}\n')
