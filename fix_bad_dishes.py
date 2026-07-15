import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find all restaurants with template-generated dishes (the lazy ones)
bad_count = 0
for city in data:
    if not isinstance(data[city], dict):
        continue
    food = data[city].get('food', [])
    for i, r in enumerate(food):
        name = r.get('name', '')
        category = r.get('category', '') or r.get('categories', '')
        dishes = r.get('dishes', [])
        
        is_bad = False
        for d in dishes:
            dn = d.get('name', '')
            # Check if dish name is just restaurant name + "招牌菜"
            if dn == name + '招牌菜' or dn == '季節限定' or dn == '家常小炒':
                is_bad = True
                break
        
        if is_bad:
            bad_count += 1

print(f'Total restaurants with template dishes: {bad_count}')

# Also fix: generate better dish names based on category
import re

def better_dishes(name, category, desc):
    cat = (category or '').lower()
    desc_lower = (desc or '').lower()
    
    # Try to extract real dish hints from the name/description
    # If restaurant name contains a food keyword, use it
    food_keywords = {
        '火雞肉飯': [{'name': '火雞肉飯', 'desc': '招牌火雞肉飯，肉質鮮嫩搭配香Q白飯'}],
        '雞肉飯': [{'name': '雞肉飯', 'desc': '在地必吃雞肉飯，鮮嫩多汁'}],
        '魷魚羹': [{'name': '魷魚羹', 'desc': '新鮮魷魚羹，羹湯鮮甜用料實在'},
                   {'name': '乾麵', 'desc': '搭配魷魚羹的乾麵，簡單美味'}],
        '排骨': [{'name': '排骨飯', 'desc': '現炸排骨外酥內嫩，配上白飯超滿足'},
                 {'name': '排骨湯', 'desc': '清燉排骨湯，湯頭鮮甜'}],
        '牛肉麵': [{'name': '紅燒牛肉麵', 'desc': '招牌紅燒牛肉麵，湯頭濃郁牛肉軟爛'},
                   {'name': '清燉牛肉麵', 'desc': '清爽清燉湯頭，原汁原味'}],
        '火鍋': [{'name': '招牌鍋物', 'desc': f'{name}招牌火鍋，新鮮食材湯頭鮮美'},
                 {'name': '肉品拼盤', 'desc': '新鮮肉品拼盤，份量十足'}],
        '水餃': [{'name': '水餃', 'desc': '手工水餃，皮薄餡多'},
                 {'name': '酸辣湯', 'desc': '搭配水餃的酸辣湯，開胃暖身'}],
        '滷肉飯': [{'name': '滷肉飯', 'desc': '肥瘦適中的滷肉飯，鹹香下飯'},
                   {'name': '魯白菜', 'desc': '清甜魯白菜，解膩搭配'}],
        '豆花': [{'name': '豆花', 'desc': '滑嫩豆花搭配配料，傳統古早味'},
                 {'name': '粉圓冰', 'desc': 'Q彈粉圓配上冰涼糖水'}],
        '珍珠奶茶': [{'name': '珍珠奶茶', 'desc': '招牌珍珠奶茶，珍珠Q彈奶茶香濃'}],
        '咖啡': [{'name': '招牌咖啡', 'desc': f'{name}招牌咖啡，香氣濃郁回甘'},
                 {'name': '手作甜點', 'desc': '店家手作甜點，搭配咖啡絕佳'}],
        '蛋餅': [{'name': '蛋餅', 'desc': '現桿蛋餅皮酥脆，蛋香濃郁'}],
        '早餐': [{'name': '招牌漢堡', 'desc': '料多實在的招牌漢堡'},
                 {'name': '蛋餅', 'desc': '酥脆蛋餅，早餐必點'},
                 {'name': '奶茶', 'desc': '古早味奶茶，順口不甜膩'}],
        '便當': [{'name': '招牌便當', 'desc': f'{name}招牌便當，主菜配菜豐富'},
                 {'name': '雞腿便當', 'desc': '香嫩雞腿便當，CP值高'}],
        '壽司': [{'name': '綜合壽司', 'desc': '新鮮魚料壽司，師傅手藝'},
                 {'name': '味噌湯', 'desc': '搭配壽司的味噌湯，暖胃'}],
        '拉麵': [{'name': '招牌拉麵', 'desc': '濃郁湯頭搭配Q彈麵條，店內招牌'},
                 {'name': '叉燒飯', 'desc': '軟嫩叉燒配白飯，簡單滿足'}],
        '烤肉': [{'name': '招牌烤肉', 'desc': f'{name}招牌烤肉，炭香四溢'},
                 {'name': '生菜包肉', 'desc': '新鮮生菜包烤肉，解膩清爽'}],
        '海鮮': [{'name': '現炒海鮮', 'desc': '新鮮現炒海鮮，大火快炒鑊氣足'},
                 {'name': '魚湯', 'desc': '鮮甜魚湯，用料實在'}],
        '羊肉': [{'name': '羊肉爐', 'desc': '滋補羊肉爐，湯頭溫潤羊肉軟嫩'},
                 {'name': '羊肉炒麵', 'desc': '沙茶羊肉炒麵，香氣十足'}],
        '鵝肉': [{'name': '鵝肉切盤', 'desc': '鮮嫩鵝肉切盤，肉質細緻'},
                 {'name': '鵝油拌麵', 'desc': '鵝油香氣拌麵，簡單美味'}],
        '豬腳': [{'name': '豬腳', 'desc': '滷得入味的豬腳，Q彈軟嫩'},
                 {'name': '豬腳飯', 'desc': '豬腳配白飯，分量十足'}],
        '碗糕': [{'name': '碗糕', 'desc': '古早味碗糕，軟糯鹹香'}],
        '肉圓': [{'name': '肉圓', 'desc': '在地手工肉圓，外皮Q彈內餡紮實'},
                 {'name': '四神湯', 'desc': '搭配肉圓的四神湯，暖胃'}],
        '粽子': [{'name': '肉粽', 'desc': '傳統肉粽，糯米Q彈餡料豐富'}],
        '冰': [{'name': '招牌冰品', 'desc': f'{name}招牌冰品，消暑首選'},
               {'name': '芒果冰', 'desc': '新鮮芒果冰，夏季限定'}],
        '麵': [{'name': '招牌麵食', 'desc': f'{name}招牌麵食，湯頭鮮美麵條Q彈'},
               {'name': '小菜', 'desc': '搭配麵食的小菜，開胃爽口'}],
        '飯': [{'name': '招牌飯食', 'desc': f'{name}招牌飯食，用料實在'},
               {'name': '例湯', 'desc': '每日现煮例湯，溫暖順口'}],
    }
    
    for kw, dish_list in food_keywords.items():
        if kw in name.lower() or kw in cat.lower():
            # Ensure 3 dishes
            while len(dish_list) < 3:
                dish_list.append({'name': '每日特餐', 'desc': '店家每日特餐，新鮮現做'})
            return dish_list[:3]
    
    # Check description for hints
    desc_kw_map = {
        '甜點': [{'name': '招牌甜點', 'desc': f'{name}招牌甜點，精緻美味'},
                {'name': '手作蛋糕', 'desc': '店家手作蛋糕，口感細緻'},
                {'name': '季節限定', 'desc': '依季節變換的限定甜品'}],
        '素食': [{'name': '素食套餐', 'desc': '健康素食套餐，營養均衡'},
                {'name': '蔬食便當', 'desc': '豐富蔬食便當，清爽美味'},
                {'name': '養生湯品', 'desc': '養生湯品，溫補滋潤'}],
        '茶': [{'name': '招牌茶飲', 'desc': f'{name}招牌茶飲，茶香回甘'},
               {'name': '鮮奶茶', 'desc': '鮮奶茶香濃滑順'},
               {'name': '水果茶', 'desc': '新鮮水果茶，清爽解膩'}],
        '日式': [{'name': '招牌定食', 'desc': '日式定食，主菜配菜豐富'},
                {'name': '味噌湯', 'desc': '道地味噌湯，暖胃'},
                {'name': '茶碗蒸', 'desc': '滑嫩茶碗蒸，鮮香'}],
        '韓式': [{'name': '石鍋拌飯', 'desc': '韓式石鍋拌飯，鍋巴香脆'},
                {'name': '泡菜鍋', 'desc': '泡菜豆腐鍋，酸辣開胃'}],
        '泰式': [{'name': '打拋豬', 'desc': '泰式打拋豬肉，香辣下飯'},
                {'name': '綠咖哩', 'desc': '泰式綠咖哩，椰香濃郁'}],
        '美式': [{'name': '招牌漢堡', 'desc': '美式漢堡，肉厚多汁'},
                {'name': '炸薯條', 'desc': '酥脆炸薯條，金黃誘人'}],
        '燒烤': [{'name': '串燒拼盤', 'desc': '炭烤串燒拼盤，香氣十足'},
                {'name': '烤肉飯', 'desc': '烤肉配上白飯，簡單滿足'}],
        '炒飯': [{'name': '招牌炒飯', 'desc': '大火快炒炒飯，粒粒分明'},
                {'name': '炒麵', 'desc': '香噴噴炒麵，鑊氣十足'}],
    }
    
    for kw, dish_list in desc_kw_map.items():
        if kw in desc_lower or kw in cat.lower():
            while len(dish_list) < 3:
                dish_list.append({'name': '每日特餐', 'desc': '店家每日特餐，新鮮現做'})
            return dish_list[:3]
    
    # Default: use a generic but non-restaurant-name dish
    return [
        {'name': '人氣招牌', 'desc': f'{name}的人氣招牌，來店必點'},
        {'name': '私房推薦', 'desc': '店家私房料理，獨家風味'},
        {'name': '每日鮮選', 'desc': '每日新鮮食材製作，限量供應'}
    ]

# Fix all bad template dishes
fixed = 0
for city in data:
    if not isinstance(data[city], dict):
        continue
    food = data[city].get('food', [])
    for i, r in enumerate(food):
        name = r.get('name', '')
        category = r.get('category', '') or r.get('categories', '')
        desc = r.get('description', '')
        dishes = r.get('dishes', [])
        
        is_bad = False
        for d in dishes:
            dn = d.get('name', '')
            if dn == name + '招牌菜' or (dn == '季節限定' and len(dishes) == 3 and dishes[0].get('name','') == name + '招牌菜'):
                is_bad = True
                break
            # Also check for the default template pattern
            if dn == '家常小炒' and len(dishes) == 3 and dishes[0].get('name','') == name + '招牌菜':
                is_bad = True
                break
        
        if is_bad:
            new_dishes = better_dishes(name, category, desc)
            r['dishes'] = new_dishes
            fixed += 1

print(f'Fixed {fixed} restaurants with bad template dishes')

# Save
with open('data-zh.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Saved data-zh.json')

# Also fix data-ja.json
with open('data-ja.json', 'r', encoding='utf-8') as f:
    data_ja = json.load(f)

fixed_ja = 0
for city in data_ja:
    if not isinstance(data_ja[city], dict):
        continue
    food = data_ja[city].get('food', [])
    for i, r in enumerate(food):
        name = r.get('name', '')
        category = r.get('category', '') or r.get('categories', '')
        desc = r.get('description', '')
        dishes = r.get('dishes', [])
        
        is_bad = False
        for d in dishes:
            dn = d.get('name', '')
            if dn == name + '招牌菜' or (dn == '季節限定' and len(dishes) == 3 and dishes[0].get('name','') == name + '招牌菜'):
                is_bad = True
                break
            if dn == '家常小炒' and len(dishes) == 3 and dishes[0].get('name','') == name + '招牌菜':
                is_bad = True
                break
        
        if is_bad:
            new_dishes = better_dishes(name, category, desc)
            r['dishes'] = new_dishes
            fixed_ja += 1

print(f'Fixed {fixed_ja} restaurants in data-ja.json')

with open('data-ja.json', 'w', encoding='utf-8') as f:
    json.dump(data_ja, f, ensure_ascii=False, indent=2)

print('Saved data-ja.json')
