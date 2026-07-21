"""
Try Google search (not Maps) to find ratings for the 3 shops that failed
Also try to get review counts for the 2 that got ratings but no reviews
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
            # Try Google search with rating keywords
            query = f"{shop['name']} {shop['area']} 評價 星"
            print(f"搜尋 Google: {query}")
            url = f"https://www.google.com/search?q={query}"
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(4)

            content = page.inner_text("body")
            lines = [l.strip() for l in content.split("\n") if l.strip()]

            rating = None
            reviews = None

            # Look for patterns like "4.2" near "評論" or "星"
            for i, line in enumerate(lines):
                # "4.2" standalone
                if re.match(r'^\d\.\d$', line) and rating is None:
                    rating = float(line)
                    # Look for reviews in nearby lines
                    for j in range(max(0, i-3), min(i+5, len(lines))):
                        m = re.search(r'([\d,]+)\s*(則評論|則Google評論|reviews|篇評論|評論)', lines[j])
                        if m:
                            reviews = int(m.group(1).replace(",", ""))
                            break
                    break

                # "4.2 星" or "4.2顆星"
                m = re.match(r'^(\d\.\d)\s*(顆星|星|stars?)', line)
                if m and rating is None:
                    rating = float(m.group(1))
                    break

                # "評分 4.2" or "4.2 分"
                m = re.search(r'(?:評分|分數|rating)[:\s]*(\d\.\d)', line, re.I)
                if m and rating is None:
                    rating = float(m.group(1))
                    break

            # Also try: "X,XXX 則 Google 評論" anywhere
            if reviews is None:
                for line in lines:
                    m = re.search(r'([\d,]+)\s*則\s*(?:Google\s*)?評論', line)
                    if m:
                        reviews = int(m.group(1).replace(",", ""))
                        break

            # Print some context lines for debugging
            print(f"  First 15 lines:")
            for idx, line in enumerate(lines[:15]):
                print(f"    [{idx}] {line[:80]}")

            result = {**shop, "rating": rating, "reviews": reviews}
            results.append(result)
            print(f"  => rating={rating}, reviews={reviews}\n")

        except Exception as e:
            result = {**shop, "rating": None, "reviews": None, "error": str(e)}
            results.append(result)
            print(f"  => ERROR: {e}\n")

        time.sleep(3)

    browser.close()

print("=== Final Results ===")
print(json.dumps(results, ensure_ascii=False, indent=2))

with open("scripts/cron_rating_results_v2.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)