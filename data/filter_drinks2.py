import json, ijson, time, urllib.request, urllib.parse, sys, os

BRAND_KEYWORDS = [
    "50嵐", "迷客夏", "八曜和茶", "麻古茶坊", "麻古", "龜記", "五桐號",
    "一沐日", "可不可", "茶魔", "季緣", "UG樂己", "茶聚", "COMEBUY",
    "清心福全", "CoCo都可", "coco都可", "茶湯會", "鮮茶道",
    "珍煮丹", "老虎堂", "日出茶太", "La Kaffa", "老賴茶棧",
    "廖老大", "茶的魔手", "翰林茶館", "Tea's原味", "好茶",
    "幸福堂", "Tray Tea", "花好茶", "仰茶", "拾豆", "找好茶"
]

COUNTY_MAP = {
    "基隆市":"基隆","台北市":"台北","新北市":"新北","宜蘭縣":"宜蘭",
    "桃園市":"桃園","新竹市":"新竹","新竹縣":"新竹","苗栗縣":"苗栗",
    "台中市":"台中","南投縣":"南投","彰化縣":"彰化","雲林縣":"雲林",
    "嘉義市":"嘉義","嘉義縣":"嘉義","台南市":"台南","高雄市":"高雄",
    "屏東縣":"屏東","花蓮縣":"花蓮","台東縣":"台東","澎湖縣":"澎湖",
    "金門縣":"金馬","連江縣":"金馬"
}

import re
def extract_area(address):
    m = re.search(r'.+?[市縣](.+?區)', address)
    if m: return m.group(1)
    m = re.search(r'.+?[市縣](.+?[鄉鎮市])', address)
    if m: return m.group(1)
    return ""

def check_brand(name):
    for kw in BRAND_KEYWORDS:
        if kw in name: return True
    return False

# 用 ijson 串流讀取大 JSON
print("串流讀取政府食品業者資料...", flush=True)
drinks = {}
count = 0
with open("97_5.json", "rb") as f:
    parser = ijson.items(f, 'item')
    for v in parser:
        count += 1
        if count % 100000 == 0:
            print(f"已讀取 {count} 筆...", flush=True)
        name = v.get("公司或商業登記名稱", "")
        addr = v.get("業者地址", "")
        if not name or not addr:
            continue
        if check_brand(name):
            key = name + "|" + addr
            if key not in drinks:
                drinks[key] = {"name": name, "address": addr}

print(f"讀取完成，總共 {count} 筆", flush=True)
print(f"篩選出 {len(drinks)} 家手搖飲店", flush=True)

# 按縣市分類
county_drinks = {}
for d in drinks.values():
    county = None
    for full, short in COUNTY_MAP.items():
        if d["address"].startswith(full):
            county = short
            break
    if not county: continue
    area = extract_area(d["address"])
    if not area: continue
    if county not in county_drinks:
        county_drinks[county] = []
    county_drinks[county].append({"name": d["name"], "area": area, "address": d["address"]})

for county, shops in county_drinks.items():
    print(f"{county}: {len(shops)} 家", flush=True)

# 查座標
print("\n開始查座標...", flush=True)
result = {}
total = 0
for county, shops in county_drinks.items():
    seen = set()
    unique = []
    for s in shops:
        if s["name"] not in seen:
            seen.add(s["name"])
            unique.append(s)
    unique = unique[:25]
    result[county] = []
    for s in unique:
        lat, lng = 0, 0
        for q in [f"{s['name']} {s['address']}", s["address"]]:
            encoded = urllib.parse.quote(q)
            url = f"https://nominatim.openstreetmap.org/search?q={encoded}&format=json&limit=1&countrycodes=tw"
            try:
                req = urllib.request.Request(url, headers={"User-Agent":"nova-pages/1.0"})
                resp = urllib.request.urlopen(req, timeout=10)
                data = json.loads(resp.read())
                if data:
                    lat = float(data[0]["lat"])
                    lng = float(data[0]["lon"])
                    if 21.5 <= lat <= 26.5 and 118 <= lng <= 123:
                        break
                    lat, lng = 0, 0
            except: pass
            time.sleep(1.2)
        
        result[county].append({
            "name": s["name"], "lat": lat, "lng": lng,
            "area": s["area"], "categories": ["飲品"],
            "rating": 0, "reviews": 0
        })
        total += 1
        if total % 10 == 0:
            print(f"已查詢 {total} 家...", flush=True)

print("\n寫入 JSON...", flush=True)
for county, shops in result.items():
    if shops:
        fn = f"{county}-drinks.json"
        json.dump(shops, open(fn,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"{fn}: {len(shops)} 家", flush=True)

print(f"\n完成！總共 {total} 家", flush=True)