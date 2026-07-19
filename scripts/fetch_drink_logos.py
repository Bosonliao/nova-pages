"""
從各品牌官網抓 Logo URL
"""
from playwright.sync_api import sync_playwright
import time
import sys
import io
from urllib.parse import urlparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

brands = {
    '50嵐': 'https://50嵐綠茶.tw/',
    '清心福全': 'https://www.chingshin.tw/',
    'CoCo都可': 'https://www.cocotea.com.tw/',
    '迷客夏': 'https://www.milksha.com/',
    'COMEBUY': 'https://www.comebuy.com.tw/',
    '可不可熟成紅茶': 'https://www.kobuko.com/',
    '茶湯會': 'https://www.teasoup.com.tw/',
    '大苑子': 'https://www.dayungs.com/',
    '鮮茶道': 'https://www.freshtea.com.tw/',
    '麻古茶坊': 'https://www.macotea.com/',
    '茶的魔手': 'https://www.teamotea.com/',
    '珍煮丹': 'https://www.truedan.com/',
    '一沐日': 'https://www.yimoriz.com/',
    '五桐號': 'https://www.wutonghao.com/',
    '八曜和茶': 'https://www.8yao.com/',
    '龜記茗品': 'https://www.gueij.com/',
    '茶聚': 'https://www.teagather.com.tw/',
    '一芳': 'https://www.yifangtea.com/',
    '日出茶太': 'https://www.layatea.com/',
    '老虎堂': 'https://www.tigerlar.com/',
    'UG樂己': 'https://www.ugtea.com/',
}

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for brand, url in brands.items():
        try:
            page = browser.new_page()
            page.goto(url, wait_until='domcontentloaded', timeout=15000)
            time.sleep(2)
            # 找 logo 圖片
            logos = page.query_selector_all('img')
            found = None
            for img in logos:
                src = img.get_attribute('src') or ''
                alt = img.get_attribute('alt') or ''
                cls = img.get_attribute('class') or ''
                if any(k in src.lower() or k in alt.lower() or k in cls.lower() for k in ['logo', 'brand', '主logo']):
                    if src and not src.startswith('data:'):
                        if src.startswith('/'):
                            base = urlparse(url)
                            src = f'{base.scheme}://{base.netloc}{src}'
                        found = src
                        break
            if found:
                print(f'{brand}: {found}')
                results[brand] = found
            else:
                # 找 favicon
                fav = page.query_selector('link[rel="icon"]')
                if fav:
                    href = fav.get_attribute('href')
                    if href and not href.startswith('data:'):
                        if href.startswith('/'):
                            base = urlparse(url)
                            href = f'{base.scheme}://{base.netloc}{href}'
                        print(f'{brand} (favicon): {href}')
                        results[brand] = href
                    else:
                        print(f'{brand}: NOT FOUND')
                else:
                    print(f'{brand}: NOT FOUND')
            page.close()
        except Exception as e:
            print(f'{brand}: ERROR {e}')
    browser.close()

print('\n=== Summary ===')
for brand, logo in results.items():
    print(f'{brand}: {logo}')