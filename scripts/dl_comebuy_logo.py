import urllib.request, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')

url = 'https://www.comebuy2002.com.tw/images/logo.png'
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=10)
    data = resp.read()
    out = 'assets/drink-logos/COMEBUY_new.png'
    with open(out, 'wb') as f:
        f.write(data)
    print(f'OK: {os.path.getsize(out)} bytes from logo.png')
except Exception as e:
    print(f'FAIL logo.png: {e}')

url2 = 'https://www.comebuy2002.com.tw/images/logo_m.png'
try:
    req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
    resp2 = urllib.request.urlopen(req2, timeout=10)
    data2 = resp2.read()
    out2 = 'assets/drink-logos/COMEBUY_m.png'
    with open(out2, 'wb') as f:
        f.write(data2)
    print(f'OK: {os.path.getsize(out2)} bytes from logo_m.png')
except Exception as e2:
    print(f'FAIL logo_m.png: {e2}')
