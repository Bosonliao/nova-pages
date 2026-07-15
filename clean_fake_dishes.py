import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data-zh.json', encoding='utf-8') as f:
    data = json.load(f)

# Patterns of fake/formulaic dishes
FAKE_DISH_NAMES = {'招牌乾麵', '餛飩湯', '招牌料理', '人氣套餐', '招牌餐點', '推薦套餐', '人氣餐點', '招牌小吃'}
FAKE_DESC_PATTERNS = [
    '人氣推薦的美味選擇',
    '簡單美味的古早味',
    '手工包製的鮮肉餛飩',
    '讓人驚豔',
    '人氣的傳統',
    '特製醬料拌勻',
]

removed = 0
kept = 0
for city, d in data.items():
    if not isinstance(d, dict):
        continue
    for r in d.get('food', []):
        dishes = r.get('dishes', [])
        if not dishes:
            continue
        new_dishes = []
        for dish in dishes:
            if isinstance(dish, dict):
                name = dish.get('name', '')
                desc = dish.get('description', '')
                # Check if this is a fake dish
                is_fake = False
                if name in FAKE_DISH_NAMES:
                    is_fake = True
                for pattern in FAKE_DESC_PATTERNS:
                    if pattern in (desc or ''):
                        is_fake = True
                # Also check restaurant description for formulaic text
                r_desc = r.get('description', '')
                for pattern in FAKE_DESC_PATTERNS:
                    if pattern in r_desc:
                        # If the restaurant desc is formulaic, the dishes are probably fake too
                        is_fake = True
                
                if is_fake:
                    removed += 1
                else:
                    new_dishes.append(dish)
                    kept += 1
            else:
                # String type dish, keep if it looks real
                new_dishes.append(dish)
                kept += 1
        r['dishes'] = new_dishes

# Also clean formulaic restaurant descriptions
for city, d in data.items():
    if not isinstance(d, dict):
        continue
    for r in d.get('food', []):
        desc = r.get('description', '')
        for pattern in FAKE_DESC_PATTERNS:
            if pattern in desc:
                # Check if it's a short generic description (likely AI-generated)
                if len(desc) < 40:
                    r['description'] = ''
                    break

print(f"Removed {removed} fake dishes, kept {kept} real dishes")

with open('data-zh.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',',':'))

# Do the same for data-ja.json
with open('data-ja.json', encoding='utf-8') as f:
    data_ja = json.load(f)

removed_ja = 0
kept_ja = 0
for city, d in data_ja.items():
    if not isinstance(d, dict):
        continue
    for r in d.get('food', []):
        dishes = r.get('dishes', [])
        if not dishes:
            continue
        new_dishes = []
        for dish in dishes:
            if isinstance(dish, dict):
                name = dish.get('name', '')
                desc = dish.get('description', '')
                is_fake = False
                if name in FAKE_DISH_NAMES:
                    is_fake = True
                for pattern in FAKE_DESC_PATTERNS:
                    if pattern in (desc or ''):
                        is_fake = True
                r_desc = r.get('description', '')
                for pattern in FAKE_DESC_PATTERNS:
                    if pattern in r_desc:
                        is_fake = True
                if is_fake:
                    removed_ja += 1
                else:
                    new_dishes.append(dish)
                    kept_ja += 1
            else:
                new_dishes.append(dish)
                kept_ja += 1
        r['dishes'] = new_dishes

for city, d in data_ja.items():
    if not isinstance(d, dict):
        continue
    for r in d.get('food', []):
        desc = r.get('description', '')
        for pattern in FAKE_DESC_PATTERNS:
            if pattern in desc:
                if len(desc) < 40:
                    r['description'] = ''
                    break

print(f"JA: Removed {removed_ja} fake dishes, kept {kept_ja} real dishes")

with open('data-ja.json', 'w', encoding='utf-8') as f:
    json.dump(data_ja, f, ensure_ascii=False, separators=(',',':'))

print("Done! Both files saved.")
