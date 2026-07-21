"""
用 Playwright 爬 Google Maps 評分和評論數
"""
from playwright.sync_api import sync_playwright
import json
import time
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

shops = [
    {"city": "taipei", "name": "冷水坑", "county": "台北", "area": "陽明山"},
    {"city": "newtaipei", "name": "碧潭", "county": "新北", "area": "新店"},
    {"city": "taichung", "name": "審計新村", "county": "台中", "area": "西區"},
    {"city": "tainan", "name": "神農街", "county": "台南", "area": "中西區"},
    {"city": "kaohsiung", "name": "橋頭糖廠", "county": "高雄", "area": "橋頭"},
]

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for shop in shops:
        try:
            query = f"{shop['name']} {shop['county']}{shop['area']}"
            print(f"搜尋: {query}")
            url = f"https://www.google.com/maps/search/{query}"
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(5)

            content = page.inner_text("body")
            lines = content.split("\n")

            rating = None
            reviews = None

            for i, line in enumerate(lines):
                line = line.strip()
                # Look for rating pattern like "4.3" standalone
                if rating is None:
                    import re
                    m = re.match(r'^(\d\.\d)$', line)
                    if m:
                        rating = float(m.group(1))

                # Look for reviews count
                if reviews is None:
                    m = re.match(r'^([\d,]+)\s*(則評論|則Google評論|reviews|篇評論)', line)
                    if m:
                        reviews = int(m.group(1).replace(",", ""))
                    else:
                        m = re.match(r'^\(([\d,]+)\)\s*(則評論|reviews)', line)
                        if m:
                            reviews = int(m.group(1).replace(",", ""))

            result = {**shop, "rating": rating, "reviews": reviews}
            results.append(result)
            print(f"  -> rating={rating}, reviews={reviews}")

        except Exception as e:
            result = {**shop, "rating": None, "reviews": None, "error": str(e)}
            results.append(result)
            print(f"  -> ERROR: {e}")

        time.sleep(3)

    browser.close()

# Save results
with open("scripts/rating_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n=== Results ===")
print(json.dumps(results, ensure_ascii=False, indent=2))