"""
菜色搜尋 v3 — 透過 DuckDuckGo HTML 版搜尋
"""
import requests, re, sys, io, json, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def search_dishes(restaurant_name, area=''):
    query = f'{restaurant_name} {area} 必點 推薦 招牌'
    url = f'https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}'
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        text = resp.text
        # 提取搜尋結果摘要
        clean = re.sub(r'<[^>]+>', ' ', text)
        clean = re.sub(r'\s+', ' ', clean)
        
        # 搜尋菜色相關關鍵字
        dishes = set()
        
        # 找「必點」「招牌」「推薦」後面的菜名
        patterns = [
            r'必點[：: ]+([^。\n,，]{2,20})',
            r'招牌[：: ]+([^。\n,，]{2,20})',
            r'推薦[：: ]+([^。\n,，]{2,20})',
            r'必吃[：: ]+([^。\n,，]{2,20})',
            r'人氣[：: ]+([^。\n,，]{2,20})',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, clean)
            for m in matches[:3]:
                m = m.strip()
                if 2 <= len(m) <= 20:
                    dishes.add(m)
        
        return list(dishes)[:5] if dishes else []
    except Exception as e:
        return []

# 測試
test_restaurants = [
    ('西堤牛排 高雄富國店', '左營'),
    ('阿宗芋冰城', '頭城'),
    ('小王煮瓜', '萬華'),
    ('楊寶寶蒸餃', '左營'),
    ('王氏魚皮', '安平'),
]

for name, area in test_restaurants:
    dishes = search_dishes(name, area)
    print(f'{name}: {dishes}')
    time.sleep(2)