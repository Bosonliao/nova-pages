import urllib.request, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

logos = {
    '茶湯會': 'https://tw.tp-tea.com/images/logo_h.png',
    '大苑子': 'https://www.dayungs.com/wp-content/uploads/2021/02/2021大苑子新CI直橫_直式-512X512-1-300x300.png',
    '一芳': 'https://www.yifangteaglobal.com/tw/images/logo.png',
}

out_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'drink-logos')

for brand, url in logos.items():
    ext = url.rsplit('.', 1)[-1].split('?')[0]
    filename = f'{brand}.{ext}'
    path = os.path.join(out_dir, filename)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req, timeout=10).read()
        with open(path, 'wb') as f:
            f.write(data)
        print(f'OK: {brand} -> {filename} ({len(data)} bytes)')
    except Exception as e:
        print(f'FAIL: {brand} -> {e}')
