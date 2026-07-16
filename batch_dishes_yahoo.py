"""
Batch dish supplement script using Yahoo Search + web_fetch
Bypasses DuckDuckGo bot detection
"""
import urllib.request, urllib.parse, re, html, json, time, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATA_DIR = 'C:/Users/USER/.openclaw/workspace/nova-pages/data'
SCRIPT_DIR = 'C:/Users/USER/.openclaw/workspace/nova-pages'

def yahoo_search(query, max_chars=8000):
    """Search via Yahoo and return text snippets"""
    encoded = urllib.parse.quote(query)
    url = f'https://search.yahoo.com/search?p={encoded}'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-TW,zh;q=0.9'
    })
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        content = resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        return f"Error: {e}"
    
    text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:max_chars]

def extract_dishes_from_text(text, restaurant_name):
    """Extract likely dish names from search result text"""
    # Common dish keywords in Taiwanese restaurant context
    dish_keywords = [
        '招牌', '必點', '推薦', '人氣', '酥脆', '鮮嫩', '爆汁',
        '肉圓', '湯', '飯', '麵', '粥', '羹', '捲', '餅', '包',
        '雞', '豬', '牛', '羊', '魚', '蝦', '蟹', '鴨', '鵝',
        '豆腐', '蘿蔔', '酸菜', '小菜', '涼拌', '滷', '炸', '煎',
        '蒸餃', '水餃', '鍋貼', '蔥油餅', '牛肉麵', '排骨飯',
        '爌肉飯', '肉燥飯', '滷肉飯', '雞肉飯', '虱目魚',
        '乾麵', '湯麵', '米粉', '米糕', '肉粽', '碗粿',
        '披薩', '漢堡', '義大利麵', '燉飯', '咖哩',
        '壽司', '生魚片', '拉麵', '定食', '烏龍麵',
        '火鍋', '麻辣', '臭豆腐', '蚵仔煎', '排骨', '雞腿',
        '香腸', '米血', '甜不辣', '關東煮', '魚丸', '貢丸',
        '芋圓', '豆花', '剉冰', '珍珠奶茶', '紅茶', '咖啡',
        '蛋餅', '蘿蔔糕', '燒餅', '油條', '飯糰', '三明治',
        '蒸蛋', '排骨湯', '雞湯', '魚湯', '豬肚湯', '龍骨髓',
        '脆皮', '鹽酥雞', '炸雞', '烤雞', '桶仔雞',
        '干貝', '香菇', '鳥蛋', '筍絲', '高麗菜',
        '牛肉捲餅', '蔥抓餅', '韭菜盒', '鍋盔',
        '小籠包', '生煎包', '叉燒包', '流沙包',
        '腸粉', '蝦餃', '燒賣', '鳳爪', '蘿蔔糕',
        '抓餅', '蛋餅', '鐵板麵', '厚片', '法式吐司',
        '咖哩飯', '親子丼', '牛丼', '天婦羅', '炸蝦',
        '拉麵', '烏龍麵', '蕎麥麵', '讚岐',
        '炒飯', '燴飯', '燉飯', '焗烤',
        '黑輪', '米苔目', '粄條', '客家',
        '釣蝦', '活蝦', '胡椒蝦', '鹽酥蝦',
        '羊肉爐', '薑母鴨', '麻油雞', '藥燉排骨',
        '四神湯', '豬腳', '蹄膀', '豬腸',
        '冬粉', '蒸蛋', '茶碗蒸',
        '生巧克力', '提拉米蘇', '布朗尼', '乳酪蛋糕',
        '抹茶', '紅豆', '芋頭', '花生',
        '鬆餅', '可麗露', '馬卡龍', '泡芙',
        '冷麵', '蕎麥', '丼飯', '烤肉',
        '串燒', '炸物', '烤物', '揚物',
        '板條', '粄條', '米線', '米粉湯',
        '肉羹', '魷魚羹', '花枝羹', '土魠魚羹',
        '控肉', '滷肉', '豬腳', '蹄膀',
    ]
    
    # Find sentences mentioning the restaurant or dishes
    dishes = []
    seen = set()
    
    # Split into sentences/segments
    segments = re.split(r'[。\n！？；·]', text)
    
    for seg in segments:
        seg = seg.strip()
        if len(seg) < 5 or len(seg) > 300:
            continue
        
        # Look for dish-like patterns
        # Pattern 1: 「菜名」 or "菜名"
        quoted = re.findall(r'[「"「](.{2,15})[」"」]', seg)
        for q in quoted:
            if q not in seen and any(k in q for k in dish_keywords):
                dishes.append(q)
                seen.add(q)
        
        # Pattern 2: 招牌/必點/推薦 + 菜名
        m = re.search(r'(?:招牌|必點|推薦|人氣|招牌菜|必吃)(?:的|是|：|:)?\s*(.{2,20})', seg)
        if m:
            name = m.group(1).strip().rstrip('。，、')
            if name and name not in seen and len(name) <= 15:
                # Check if it looks like a dish
                if any(k in name for k in dish_keywords) or '湯' in name or '飯' in name or '麵' in name:
                    dishes.append(name)
                    seen.add(name)
    
    # Also look for ### headers (from web_fetch markdown)
    headers = re.findall(r'###\s+(.+)', text)
    for h in headers:
        h = h.strip()
        if h and h not in seen and len(h) <= 20 and h != restaurant_name:
            if any(k in h for k in dish_keywords) or '湯' in h or '飯' in h or '麵' in h:
                dishes.append(h)
                seen.add(h)
    
    return dishes[:5]  # Max 5 dishes

def find_next_restaurant():
    """Run the find_next script and parse output"""
    import subprocess
    result = subprocess.run(
        ['python', f'{SCRIPT_DIR}/find_next_restaurant_all.py'],
        capture_output=True, text=True, timeout=30,
        encoding='utf-8', errors='replace'
    )
    if result.stdout is None:
        return {}
    lines = result.stdout.strip().split('\n')
    info = {}
    for line in lines:
        if ':' in line:
            key, val = line.split(':', 1)
            info[key.strip()] = val.strip()
    return info

def save_dishes(county, restaurant_name, dishes):
    """Save dishes to the county JSON file"""
    path = f'{DATA_DIR}/{county}.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for r in data['food']:
        if r['name'] == restaurant_name:
            r['dishes'] = dishes
            break
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def process_one():
    """Process one restaurant"""
    info = find_next_restaurant()
    if not info.get('NEXT_RESTAURANT'):
        print("No more restaurants to process!")
        return False
    
    name = info['NEXT_RESTAURANT']
    county = info['COUNTY']
    remaining = int(info.get('REMAINING', '0'))
    
    print(f"\n{'='*60}")
    print(f"Restaurant: {name} ({county})")
    print(f"Remaining: {remaining}")
    
    # Search for recommended dishes
    queries = [
        f"{name} {county} 推薦菜 必點",
        f"{name} 推薦 必吃",
        f"{name} 招牌菜",
    ]
    
    all_text = ""
    for q in queries:
        print(f"  Searching: {q}")
        result = yahoo_search(q)
        if not result.startswith('Error:'):
            all_text += " " + result
        time.sleep(2)  # Be polite
    
    if not all_text.strip():
        print(f"  -> Search failed, skipping")
        return True
    
    # Extract dishes
    dishes = extract_dishes_from_text(all_text, name)
    
    if not dishes:
        # Try fetching a specific blog page from search results
        print(f"  -> No dishes from search snippets, trying blog fetch...")
        # Try to find a blog URL from search text
        urls = re.findall(r'https?://[^\s<>"]+(?:blog|food|eat|restaurant|美食|小吃)[^\s<>"]*', all_text, re.I)
        if urls:
            print(f"  -> Found URL: {urls[0]}")
            # Can't use web_fetch from here, so just use what we have
        print(f"  -> Could not extract dishes, skipping")
        return True
    
    # Clean up dishes
    cleaned = []
    for d in dishes[:5]:
        d = d.strip()
        if d and len(d) <= 20 and d != name:
            cleaned.append(d)
    
    if not cleaned:
        print(f"  -> No valid dishes found, skipping")
        return True
    
    print(f"  -> Dishes: {cleaned}")
    save_dishes(county, name, cleaned)
    print(f"  -> Saved to {county}.json")
    return True

if __name__ == '__main__':
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    for i in range(count):
        print(f"\n{'#'*60}")
        print(f"Processing restaurant {i+1}/{count}")
        success = process_one()
        if not success:
            break
        time.sleep(3)  # Be polite between searches