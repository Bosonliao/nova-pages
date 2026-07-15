import urllib.request, urllib.parse, json, sys, io, re, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
    'Referer': 'https://duckduckgo.com/',
}

restaurants = [
    "金誠石火鍋 斗南 石頭火鍋 推薦菜",
    "庵古坑咖啡 古坑 推薦 必喝",
    "台灣鯛生態創意園區 口湖 推薦 必吃",
    "圓砌鴛鴦升降鍋物 斗六 推薦菜",
    "長興圓仔冰 斗六 必吃 推薦",
    "聚 日式鍋物 斗六 推薦菜 必吃",
]

for q in restaurants:
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers=headers)
    try:
        r = urllib.request.urlopen(req, timeout=10)
        html = r.read().decode('utf-8', errors='ignore')
        # Extract result snippets
        snippets = re.findall(r'result__snippet[^>]*>(.*?)</a>', html, re.DOTALL)
        clean_snippets = [re.sub(r'<[^>]+>', '', s).strip() for s in snippets[:2]]
        if clean_snippets:
            print(f'\n=== {q} ===')
            for s in clean_snippets:
                print(f'  {s[:200]}')
        else:
            # Check if blocked
            if 'bot' in html.lower() or 'challenge' in html.lower():
                print(f'\n=== {q} === BLOCKED')
            else:
                # Try to find any text content
                text = re.sub(r'<[^>]+>', ' ', html)
                text = re.sub(r'\s+', ' ', text).strip()
                if len(text) > 100:
                    print(f'\n=== {q} ===')
                    print(f'  Text: {text[:300]}')
                else:
                    print(f'\n=== {q} === No results ({len(html)} bytes)')
    except Exception as e:
        print(f'\n=== {q} === Error: {e}')
    time.sleep(2)  # Be polite
