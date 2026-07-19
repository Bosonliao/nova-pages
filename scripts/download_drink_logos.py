"""
下載品牌 Logo 到本地 assets/drink-logos/
"""
import urllib.request
import ssl
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

LOGO_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'drink-logos')
os.makedirs(LOGO_DIR, exist_ok=True)

# 已找到的 Logo URL（絕對路徑）
logos = {
    '50嵐': 'https://50嵐綠茶.tw/images/logo.jpg',
    '清心福全': 'https://www.chingshin.tw/img/logo.png',
    '迷客夏': 'https://www.milksha.com/image/logo.jpg',
    'COMEBUY': 'https://www.comebuy.com.tw/template/img/tw/logo/logo01.svg',
    '茶湯會': 'https://teasoup.com.tw/wp-content/uploads/logo-1.png',
    '大苑子': 'https://www.dayungs.com/wp-content/uploads/2020/08/rsz_appstorelogo-1024x312.png',
    '茶的魔手': 'https://static.tildacdn.com/tild6130-3465-4366-a566-336231623331/teamotea_logo.svg',
    '一芳': 'https://www.yifangtea.com/hs-fs/hubfs/yifang%20logo%201.1.png',
    'UG樂己': 'https://www.ugtea.com/themes/basic/skin/images/logo.png',
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

for brand, url in logos.items():
    ext = url.rsplit('.', 1)[-1].split('?')[0]
    filename = f"{brand}.{ext}"
    filepath = os.path.join(LOGO_DIR, filename)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = resp.read()
            with open(filepath, 'wb') as f:
                f.write(data)
            print(f"✅ {brand} → {filename} ({len(data)} bytes)")
    except Exception as e:
        print(f"❌ {brand}: {e}")