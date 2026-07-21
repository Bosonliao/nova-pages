"""
測試不同來源的營業時間：
1. OSM Overpass API（免費）
2. Foursquare Places API（免費額度）
"""
import sys
import io
import json
import urllib.request
import urllib.parse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 方法 1: OSM Overpass API 查光嶼咖啡
print("=== OSM Overpass API ===")
overpass_url = "https://overpass-api.de/api/interpreter"
query = """
[out:json][timeout:25];
(
  node["name"~"光嶼咖啡"](around:5000,24.9132,121.1777);
  way["name"~"光嶼咖啡"](around:5000,24.9132,121.1777);
);
out tags;
"""
data = urllib.parse.urlencode({"data": query}).encode()
try:
    req = urllib.request.Request(overpass_url, data=data)
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
        elements = result.get("elements", [])
        print(f"找到 {len(elements)} 個結果")
        for el in elements:
            tags = el.get("tags", {})
            print(f"  name: {tags.get('name','')}")
            print(f"  opening_hours: {tags.get('opening_hours','N/A')}")
            print(f"  amenity: {tags.get('amenity','N/A')}")
            print(f"  all tags: {tags}")
except Exception as e:
    print(f"Error: {e}")

# 方法 2: OSM Nominatim 查光嶼咖啡
print("\n=== OSM Nominatim ===")
nom_url = "https://nominatim.openstreetmap.org/search"
params = urllib.parse.urlencode({
    "q": "光嶼咖啡 楊梅",
    "format": "json",
    "limit": 5,
    "addressdetails": 1
})
try:
    req = urllib.request.Request(f"{nom_url}?{params}", headers={"User-Agent": "NovaBot/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read())
        print(f"找到 {len(result)} 個結果")
        for r in result:
            print(f"  name: {r.get('display_name','')}")
            print(f"  type: {r.get('type','')}")
            print(f"  class: {r.get('class','')}")
except Exception as e:
    print(f"Error: {e}")

# 方法 3: 用 Playwright 查 Google Maps 但用不同的 URL 格式
# 嘗試 place details 頁面而不是 search 頁
print("\n=== 嘗試 Google Maps CID 直接訪問 ===")
# 從之前的 place URL 取得 CID
cid = "0x346823c67dab675f:0xba9c838c8f44a362"
maps_url = f"https://www.google.com/maps?cid={cid}"
print(f"URL: {maps_url}")