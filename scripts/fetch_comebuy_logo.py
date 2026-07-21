import urllib.request, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')

urls = [
    'https://www.comebuy2002.com.tw/wp-content/uploads/2020/07/comebuy-logo.png',
    'https://www.comebuy2002.com.tw/wp-content/uploads/2020/07/cropped-comebuy-icon-1.png',
    'https://www.comebuy2002.com.tw/wp-content/themes/flavor/assets/img/logo.png',
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=10)
        data = resp.read()
        out = 'assets/drink-logos/COMEBUY.png'
        with open(out, 'wb') as f:
            f.write(data)
        size = os.path.getsize(out)
        print(f'OK from {url.split("/")[-1]}: {size} bytes')
        break
    except Exception as e:
        print(f'FAIL {url}: {e}')
else:
    print('All failed')
