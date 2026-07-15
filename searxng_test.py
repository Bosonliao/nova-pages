import urllib.request, urllib.parse, json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
}

# Try SearXNG public instances
instances = [
    'https://searx.be/search?q=',
    'https://search.sapti.me/search?q=',
    'https://searx.tiekoetter.com/search?q=',
]

queries = [
    '長興圓仔冰 斗六 必吃',
    '聚 日式鍋物 斗六 推薦菜',
    '金誠石火鍋 斗南 推薦',
]

for instance in instances:
    for q in queries:
        url = instance + urllib.parse.quote(q) + '&format=json'
        req = urllib.request.Request(url, headers=headers)
        try:
            r = urllib.request.urlopen(req, timeout=10)
            html = r.read().decode('utf-8', errors='ignore')
            print(f'{instance} [{q[:20]}]: {r.status}, {len(html)} bytes')
            if '長興' in html or '圓仔' in html or '聚' in html or '金誠' in html:
                print('  Found relevant content!')
                # Try to extract text
                text = re.sub(r'<[^>]+>', ' ', html)
                text = re.sub(r'\s+', ' ', text).strip()
                # Find relevant sections
                for keyword in ['必吃', '推薦', '招牌', '菜']:
                    idx = text.find(keyword)
                    if idx > 0:
                        print(f'  [{keyword}]: {text[max(0,idx-30):idx+150]}')
                        break
            time.sleep(1)
        except Exception as e:
            print(f'{instance} [{q[:20]}]: {e}')
        import time
        time.sleep(1)
