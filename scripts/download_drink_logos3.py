import urllib.request, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

logos = {
    'CoCo都可': 'https://www.coco-tea.com.cn/static/portal/images/logo.png',
    '可不可熟成紅茶': 'https://kebuke.com/wp-content/themes/project-theme-v2/src/img/ico/android-icon-192x192.png',
    '鮮茶道': 'https://www.presotea.com/_next/static/media/logo.55c4f148.svg',
    '麻古茶坊': 'https://www.macutea.com.tw/images/fav.png',
}

out_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'drink-logos')

for brand, url in logos.items():
    ext = url.rsplit('.', 1)[-1].split('?')[0]
    filename = f'{brand}.{ext}'
    path = os.path.join(out_dir, filename)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        data = urllib.request.urlopen(req, timeout=10).read()
        with open(path, 'wb') as f:
            f.write(data)
        print(f'OK: {brand} -> {filename} ({len(data)} bytes)')
    except Exception as e:
        print(f'FAIL: {brand} -> {e}')
