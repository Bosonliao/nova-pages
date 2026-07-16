"""用 Google 搜尋餐廳推薦菜色"""
import sys, io, json, re, time, urllib.request, urllib.parse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def google_search_dishes(restaurant_name, area=''):
    """用 Google 搜尋餐廳推薦菜"""
    query = f"{restaurant_name} {area} 推薦菜 必點" if area else f"{restaurant_name} 推薦菜 必點"
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&hl=zh-TW"
    
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8'
    })
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None, str(e)
    
    # Extract snippets from Google search results
    snippets = []
    # Look for text in search result snippets
    for m in re.finditer(r'<span[^>]*>(.*?)</span>', html):
        text = re.sub(r'<[^>]+>', '', m.group(1))
        if len(text) > 20 and any(k in text for k in ['推薦', '必點', '必吃', '招牌', '菜', '好吃']):
            snippets.append(text)
    
    # Also look for menu items
    menu_items = set()
    for s in snippets:
        # Look for Chinese dish names (usually 2-8 chars followed by common food suffixes)
        for m in re.finditer(r'([\u4e00-\u9fff]{2,10}(?:飯|麵|湯|粥|餅|糕|飲|茶|冰|肉|魚|蝦|蟹|雞|鴨|牛|豬|羊|蔬|果|莓|奶|酒|卷|壽司|沙拉|鍋|串|烤|煎|蒸|煮|炒|炸|滷|羹|粿|粽|糰|丸|餃|捲|拼盤|套餐|組合|握壽司))', s):
            menu_items.add(m.group(1))
    
    return list(menu_items)[:10], None

# Test
if __name__ == '__main__':
    name = sys.argv[1] if len(sys.argv) > 1 else '一蘭台灣台北本店'
    area = sys.argv[2] if len(sys.argv) > 2 else ''
    dishes, err = google_search_dishes(name, area)
    if err:
        print(f"ERROR: {err}")
    else:
        print(f"DISHES: {json.dumps(dishes, ensure_ascii=False)}")