"""
菜色搜尋 v4 — 透過 Google 純文字版搜尋 + 食記網站
"""
import requests, re, sys, io, json, time, urllib.parse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}

def google_search_text(query, num=5):
    """用 Google 搜尋並提取純文字結果"""
    url = f'https://www.google.com/search?q={urllib.parse.quote(query)}&num={num}&hl=zh-TW'
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        # 提取所有文字
        text = re.sub(r'<[^>]+>', '\n', resp.text)
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'  +', ' ', text)
        return text
    except Exception as e:
        return ''

def search_dishes(restaurant_name, area='', category=''):
    """搜尋餐廳推薦菜色"""
    query = f'{restaurant_name} {area} 必點 推薦菜 招牌'
    text = google_search_text(query)
    
    if not text:
        return []
    
    # 找所有可能的菜色名稱
    dishes = set()
    
    # 方法 1: 找「必點」「招牌」等關鍵字附近的菜名
    patterns = [
        r'必點[：: ]+([^。\n,，！!？?]{2,25})',
        r'招牌[：: ]+([^。\n,，！!？?]{2,25})',
        r'推薦[：: ]+([^。\n,，！!？?]{2,25})',
        r'必吃[：: ]+([^。\n,，！!？?]{2,25})',
        r'人氣[：: ]+([^。\n,，！!？?]{2,25})',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for m in matches[:3]:
            m = m.strip()
            if 2 <= len(m) <= 20 and not any(x in m for x in ['我們', '這家', '這間', '可以', '比較', '非常', '覺得']):
                dishes.add(m)
    
    return list(dishes)[:5] if dishes else []

# 測試
tests = [
    ('西堤牛排 高雄富國店', '左營', '西式'),
    ('阿宗芋冰城', '頭城', '甜品'),
    ('小王煮瓜', '萬華', '中式'),
    ('楊寶寶蒸餃', '左營', '中式'),
    ('王氏魚皮', '安平', '中式'),
]

for name, area, cat in tests:
    dishes = search_dishes(name, area, cat)
    print(f'{name}: {dishes}')
    time.sleep(3)