import json
import re
import time
import urllib.request
import urllib.parse

# 知名手搖飲連鎖品牌關鍵字
BRAND_KEYWORDS = [
    "50嵐", "迷客夏", "八曜和茶", "麻古茶坊", "麻古", "龜記", "五桐號",
    "一沐日", "可不可", "可不可熟成紅茶", "茶魔", "季緣", "UG樂己",
    "茶聚", "COMEBUY", "清心福全", "CoCo都可", "coco都可", "CoCo",
    "茶湯會", "鮮茶道", "Tea's 原味", "茶自飲", "喝茶好嗎",
    "翰林茶館", "老賴茶棧", "廖老大", "茶的魔手", "茶研社",
    "水舞饌", "桐花茶鄉", "一茶天下", "茶街", "好茶",
    "珍煮丹", "Tray Tea", "幸福堂", "老虎堂", "老虎牙子",
    "花好茶", "茶葉有約", "仰茶", "拾豆", "找好茶",
    "茶之鄉", "原沏", "鮮茶一番", "日出茶太", "La Kaffa",
    "囍杯杯", "杯杯", "飲茶人家", "茶坊", "茶行"
]

# 縣市對照表
COUNTY_MAP = {
    "基隆市": "基隆", "台北市": "台北", "新北市": "新北",
    "宜蘭縣": "宜蘭", "桃園市": "桃園", "新竹市": "新竹",
    "新竹縣": "新竹", "苗栗縣": "苗栗", "台中市": "台中",
    "南投縣": "南投", "彰化縣": "彰化", "雲林縣": "雲林",
    "嘉義市": "嘉義", "嘉義縣": "嘉義", "台南市": "台南",
    "高雄市": "高雄", "屏東縣": "屏東", "花蓮縣": "花蓮",
    "台東縣": "台東", "澎湖縣": "澎湖", "金門縣": "金馬",
    "連江縣": "金馬"
}

# 區域提取（從地址中提取區/鄉/鎮/市）
def extract_area(address):
    # 台北/新北/桃園/台中/台南/高雄 用「區」
    m = re.search(r'(.+?[市縣])(.+?區)', address)
    if m:
        return m.group(2)
    # 其他用「鄉/鎮/市」
    m = re.search(r'.+?[市縣](.+?[鄉鎮市])', address)
    if m:
        return m.group(1)
    return ""

def check_brand(name):
    for kw in BRAND_KEYWORDS:
        if kw in name:
            return True
    return False

# 讀取政府資料
print("讀取政府食品業者資料...")
with open("97_5.json", "r", encoding="utf-8") as f:
    vendors = json.load(f)

print(f"總共 {len(vendors)} 筆資料")

# 篩選飲料店
print("篩選手搖飲店...")
drinks = {}
for v in vendors:
    name = v.get("公司或商業登記名稱", "")
    addr = v.get("業者地址", "")
    if not name or not addr:
        continue
    if check_brand(name):
        # 去重（同一地址同一店名只保留一筆）
        key = name + "|" + addr
        if key not in drinks:
            drinks[key] = {"name": name, "address": addr}

print(f"篩選出 {len(drinks)} 家手搖飲店")

# 按縣市分類
county_drinks = {}
for d in drinks.values():
    addr = d["address"]
    county = None
    for full_county, short_county in COUNTY_MAP.items():
        if addr.startswith(full_county):
            county = short_county
            break
    if not county:
        continue
    area = extract_area(addr)
    if not area:
        continue
    if county not in county_drinks:
        county_drinks[county] = []
    county_drinks[county].append({
        "name": d["name"],
        "area": area,
        "address": d["address"]
    })

# 統計
for county, shops in county_drinks.items():
    print(f"{county}: {len(shops)} 家")

# 用 Nominatim 查座標（每縣市最多取 30 家，避免太多 API 呼叫）
print("\n開始查座標...")
result = {}
total_queries = 0
for county, shops in county_drinks.items():
    # 去重同名店（同縣市同名只取第一家）
    seen_names = set()
    unique_shops = []
    for s in shops:
        if s["name"] not in seen_names:
            seen_names.add(s["name"])
            unique_shops.append(s)
    # 最多 30 家
    unique_shops = unique_shops[:30]
    
    result[county] = []
    for s in unique_shops:
        # 用店名 + 地址查座標
        query = f"{s['name']} {s['address']}"
        encoded = urllib.parse.quote(query)
        url = f"https://nominatim.openstreetmap.org/search?q={encoded}&format=json&limit=1&countrycodes=tw"
        
        lat = 0
        lng = 0
        
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "nova-pages/1.0"})
            resp = urllib.request.urlopen(req, timeout=10)
            data = json.loads(resp.read())
            if data:
                lat = float(data[0]["lat"])
                lng = float(data[0]["lon"])
        except Exception as e:
            # 嘗試只用地址查
            try:
                encoded2 = urllib.parse.quote(s["address"])
                url2 = f"https://nominatim.openstreetmap.org/search?q={encoded2}&format=json&limit=1&countrycodes=tw"
                req2 = urllib.request.Request(url2, headers={"User-Agent": "nova-pages/1.0"})
                resp2 = urllib.request.urlopen(req2, timeout=10)
                data2 = json.loads(resp2.read())
                if data2:
                    lat = float(data2[0]["lat"])
                    lng = float(data2[0]["lon"])
            except:
                pass
        
        result[county].append({
            "name": s["name"],
            "lat": lat,
            "lng": lng,
            "area": s["area"],
            "categories": ["飲品"],
            "rating": 0,
            "reviews": 0
        })
        
        total_queries += 1
        if total_queries % 10 == 0:
            print(f"已查詢 {total_queries} 家...")
        
        time.sleep(1)  # Nominatim 要求每次查詢間隔至少 1 秒

# 輸出每個縣市的飲料店 JSON
print("\n寫入 JSON 檔...")
for county, shops in result.items():
    if shops:
        filename = f"data/{COUNTY_MAP.get(county, county)}-drinks.json"
        # 反查 county short name
        short = county
        for full, s in COUNTY_MAP.items():
            if s == county:
                short = s
                break
        filename = f"data/{short}-drinks.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(shops, f, ensure_ascii=False, indent=2)
        print(f"{filename}: {len(shops)} 家")

print(f"\n完成！總共查詢 {total_queries} 家飲料店")