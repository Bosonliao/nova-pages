"""
Get missing review counts for spots that got ratings but no reviews.
"""
from playwright.sync_api import sync_playwright
import json
import time
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Spots missing reviews
missing_reviews = [
    {"file": "taipei.json", "name": "冷水坑", "area": "陽明山", "lat": 25.1655828, "lng": 121.5640191},
    {"file": "newtaipei.json", "name": "碧潭", "area": "新店", "lat": 24.8663721, "lng": 121.5497801},
    {"file": "newtaipei.json", "name": "猴硐貓村", "area": "瑞芳", "lat": 25.0869527, "lng": 121.8274974},
]

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for shop in missing_reviews:
        name = shop["name"]
        # Try Google search instead of Maps
        query = f"{name} {shop['area']} 台灣 Google 評論 數"
        print(f"\n搜尋 Google: {query}")
        url = f"https://www.google.com/search?q={query}"
        
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(4)

            content = page.inner_text("body")
            lines = [l.strip() for l in content.split("\n") if l.strip()]

            reviews = None
            rating = None

            for i, line in enumerate(lines):
                # "X,XXX 則評論" or "X,XXX reviews"
                m = re.search(r'([\d,]+)\s*(則評論|則Google評論|reviews|篇評論|評論數)', line)
                if m and reviews is None:
                    reviews = int(m.group(1).replace(",", ""))
                
                # "4.3" standalone
                if re.match(r'^\d\.\d$', line) and rating is None:
                    rating = float(line)

            # Print relevant lines for debugging
            print(f"  First 20 lines:")
            for idx, line in enumerate(lines[:20]):
                print(f"    [{idx}] {line[:100]}")

            result = {**shop, "rating": rating, "reviews": reviews}
            results.append(result)
            print(f"  => rating={rating}, reviews={reviews}")

        except Exception as e:
            result = {**shop, "rating": None, "reviews": None, "error": str(e)}
            results.append(result)
            print(f"  => ERROR: {e}")

        time.sleep(3)

    browser.close()

print("\n=== Review Count Results ===")
print(json.dumps(results, ensure_ascii=False, indent=2))

# Now update the JSON files with any found review counts
for result in results:
    if result["reviews"] is not None:
        city_file = f"data/{result['file']}"
        with open(city_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for s in data["spots"]:
            if s["name"] == result["name"]:
                s["reviews"] = result["reviews"]
                print(f"Updated reviews: {s['name']} -> {result['reviews']}")
                break
        
        with open(city_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

print("\nDone!")