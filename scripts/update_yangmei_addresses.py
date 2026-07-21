import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

# Address data from cron job search
address_updates = {
    "50嵐 埔心中興店": "桃園市楊梅區埔心里中興路103號",
    "50嵐 楊梅大成店": "桃園市楊梅區大成路204號",
    "清心福全楊梅環南店": "桃園市楊梅區環南路180號",
    "清心福全青山店": "桃園市楊梅區青山一街11號",
    "清心福全中山北店": "桃園市楊梅區中山北路二段162號",
    "迷客夏Milksha 桃園楊梅店": "桃園市楊梅區大成路122號",
    "迷客夏Milksha 桃園楊梅埔心店": "桃園市楊梅區埔心里中興路109號",
    "CoCo都可 楊梅大成店": "桃園市楊梅區大成路10-1號",
    "CoCo都可 楊梅環東店": "桃園市楊梅區環東路506號",
    "COMEBUY 楊梅大成店": "桃園市楊梅區大成路118號",
    "可不可熟成茶行 埔心文化店": "桃園市楊梅區埔心文化街250號",
    "茶朵ㄦ 楊梅新成店": None,  # no address found, keep
    "麻古茶坊 楊梅文化店": "桃園市楊梅區光華里文化街167號",
}

# Rating updates
rating_updates = {
    "50嵐 楊梅大成店": (3.6, 399),
    "迷客夏Milksha 桃園楊梅店": (3.5, 340),
    "大苑子 楊梅大成店": (4.3, 379),
}

# New stores to add (not in current DB)
new_stores = [
    {"name": "清心福全 楊梅大成店", "address": "桃園市楊梅區大成路186號", "rating": 0, "reviews": 0},
    {"name": "清心福全 楊梅文化店", "address": "桃園市楊梅區文化街238號", "rating": 0, "reviews": 0},
    {"name": "清心福全 楊梅富岡店", "address": "桃園市楊梅區民富路三段906號", "rating": 0, "reviews": 0},
    {"name": "清心福全 楊梅永美店", "address": "桃園市楊梅區永美路233號", "rating": 0, "reviews": 0},
    {"name": "清心福全 楊梅環東店", "address": "桃園市楊梅區環東路470號", "rating": 0, "reviews": 0},
    {"name": "茶湯會 楊梅大成店", "address": "桃園市楊梅區大成路10號", "rating": 0, "reviews": 0},
    {"name": "大苑子 楊梅大成店", "address": "桃園市楊梅區大成路162號", "rating": 4.3, "reviews": 379},
    {"name": "CoCo都可 楊梅富岡店", "address": "桃園市楊梅區中正路84號", "rating": 0, "reviews": 0},
    {"name": "CoCo都可 埔心中興店", "address": "桃園市楊梅區中興路81號", "rating": 0, "reviews": 0},
    {"name": "CoCo都可 埔心文化店", "address": "桃園市楊梅區埔心文化街250號", "rating": 0, "reviews": 0},
    {"name": "CoCo都可 楊梅楊新店", "address": "桃園市楊梅區大成路232號", "rating": 0, "reviews": 0},
    {"name": "COMEBUY 楊梅埔心店", "address": "桃園市楊梅區中興路18號", "rating": 0, "reviews": 0},
    {"name": "可不可熟成茶行 楊梅文化店", "address": "桃園市楊梅區文化街252號", "rating": 0, "reviews": 0},
    {"name": "麻古茶坊 楊梅新農店", "address": "桃園市楊梅區陽明里新農街521號", "rating": 0, "reviews": 0},
]

# Update existing entries
updated = 0
for f in foods:
    if f.get('area') != '楊梅區':
        continue
    if not any('飲品' in c for c in (f.get('categories') or [])):
        continue
    
    name = f.get('name', '')
    
    # Address updates
    for key, addr in address_updates.items():
        if key in name or name in key:
            if addr and not f.get('address'):
                f['address'] = addr
                updated += 1
                break
    
    # Rating updates
    for key, (rating, reviews) in rating_updates.items():
        if key in name or name in key:
            if f.get('rating', 0) == 0 or not f.get('rating'):
                f['rating'] = rating
                f['reviews'] = reviews
                updated += 1
                break

# Remove "茶聚" entries (no stores in Yangmei)
before = len(foods)
foods = [f for f in foods if not (
    f.get('area') == '楊梅區' and 
    any('飲品' in c for c in (f.get('categories') or [])) and
    '茶聚' in f.get('name', '') and
    'CHAGE' not in f.get('name', '')
)]
removed = before - len(foods)

# Add new stores
existing_names = {f.get('name','') for f in foods if f.get('area') == '楊梅區'}
added = 0
for ns in new_stores:
    if ns['name'] not in existing_names:
        ns.update({
            "place_id": "",
            "lat": None,
            "lng": None,
            "area": "楊梅區",
            "categories": ["飲品"],
            "description": ""
        })
        foods.append(ns)
        existing_names.add(ns['name'])
        added += 1

data['food'] = foods
with open('data/taoyuan.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Summary
yangmei_drinks = [f for f in foods if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or []))]
print(f'Updated existing: {updated}')
print(f'Removed (茶聚 no branch): {removed}')
print(f'Added new: {added}')
print(f'Total 楊梅 drinks: {len(yangmei_drinks)}')
print()
for d in sorted(yangmei_drinks, key=lambda x: x.get('rating',0), reverse=True):
    addr = d.get('address','')
    addr_short = addr.replace('桃園市楊梅區','') if addr else '無地址'
    print(f'  {d["name"]:30s} | {d.get("rating",0):.1f}★ ({d.get("reviews",0)}) | {addr_short}')
