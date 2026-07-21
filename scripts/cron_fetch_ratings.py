"""
Cron task: 用 Playwright 爬 Google Maps 評分和評論數
Targets 5 shops with null ratings from city JSON files
"""
from playwright.sync_api import sync_playwright
import json
import time
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

shops = [
    {"city": "taoyuan", "name": "雅聞魅力博覽館", "area": "楊梅", "lat": 24.9067588, "lng": 121.1508582},
    {"city": "yilan", "name": "羅東夜市", "area": "羅東", "lat": 24.6770442, "lng": 121.7693122},
    {"city": "miaoli", "name": "崎頂子母隧道", "area": "竹南鎮", "lat": 24.7276784, "lng": 120.8763224},
    {"city": "changhua", "name": "八卦山天空步道", "area": "彰化市", "lat": 24.0782765, "lng": 120.5496666},
    {"city": "nantou", "name": "中興新村", "area": "南投市", "lat": 23.955234, "lng": 120.687352},
]

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for shop in shops:
        try:
            query = f"{shop['name']} {shop['area']}"
            print(f"搜尋: {query}")
            url = f"https://www.google.com/maps/search/{query}"
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(6)

            content = page.inner_text("body")
            lines = [l.strip() for l in content.split("\n") if l.strip()]

            rating = None
            reviews = None

            # Print first 30 lines for debugging
            for i, line in enumerate(lines[:30]):
                print(f"  [{i}] {line}")

            # Look for rating: standalone number like "4.3"
            for i, line in enumerate(lines):
                if re.match(r'^\d\.\d$', line) and rating is None:
                    rating = float(line)
                    for j in range(i+1, min(i+5, len(lines))):
                        m = re.search(r'([\d,]+)\s*(則評論|則Google評論|reviews|篇評論)', lines[j])
                        if m:
                            reviews = int(m.group(1).replace(",", ""))
                            break
                    break

                m = re.match(r'^(\d\.\d)\s*(顆星|stars|星)', line)
                if m and rating is None:
                    rating = float(m.group(1))
                    break

            # Try aria labels
            if rating is None:
                try:
                    els = page.query_selector_all('[aria-label]')
                    for el in els:
                        label = el.get_attribute('aria-label') or ''
                        m = re.search(r'(\d\.\d)\s*(顆星|星|star)', label, re.I)
                        if m:
                            rating = float(m.group(1))
                            m2 = re.search(r'([\d,]+)\s*(則評論|reviews|篇評論)', label)
                            if m2 and reviews is None:
                                reviews = int(m2.group(1).replace(",", ""))
                            break
                except:
                    pass

            # Search all lines for reviews if still missing
            if reviews is None:
                for line in lines:
                    m = re.search(r'([\d,]+)\s*(則評論|則Google評論|reviews|篇評論)', line)
                    if m:
                        reviews = int(m.group(1).replace(",", ""))
                        break

            result = {**shop, "rating": rating, "reviews": reviews}
            results.append(result)
            print(f"  => rating={rating}, reviews={reviews}\n")

        except Exception as e:
            result = {**shop, "rating": None, "reviews": None, "error": str(e)}
            results.append(result)
            print(f"  => ERROR: {e}\n")

        time.sleep(3)

    browser.close()

# Save results
with open("scripts/cron_rating_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("=== Final Results ===")
print(json.dumps(results, ensure_ascii=False, indent=2))