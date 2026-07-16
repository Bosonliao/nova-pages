"""Debug: 看 Google 搜尋結果的結構"""
import requests, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-TW,zh;q=0.9'
}

url = 'https://www.google.com/search?q=%E5%B0%8F%E7%8E%8B%E7%85%AE%E7%93%9C+%E5%BF%85%E9%BB%9E&gl=tw&hl=zh-TW'
resp = requests.get(url, headers=headers, timeout=15)
print(f'Status: {resp.status_code}, Length: {len(resp.text)}')

# 看前 2000 字元
text = resp.text[:2000]
# 去掉太長的 HTML 屬性
clean = re.sub(r'=[^ >]{20,}', '=...', text)
print(clean)

print('\n\n--- Link patterns ---')
# 找所有 href
hrefs = re.findall(r'href="([^"]*)"', resp.text)
for h in hrefs[:20]:
    if 'google' not in h and len(h) > 10:
        print(h)

print('\n--- /url?q= patterns ---')
url_links = re.findall(r'/url\?q=([^&]+)', resp.text)
for u in url_links[:10]:
    print(u)

print('\n--- data-href patterns ---')
data_hrefs = re.findall(r'data-href="([^"]*)"', resp.text)
for d in data_hrefs[:10]:
    print(d)