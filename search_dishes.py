"""用 Google 搜尋找菜色 — 透過 requests 直接抓搜尋結果"""
import requests, re, sys, io, time, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def search_dishes(restaurant_name, area=''):
    """搜尋餐廳推薦菜色"""
    query = f'{restaurant_name} {area} 必點 推薦菜'
    url = f'https://www.google.com/search?q={query}&num=10'
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        # 提取文字內容
        text = resp.text
        # 去掉 HTML tags
        clean = re.sub(r'<[^>]+>', ' ', text)
        clean = re.sub(r'\s+', ' ', clean)
        
        # 搜尋常見菜色關鍵字
        dish_patterns = [
            r'必點[：:]\s*([^\n。]{2,30})',
            r'推薦[：:]\s*([^\n。]{2,30})',
            r'招牌[：:]\s*([^\n。]{2,30})',
            r'必吃[：:]\s*([^\n。]{2,30})',
        ]
        
        dishes = set()
        for pattern in dish_patterns:
            matches = re.findall(pattern, clean)
            for m in matches:
                m = m.strip()
                if len(m) > 1 and len(m) < 30:
                    dishes.add(m)
        
        return list(dishes)[:5]
    except Exception as e:
        print(f'ERROR: {e}')
        return []

# 測試
dishes = search_dishes('汕頭泉成沙茶火鍋', '高雄')
print(f'測試結果: {dishes}')