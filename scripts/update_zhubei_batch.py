"""
Update hsinchu.json and drinks.csv with Johnny's 22 Zhubei drink shops
"""
import json, csv, sys, io, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

now = datetime.datetime.now().strftime('%Y-%m-%d')

ZHUbei_DATA = [
    ("得正 #竹北博愛計劃", "新竹縣竹北市博愛街200號", 24.83855, 121.00812),
    ("得正 #竹北勝利計劃", "新竹縣竹北市勝利二路105號", 24.82522, 121.02688),
    ("50嵐 竹北十興店", "新竹縣竹北市莊敬五街138號", 24.82355, 121.02912),
    ("50嵐 竹北正東店", "新竹縣竹北市中正東路262號", 24.83988, 121.01255),
    ("50嵐 竹北博愛店", "新竹縣竹北市博愛街224號", 24.83912, 121.00845),
    ("50嵐 竹北正西店", "新竹縣竹北市中正西路124號", 24.84122, 121.00288),
    ("50嵐 嘉豐南店", "新竹縣竹北市嘉豐南路二段30號", 24.81515, 121.03412),
    ("50嵐 竹北福興東店", "新竹縣竹北市福興東路一段345號", 24.81888, 121.02512),
    ("一沐日 竹北三民店", "新竹縣竹北市三民路328號", 24.84152, 121.00988),
    ("CHILLDAY 鶖茶 竹北三民店", "新竹縣竹北市三民路291號", 24.84088, 121.01042),
    ("茶棧 竹北總店", "新竹縣竹北市中正東路429號", 24.84212, 121.01588),
    ("茶棧 竹北勝利店", "新竹縣竹北市勝利十二街95號", 24.83155, 121.03212),
    ("茶棧 竹北嘉興店", "新竹縣竹北市嘉興路206號", 24.82885, 121.02812),
    ("煉瓦良茶 竹北總店", "新竹縣竹北市勝利一路156號", 24.82422, 121.02755),
    ("希希丁飲品專賣 竹北福興店", "新竹縣竹北市福興東路二段95號", 24.81812, 121.03122),
    ("有飲Youin 竹北三民店", "新竹縣竹北市三民路342號", 24.84188, 121.00955),
    ("龜記茗品 竹北三民店", "新竹縣竹北市三民路270號", 24.84055, 121.01088),
    ("清心福全 竹北文興店", "新竹縣竹北市文興路一段196號", 24.81233, 121.03045),
    ("先喝道 竹北三民店", "新竹縣竹北市三民路353號", 24.84215, 121.00912),
    ("先喝道 竹北勝利店", "新竹縣竹北市勝利二路128號", 24.82588, 121.02645),
    ("搗壺DAOHUDAY 豆腐奶茶", "新竹縣竹北市三民路265號", 24.84032, 121.01112),
    ("沫飲More in. 竹北旗艦店", "新竹縣竹北市自強五路30號", 24.82112, 121.02988),
]

# === 1. Update hsinchu.json ===
data = json.load(open('data/hsinchu.json','r',encoding='utf-8'))
foods = data.get('food', [])

json_updated = 0
json_added = 0

for name, addr, lat, lng in ZHUbei_DATA:
    found = False
    jn = name.replace(' ', '').replace('#', '').replace('.', '')
    for f in foods:
        fn = (f.get('name') or '').replace(' ', '').replace('#', '').replace('.', '')
        if fn == jn or jn in fn or fn in jn:
            f['lat'] = lat
            f['lng'] = lng
            f['address'] = addr
            f['name'] = name
            json_updated += 1
            found = True
            break
        # Brand + branch match
        brand_j = name.split(' ')[0].split('-')[0].split('（')[0].strip()
        brand_f = (f.get('name') or '').split(' ')[0].split('-')[0].split('（')[0].strip()
        if brand_f == brand_j:
            for kw in ['竹北', '博愛', '勝利', '十興', '正東', '正西', '嘉豐', '福興', '三民', '文興']:
                if kw in name and kw in (f.get('name') or ''):
                    f['lat'] = lat
                    f['lng'] = lng
                    f['address'] = addr
                    f['name'] = name
                    json_updated += 1
                    found = True
                    break
            if found:
                break
    
    if not found:
        foods.append({
            "name": name,
            "place_id": "",
            "lat": lat,
            "lng": lng,
            "rating": 0,
            "reviews": 0,
            "address": addr,
            "area": "竹北市",
            "categories": ["飲品"],
            "description": ""
        })
        json_added += 1

data['food'] = foods
with open('data/hsinchu.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'=== hsinchu.json ===')
print(f'Updated: {json_updated}, Added: {json_added}')

# === 2. Update drinks.csv ===
with open('data/drinks.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    csv_rows = list(reader)

csv_updated = 0
csv_added = 0

for name, addr, lat, lng in ZHUbei_DATA:
    parts = name.split(' ', 1)
    brand = parts[0]
    store_name = parts[1] if len(parts) > 1 else ''
    
    found = False
    for row in csv_rows:
        if row.get('county') == '新竹' and '竹北' in (row.get('district') or ''):
            csv_full = f"{row.get('brand','')} {row.get('store_name','')}".strip().replace(' ', '').replace('#', '').replace('.', '')
            jn = name.replace(' ', '').replace('#', '').replace('.', '')
            if csv_full == jn or jn in csv_full or csv_full in jn:
                row['lat'] = str(lat)
                row['lng'] = str(lng)
                row['address'] = addr
                row['source'] = 'johnny'
                row['updated_at'] = now
                csv_updated += 1
                found = True
                break
    
    if not found:
        new_id = 'HS' + str(len(csv_rows) + 1).zfill(3)
        new_row = {fn: '' for fn in fieldnames}
        new_row[fieldnames[0]] = new_id
        new_row['brand'] = brand
        new_row['store_name'] = store_name
        new_row['county'] = '新竹'
        new_row['district'] = '竹北市'
        new_row['address'] = addr
        new_row['lat'] = str(lat)
        new_row['lng'] = str(lng)
        new_row['source'] = 'johnny'
        new_row['updated_at'] = now
        csv_rows.append(new_row)
        csv_added += 1

with open('data/drinks.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(csv_rows)

print(f'\n=== drinks.csv ===')
print(f'Updated: {csv_updated}, Added: {csv_added}')

has = sum(1 for r in csv_rows if r.get('lat') and r.get('lng'))
print(f'drinks.csv total: {len(csv_rows)}, with coords: {has}')
