import urllib.request, os, sys, io, ssl
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

logos = {
    '五桐號': ('https://www.wootea.com/images/logo.png', 'png'),
    '八曜和茶': ('https://8yotea.com/wp-content/uploads/2023/05/logo2023.png', 'png'),
    '龜記茗品': ('https://guiji-group.com/images/fav.png', 'png'),
    '茶聚': ('https://www.chage.com.tw/archive/image/weblogo/1687941808_thumb_2756_1697.png', 'png'),
    '日出茶太': ('https://cdn.chatime.com.tw/2024/01/cropped-CHA23000-FA01-Chatime-Logo-–-Digital_Leaf-Round_RGB-192x192.png', 'png'),
    '老虎堂': ('https://upload.wikimedia.org/wikipedia/en/6/6b/Tiger_Sugar_logo.jpeg', 'jpg'),
    '季緣': ('https://www.chiyuantea.com/images/loadingLogo.png', 'png'),
}

out_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'drink-logos')
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

for brand, (url, ext) in logos.items():
    filename = f'{brand}.{ext}'
    path = os.path.join(out_dir, filename)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        data = urllib.request.urlopen(req, timeout=15, context=ctx).read()
        with open(path, 'wb') as f:
            f.write(data)
        print(f'OK: {brand} -> {filename} ({len(data)} bytes)')
    except Exception as e:
        print(f'FAIL: {brand} -> {e}')
