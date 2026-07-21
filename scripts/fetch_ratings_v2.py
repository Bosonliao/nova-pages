"""
用 Playwright 爬 Google Maps 評分和評論數 - v2
改進解析邏輯，用更寬鬆的匹配
"""
from playwright.sync_api import sync_playwright
import json
import time
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

shops = [
    {"city": "taipei", "name": "冷水坑", "county": "台北", "area": "陽明山", "district": "士林區"},
    {"city": "newtaipei", "name": "碧潭", "county": "新北", "area": "新店", "district": "新店區"},
    {"city": "taichung", "name": "審計新村", "county": "台中", "area": "西區", "district": "西區"},
    {"city": "tainan", "name": "神農街", "county": "台南", "area": "中西區", "district": "中西區"},
    {"city": "kaohsiung", "name": "橋頭糖廠", "county": "高雄", "area": "橋頭", "district": "橋頭區"},
]

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for shop in shops:
        try:
            # Search Google Maps with more specific query
            query = f"{shop['name']} {shop['district']}"
            print(f"搜尋: {query}")
            url = f"https://www.google.com/maps/search/{query}"
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(6)

            # Get full page text
            content = page.inner_text("body")
            lines = [l.strip() for l in content.split("\n") if l.strip()]

            rating = None
            reviews = None

            # Print first 50 lines for debugging
            print(f"  --- First 50 lines ---")
            for i, line in enumerate(lines[:50]):
                print(f"  [{i}] {line}")

            # Look for rating: usually a standalone number like "4.3" or "4.1"
            # On Google Maps, rating often appears near star character or as "X.X" 
            for i, line in enumerate(lines):
                # Exact match "4.3"
                if re.match(r'^\d\.\d$', line) and rating is None:
                    rating = float(line)
                    # Check next few lines for reviews count
                    for j in range(i+1, min(i+5, len(lines))):
                        m = re.search(r'([\d,]+)\s*(則評論|則Google評論|reviews|篇評論)', lines[j])
                        if m:
                            reviews = int(m.group(1).replace(",", ""))
                            break
                    break

                # Also check "4.3 顆星" or "4.3 stars"
                m = re.match(r'^(\d\.\d)\s*(顆星|stars|星)', line)
                if m and rating is None:
                    rating = float(m.group(1))
                    break

            # If still no rating, try aria labels
            if rating is None:
                try:
                    els = page.query_selector_all('[aria-label]')
                    for el in els:
                        label = el.get_attribute('aria-label') or ''
                        m = re.search(r'(\d\.\d)\s*(顆星|星|star)', label, re.I)
                        if m:
                            rating = float(m.group(1))
                            # Check for reviews in the same label
                            m2 = re.search(r'([\d,]+)\s*(則評論|reviews|篇評論)', label)
                            if m2 and reviews is None:
                                reviews = int(m2.group(1).replace(",", ""))
                            break
                except:
                    pass

            # If still no reviews, search all lines more broadly
            if reviews is None:
                for line in lines:
                    m = re.search(r'([\d,]+)\s*(則評論|則Google評論|reviews|篇評論)', line)
                    if m:
                        reviews = int(m.group(1).replace(",", ""))
                        break

            result = {**shop, "rating": rating, "reviews": reviews}
            results.append(result)
            print(f"  => rating={rating}, reviews={reviews}")

        except Exception as e:
            result = {**shop, "rating": None, "reviews": None, "error": str(e)}
            results.append(result)
            print(f"  => ERROR: {e}")

        time.sleep(3)

    browser.close()

# Save results
with open("scripts/rating_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n=== Final Results ===")
print(json.dumps(results, ensure_ascii=False, indent=2))