"""
菜色搜尋 v6 — 直接用 web_fetch 抓食記頁面
策略：用各種已知食記網站的搜尋功能
"""
import sys, io, re, json, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 測試用 web_fetch 工具能抓到的食記網站
test_urls = [
    # 痞客邦美食搜尋
    ('pixnet 美食', 'https://emmadoudou.pixnet.net/blog/post/小王煮瓜'),
    # 愛食記
    ('ifoodie', 'https://ifoodie.tw/explore?q=小王煮瓜'),
    # 窩客島
    ('walkerland', 'https://www.walkerland.com.tw/subject/view?title=小王煮瓜'),
    # 食計
    ('eatwise', 'https://eatwise.com.tw/search?q=小王煮瓜'),
]

# 直接測試一些已知的食記 URL
known_food_blogs = [
    'https://niniyeh.com/?s=小王煮瓜',
    'https://victoriatango.pixnet.net/blog/search?q=小王煮瓜',
    'https://tisss.com/?s=小王煮瓜',
]

# 用 Google 進階搜尋 — 可能不被擋
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

# 試 Google Scholar (通常不擋)
url = 'https://scholar.google.com/scholar?q=test'
resp = requests.get(url, headers=headers, timeout=10)
print(f'Google Scholar: {resp.status_code}')

# 試 Google News
url2 = 'https://news.google.com/search?q=小王煮瓜+必點&hl=zh-TW&gl=TW&ceid=TW:zh-Hant'
resp2 = requests.get(url2, headers=headers, timeout=10)
print(f'Google News: {resp2.status_code}, len={len(resp2.text)}')

# 試 Google 的文本搜尋版本
url3 = 'https://www.google.com/search?q=小王煮瓜+必點&gl=tw&hl=zh-TW&tbm=&tbs=li:1'
resp3 = requests.get(url3, headers=headers, timeout=10)
print(f'Google text: {resp3.status_code}, len={len(resp3.text)}')

# 看看 Google News 的內容
clean = re.sub(r'<[^>]+>', ' ', resp2.text[:5000])
clean = re.sub(r'\s+', ' ', clean)
print(f'\nGoogle News content: {clean[:500]}')