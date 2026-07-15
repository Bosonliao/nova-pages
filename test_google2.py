import urllib.request, urllib.parse, json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
}

# Check Google raw HTML
q = '千巧谷牛樂園牧場 推薦菜 必吃'
url2 = 'https://www.google.com/search?q=' + urllib.parse.quote(q) + '&hl=zh-TW&gl=tw&num=10'
req2 = urllib.request.Request(url2, headers=headers)
r2 = urllib.request.urlopen(req2, timeout=15)
html2 = r2.read().decode('utf-8', errors='ignore')

if '千巧谷' in html2:
    print('Google raw HTML: Found restaurant!')
    idx = 0
    count = 0
    while True:
        idx = html2.find('千巧谷', idx)
        if idx == -1:
            break
        context = re.sub(r'<[^>]+>', ' ', html2[max(0,idx-100):idx+200])
        context = re.sub(r'\s+', ' ', context).strip()
        print(f'  [{count}] {context[:150]}')
        idx += 3
        count += 1
        if count >= 5:
            break
else:
    print('Google raw HTML: NOT found')
    title_match = re.search(r'<title>(.*?)</title>', html2)
    title = title_match.group(1) if title_match else '?'
    print(f'  Title: {title}')
    has_captcha = 'captcha' in html2.lower() or 'blocked' in html2.lower()
    print(f'  Has captcha: {has_captcha}')
    # Check for consent page
    has_consent = 'consent' in html2.lower() or 'cookie' in html2.lower()
    print(f'  Has consent: {has_consent}')
    # Show a snippet
    text = re.sub(r'<[^>]+>', ' ', html2)
    text = re.sub(r'\s+', ' ', text).strip()
    print(f'  Text snippet: {text[:500]}')
