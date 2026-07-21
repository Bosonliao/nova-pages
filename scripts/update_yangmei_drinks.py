import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Parse the Google Maps data we scraped
raw_data = [
    ("花火禾茶 はなび 製茶所", 4.9, 1128),
    ("茶詠春-楊梅埔心店", 3.4, 30),
    ("食茶 楊梅平價飲料", 4.8, 104),
    ("金茶伍手作飲品-楊梅瑞溪門市", 4.8, 178),
    ("TrueWin初韻 中壢過嶺店", 4.3, 47),
    ("紅茶媽媽-中壢過嶺店", 4.6, 79),
    ("思茶MissingTea手作飲品 桃園楊梅店", 4.2, 353),
    ("茗茗究市", 4.4, 135),
    ("吾奶王桃園楊梅店", 4.6, 158),
    ("鮮饗茶GOTCHA楊梅店", 4.5, 32),
    ("回憶小時候 楊梅青山店", 5.0, 12),
    ("龜記茗品 楊梅大成店", 4.7, 362),
    ("茶聚CHAGE 楊梅大成店", 4.7, 75),
    ("享飲 手搖杯 創始店", 4.7, 18),
    ("先喝道桃園楊梅店", 3.8, 200),
    ("蓋胖杯茶飲", 4.8, 77),
    ("萃Da手搖飲埔心店", 4.7, 23),
    ("得正#楊梅大成計劃", 3.3, 164),
    ("功夫茶 KUNGFUTEA 楊梅四維店", 4.9, 2419),
    ("迷客夏Milksha 桃園楊梅埔心店", 4.2, 137),
    ("CoCo都可 楊梅幼獅店", 4.5, 174),
    ("五桐號WooTEA 楊梅大成店", 4.3, 84),
    ("上宇林楊梅大成店", 4.0, 111),
    ("Mr.WISH 希望好茶 楊梅金溪店", 4.9, 110),
    ("Tea's原味-楊梅新農店", 4.3, 309),
    ("紅茶巴士 楊梅文化站", 4.5, 136),
    ("皇后先生楊梅新農店", 4.1, 51),
    ("菓點子-楊梅店", None, None),
    ("Coco楊梅楊新店", None, None),
    ("自然湉楊梅大成店", None, None),
    ("永珍珍珠奶茶店", None, None),
    ("茶朵ㄦ埔心店", None, None),
    ("Tea's 原味 楊梅梅獅店", None, None),
    ("COMEBUY 楊梅大成店", None, None),
    ("萬波島嶼紅茶 楊梅大成店", None, None),
    ("50嵐 埔心中興店", None, None),
    ("迷客夏Milksha 桃園楊梅店", None, None),
    ("可不可熟成茶行 楊梅大成店", None, None),
    ("50嵐 楊梅大成店", None, None),
    ("清心福全楊梅環南店", None, None),
    ("清心福全青山店", None, None),
    ("可不可熟成茶行 埔心文化店", None, None),
    ("紅茶帝國 楊梅環南店", None, None),
    ("鮮茶道 埔心站前店", None, None),
    ("CoCo都可 楊梅環東店", None, None),
    ("茶朵ㄦ 楊梅新成店", None, None),
    ("清心福全中山北店", None, None),
    ("鵡緣", None, None),
    ("酷叟茶癮", None, None),
    ("CoCo都可 楊梅大成店", None, None),
    ("薩可米Coffee&Tea", None, None),
    ("麻古茶坊 楊梅文化店", 4.3, 258),  # already added
]

# Load existing data
data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

# Get existing drink shop names in 楊梅區
existing_yangmei = {}
for f in foods:
    if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or [])):
        existing_yangmei[f['name']] = f

print(f"Existing 楊梅 drinks: {len(existing_yangmei)}")

# Map brand names from our data to existing entries
# Clean up names - remove SEO junk
def clean_name(name):
    # Remove everything after | or - or （ that looks like SEO
    name = re.split(r'[|（(]', name)[0].strip()
    return name

# For each scraped shop, check if we need to update or add
updated = 0
added = 0

for shop_name, rating, reviews in raw_data:
    clean = clean_name(shop_name)
    
    # Check by brand match
    brand = clean.split(' ')[0].split('-')[0].split('（')[0].strip()
    
    # Try to find existing match
    found = False
    for f in foods:
        if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or [])):
            # Check if this is the same shop
            if f['name'] == brand or brand in f['name']:
                # Update with better name and rating
                if rating is not None:
                    f['rating'] = rating
                    f['reviews'] = reviews
                f['name'] = clean  # Use full name
                updated += 1
                found = True
                break
    
    if not found:
        # Add new
        new_shop = {
            "name": clean,
            "place_id": "",
            "lat": None,
            "lng": None,
            "rating": rating or 0,
            "reviews": reviews or 0,
            "address": "",
            "area": "楊梅區",
            "categories": ["飲品"],
            "description": ""
        }
        foods.append(new_shop)
        added += 1

# Remove duplicates - keep the one with rating
yangmei_drinks = [f for f in foods if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or []))]
print(f"\nTotal 楊梅 drinks after update: {len(yangmei_drinks)}")
print(f"Updated: {updated}, Added: {added}")

for d in yangmei_drinks:
    print(f'  {d["name"]} | {d.get("rating","?")}★ ({d.get("reviews","?")})')

data['food'] = foods
with open('data/taoyuan.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"\nTotal foods: {len(foods)}")
