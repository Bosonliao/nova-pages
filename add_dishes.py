"""
Auto-search and add dishes for Taipei restaurants.
Uses DuckDuckGo HTML search to find signature dishes.
Saves every 5 restaurants.
"""
import json
import time
import re
import os
import urllib.request
import urllib.parse
from html import unescape

data_path = r'C:\Users\USER\.openclaw\workspace\nova-pages\data-zh.json'

def load_data():
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def search_ddg(query, max_retries=2):
    """Search DuckDuckGo HTML and return result snippets."""
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(query)
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
            # Extract text snippets from results
            # DDG HTML results have snippets in class="result__snippet"
            snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
            snippets = [unescape(re.sub(r'<[^>]+>', '', s)).strip() for s in snippets]
            # Also extract result titles for context
            titles = re.findall(r'class="result__a"[^>]*>(.*?)</a>', html, re.DOTALL)
            titles = [unescape(re.sub(r'<[^>]+>', '', s)).strip() for s in titles]
            return list(zip(titles, snippets))
        except Exception as e:
            print(f"  Search error (attempt {attempt+1}): {e}")
            time.sleep(2)
    return []

def extract_dishes_from_snippets(results, restaurant_name):
    """Extract likely dish names from search results."""
    dishes = []
    
    # Common dish keywords that indicate a specific dish
    dish_keywords = [
        '牛肉麵', '紅燒', '清燉', '半筋半肉', '麻辣', '鴨血', '豆腐',
        '滷肉飯', '雞肉飯', '控肉飯', '排骨', '雞腿', '豬腳',
        '水餃', '鍋貼', '抄手', '酸辣湯', '牛肉湯', '羊肉湯',
        '生煎包', '小籠包', '蒸餃', '湯包', '蔥油餅',
        '擔仔麵', '乾麵', '湯麵', '粄條', '米粉', '米糕',
        '滷味', '鹽酥雞', '雞排', '甜不辣', '肉圓', '糯米飯',
        '冰品', '豆花', '刨冰', '雪花冰', '湯圓', '紅豆',
        '漢堡', '牛排', '豬排', '雞排', '義大利麵', '燉飯',
        '披薩', '燉飯', ' risotto', 'pasta',
        '拉麵', '壽司', '生魚片', '丼飯', '定食', '天婦羅',
        '燒肉', '烤肉', '火鍋', '麻辣鍋', '酸菜魚',
        '海南雞', '咖哩', '烤鴨', '醉雞', '鹽水雞',
        '炒飯', '炒麵', '燴飯', '排骨飯', '雞腿飯',
        '蚵仔煎', '肉羹', '魚羹', '擔仔麵', '意麵',
        '羊肉', '牛肉', '豬肉', '雞肉', '鴨肉', '鵝肉',
        '魚湯', '海鮮', '熱炒', '三杯', '蔥爆',
        '蛋餅', '吐司', '三明治', 'Brunch',
        '咖菲', '咖啡', '甜點', '蛋糕', '千層',
        '烤魚', '酸菜白肉鍋', '麻辣香鍋',
        '炒手', '涼麵', '麻醬麵', '榨菜肉絲麵',
        '牛肉捲餅', '蔥油餅', '韭菜盒',
        '藥燉排骨', '四神湯', '當歸鴨',
        '胡椒餅', '胡椒蝦', '麻油雞',
        '番茄牛肉麵', '番茄蛋麵',
        '蒜味薯條', '爐烤羊排', '海鮮盤',
        '松露', '白松露', '黑松露',
        '戰斧牛排', '肋眼', '菲力', '沙朗', '紐約客',
        '乾式熟成', '濕式熟成',
        '丼', '炊飯', '茶碗蒸',
        '握壽司', '散壽司', '軍艦',
        '烏龍麵', '蕎麥麵',
        '關東煮', '大阪燒', '章魚燒',
        '部隊鍋', '豆腐鍋', '石鍋拌飯', '銅盤烤肉',
        '春捲', '潤餅', '粽子', '油飯',
        '燒鵝', '燒鴨', '叉燒', '油雞', '脆皮燒肉',
        '煲仔飯', '腸粉', '蘿蔔糕', '叉燒包',
        '飲茶', '蝦餃', '燒賣', '鳳爪',
        '佛跳牆', '紅燒獅子頭', '東坡肉', '梅干扣肉',
        '三杯雞', '白斬雞', '鹹豬肉', '客家小炒',
        '炒米粉', '魷魚羹', '肉燥飯',
    ]
    
    # Also look for quoted dish names or specific patterns
    all_text = ' '.join([f"{t} {s}" for t, s in results])
    
    # Look for patterns like "招牌XXX" or "必點XXX" or "推薦XXX"
    # Also look for dish names followed by prices
    dish_patterns = re.findall(r'[必點推薦招牌]*\s*【?「?([\u4e00-\u9fff]{2,8}(?:麵|飯|湯|餃|包|餅|盤|鍋|雞|鴨|魚|肉|蝦|蟹|菜|糕|冰|捲|捲餅|炒飯|炒麵|燴飯|排|里肌|控肉|滷味|鹽酥|甜不辣|肉圓|豆花|刨冰|雪花冰|湯圓|拉麵|壽司|丼|定食|燒肉|火鍋|咖哩|牛排|豬排|漢堡|三明治|蛋餅|吐司|咖啡|蛋糕|千層|當歸|藥燉|四神|胡椒|麻油|松露|熟成|丼飯|炊飯|握壽司|散壽司|烏龍麵|關東煮|燒賣|蝦餃|鳳爪|叉燒|燒鵝|燒鴨|油雞|煲仔飯|腸粉|蘿蔔糕|佛跳牆|獅子頭|東坡肉|扣肉|三杯雞|白斬雞|鹹豬肉|客家小炒|炒米粉|魷魚羹|肉燥飯|牛肉捲餅|蔥油餅|韭菜盒|藥燉排骨|四神湯|當歸鴨|胡椒餅|胡椒蝦|麻油雞|番茄牛肉麵|蒜味薯條|爐烤羊排|海鮮盤|戰斧牛排|肋眼|菲力|沙朗|紐約客|乾式熟成|茶碗蒸|軍艦|蕎麥麵|大阪燒|章魚燒|部隊鍋|豆腐鍋|石鍋拌飯|銅盤烤肉|春捲|潤餅|粽子|油飯|燒鵝|燒鴨|叉燒|油雞|脆皮燒肉|煲仔飯|腸粉|蘿蔔糕|叉燒包|飲茶|蝦餃|燒賣|鳳爪|佛跳牆|獅子頭|東坡肉|梅干扣肉|三杯雞|白斬雞|鹹豬肉|客家小炒|炒米粉|魷魚羹|肉燥飯))】?」?', all_text)
    
    # Deduplicate while preserving order
    seen = set()
    candidates = []
    for d in dish_patterns:
        d = d.strip()
        if d and d not in seen and len(d) >= 2:
            seen.add(d)
            candidates.append(d)
    
    # Also check for specific dish mentions in snippets
    for title, snippet in results:
        for kw in dish_keywords:
            if kw in snippet or kw in title:
                if kw not in seen:
                    seen.add(kw)
                    candidates.append(kw)
    
    # Filter out the restaurant name itself
    name_chars = set(restaurant_name)
    candidates = [c for c in candidates if c != restaurant_name and not restaurant_name.startswith(c)]
    
    return candidates[:6]  # Return top candidates

def make_desc(dish_name, snippet_text):
    """Generate a one-line description for a dish from snippet context."""
    # Try to find context around the dish name in snippets
    for s in [snippet_text] if isinstance(snippet_text, str) else snippet_text:
        idx = s.find(dish_name)
        if idx >= 0:
            start = max(0, idx - 10)
            end = min(len(s), idx + len(dish_name) + 30)
            context = s[start:end]
            # Clean up
            context = re.sub(r'\s+', ' ', context).strip()
            if len(context) > 5:
                return context[:60]
    return f"{dish_name}，店內人氣招牌"

def process_restaurant(restaurant_name, results):
    """Process search results and return dishes list."""
    if not results:
        return []
    
    candidates = extract_dishes_from_snippets(results, restaurant_name)
    if not candidates:
        return []
    
    # Build snippets text for descriptions
    snippets_text = [s for _, s in results]
    
    dishes = []
    for dish in candidates[:4]:  # Max 4 dishes
        desc = make_desc(dish, snippets_text)
        dishes.append({"name": dish, "desc": desc})
    
    return dishes

def main():
    data = load_data()
    taipei = data['台北']
    food = taipei['food']
    
    # Find restaurants needing dishes
    need_dishes = []
    for i, r in enumerate(food):
        has_michelin = r.get('tags') and 'michelin' in r.get('tags', [])
        is_popular = r.get('rating', 0) >= 4.0 and r.get('reviews', 0) >= 1000
        has_dishes = r.get('dishes') and len(r.get('dishes', [])) > 0
        if (has_michelin or is_popular) and not has_dishes:
            need_dishes.append(i)
    
    print(f"Total restaurants needing dishes: {len(need_dishes)}")
    
    processed = 0
    saved_count = 0
    batch_save_counter = 0
    
    for idx in need_dishes:
        restaurant = food[idx]
        name = restaurant['name']
        
        # Clean name for search (remove extra info after dash/pipe for some names)
        search_name = name.split('-')[0].split('|')[0].split('（')[0].strip()
        if len(search_name) < 2:
            search_name = name
        
        query = f"{search_name} 台北 招牌菜 推薦 必點"
        print(f"\n[{processed+1}/{len(need_dishes)}] Searching: {query}")
        
        results = search_ddg(query)
        print(f"  Got {len(results)} results")
        
        dishes = process_restaurant(name, results)
        
        if dishes:
            food[idx]['dishes'] = dishes
            saved_count += 1
            print(f"  ✓ Added {len(dishes)} dishes: {[d['name'] for d in dishes]}")
        else:
            print(f"  ✗ No dishes found, skipping")
        
        processed += 1
        batch_save_counter += 1
        
        # Save every 5 restaurants
        if batch_save_counter >= 5:
            print(f"\n--- Saving progress (processed {processed}) ---")
            save_data(data)
            batch_save_counter = 0
            print("--- Saved ---")
        
        # Rate limiting
        time.sleep(1.5)
    
    # Final save
    if batch_save_counter > 0:
        print(f"\n--- Final save ---")
        save_data(data)
    
    print(f"\n========== DONE ==========")
    print(f"Total processed: {processed}")
    print(f"Successfully added dishes: {saved_count}")
    print(f"Skipped (no results): {processed - saved_count}")

if __name__ == '__main__':
    main()
