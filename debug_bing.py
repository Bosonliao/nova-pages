"""Debug Bing search"""
import requests, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-TW,zh;q=0.9'
}

# Bing 搜尋
url = 'https://www.bing.com/search?q=%E5%B0%8F%E7%8E%8B%E7%85%AE%E7%93%9C+%E5%BF%85%E9%BB%9E&setlang=zh-TW'
resp = requests.get(url, headers=headers, timeout=15)
print(f'Status: {resp.status_code}, Length: {len(resp.text)}')

# 找連結 - 用更簡單的方式
all_links = re.findall(r'href="(https?://[^"]+)"', resp.text)
unique_links = []
seen = set()
for l in all_links:
    if 'bing.com' not in l and 'microsoft.com' not in l and l not in seen:
        unique_links.append(l)
        seen.add(l)

print(f'Found {len(unique_links)} unique external links')
for l in unique_links[:20]:
    print(l[:100])

# 也看看純文字內容裡有沒有菜色
clean = re.sub(r'<[^>]+>', ' ', resp.text)
clean = re.sub(r'\s+', ' ', clean)
# 搜尋「必點」「招牌」附近文字
for pattern in [r'必點[^。]{0,50}', r'招牌[^。]{0,50}', r'推薦[^。]{0,50}']:
    matches = re.findall(pattern, clean)
    for m in matches[:3]:
        print(f'  MATCH: {m.strip()}')