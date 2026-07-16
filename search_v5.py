"""
菜色搜尋 v5 — 用 Python requests 抓 Google 搜尋結果，解析食記頁面
"""
import requests, re, sys, io, json, time, urllib.parse, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

def google_search_links(query, num=5):
    """用 Google 搜尋並提取結果連結"""
    url = f'https://www.google.com/search?q={urllib.parse.quote(query)}&num={num}&gl=tw&hl=zh-TW'
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        text = resp.text
        # 提取搜尋結果 URL
        links = re.findall(r'/url\?q=([^&]+)', text)
        # 過濾掉 google 自己的連結
        clean_links = []
        for l in links:
            l = urllib.parse.unquote(l)
            if 'google.com' not in l and 'youtube.com' not in l:
                clean_links.append(l)
        return clean_links[:num]
    except:
        return []

def fetch_page(url):
    """抓取頁面內容"""
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        text = resp.text
        # 去掉 HTML tags
        clean = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
        clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
        clean = re.sub(r'<[^>]+>', '\n', clean)
        clean = html.unescape(clean)
        clean = re.sub(r'\n\s*\n', '\n', clean)
        clean = re.sub(r'  +', ' ', clean)
        return clean
    except:
        return ''

def extract_dishes(text, restaurant_name):
    """從食記內容提取菜色"""
    dishes = set()
    
    # 各種菜色提取模式
    patterns = [
        r'必點[：: ]+([^。\n,，！!？?；;]{2,25})',
        r'招牌[：: ]+([^。\n,，！!？?；;]{2,25})',
        r'推薦[：: ]+([^。\n,，！!？?；;]{2,25})',
        r'必吃[：: ]+([^。\n,，！!？?；;]{2,25})',
        r'人氣[：: ]+([^。\n,，！!？?；;]{2,25})',
        r'★\s*([^★\n]{2,25})',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for m in matches[:5]:
            m = m.strip()
            # 過濾掉非菜色的詞
            if 2 <= len(m) <= 20 and not any(x in m for x in 
                ['我們', '這家', '這間', '可以', '比較', '非常', '覺得', '真的',
                 '一下', '口感', '味道', '好吃', '不錯', '地址', '電話', '營業',
                 '捷運', '公車', '停車', '價格', '價位', '消費', '每人', '低消',
                 '點了', '吃了', '覺得', '朋友', '今天', '這次', '第一次',
                 '菜单', '菜單', 'menu']):
                dishes.add(m)
    
    return list(dishes)[:5] if dishes else []

def search_dishes(restaurant_name, area='', category=''):
    """完整搜尋流程"""
    query = f'{restaurant_name} {area} 必點 推薦 招牌' if area else f'{restaurant_name} 必點 推薦 招牌'
    
    # Step 1: Google 搜尋找食記連結
    links = google_search_links(query, num=5)
    if not links:
        return []
    
    # Step 2: 抓取前 2 個食記頁面
    all_dishes = set()
    for link in links[:3]:
        page_text = fetch_page(link)
        if page_text:
            found = extract_dishes(page_text, restaurant_name)
            all_dishes.update(found)
        time.sleep(1)
    
    return list(all_dishes)[:5]

# 測試
tests = [
    ('小王煮瓜', '萬華', '中式'),
    ('楊寶寶蒸餃', '左營', '中式'),
    ('王氏魚皮', '安平', '中式'),
    ('阿宗芋冰城', '頭城', '甜品'),
    ('赤鬼炙燒牛排', '', '西式'),
]

for name, area, cat in tests:
    dishes = search_dishes(name, area, cat)
    print(f'{name}: {dishes}')
    time.sleep(2)