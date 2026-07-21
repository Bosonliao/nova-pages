import urllib.request, re, sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sites = {
    '茶湯會': 'https://tw.tp-tea.com/',
    '大苑子': 'https://www.dayungs.com/',
    '一芳': 'https://www.yifangteaglobal.com/tw/',
}

for brand, url in sites.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', 'ignore')
        imgs = re.findall(r'<img[^>]*src=["\']([^"\'>]+)["\'][^>]*>', html)
        print(f'=== {brand} ({url}) ===')
        for i in imgs[:15]:
            print(f'  {i}')
        # also check for favicon
        favs = re.findall(r'rel=["\']icon["\'][^>]*href=["\']([^"\'>]+)["\']', html)
        for f in favs:
            print(f'  favicon: {f}')
        print()
    except Exception as e:
        print(f'{brand}: ERROR {e}')
