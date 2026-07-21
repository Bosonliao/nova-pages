import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

# Updates from cron search results
updates = {
    # 50嵐 大成店: 3.6★ 399 reviews (we had 3.5★ 0 reviews)
    "50嵐 楊梅大成店": {"rating": 3.6, "reviews": 399},
    # 迷客夏 桃園楊梅店: 3.5★ 340 reviews (cron data, our existing had 4.2/137 - keep existing as it might be more recent)
    # 大苑子 大成店: 4.3★ 379 reviews - check if we have it
}

# Also add missing stores found by cron that we don't have
new_stores = [
    {"name": "大苑子 楊梅大成店", "rating": 4.3, "reviews": 379, "area": "楊梅區", "categories": ["飲品"]},
    {"name": "茶湯會 楊梅大成店", "rating": 0, "reviews": 0, "area": "楊梅區", "categories": ["飲品"]},
]

updated = 0
for f in foods:
    if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or [])):
        name = f.get('name', '')
        if name in updates:
            print(f'Updating {name}: {f.get("rating","?")}★ -> {updates[name]["rating"]}★ ({updates[name]["reviews"]} reviews)')
            f['rating'] = updates[name]['rating']
            f['reviews'] = updates[name]['reviews']
            updated += 1

# Check if new stores already exist
existing_names = {f.get('name','') for f in foods if f.get('area') == '楊梅區'}
added = 0
for ns in new_stores:
    if ns['name'] not in existing_names:
        foods.append({
            "name": ns['name'],
            "place_id": "",
            "lat": None,
            "lng": None,
            "rating": ns['rating'],
            "reviews": ns['reviews'],
            "address": "",
            "area": ns['area'],
            "categories": ns['categories'],
            "description": ""
        })
        print(f'Added: {ns["name"]} ({ns["rating"]}★ {ns["reviews"]} reviews)')
        added += 1
    else:
        print(f'Already exists: {ns["name"]}')

data['food'] = foods
with open('data/taoyuan.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

yangmei_drinks = [f for f in foods if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or []))]
print(f'\nTotal 楊梅 drinks: {len(yangmei_drinks)}')
print(f'Updated: {updated}, Added: {added}')
