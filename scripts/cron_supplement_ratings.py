"""
Cron script: Search Google Maps for shops missing ratings.
Uses Playwright to search Google Maps and extract rating + review count.
"""
from playwright.sync_api import sync_playwright
import json
import time
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Find null shops from taoyuan (first 5)
city_file = "data/taoyuan.json"
with open(city_file, "r", encoding="utf-8") as f:
    data = json.load(f)

null_shops = []
for s in data["spots"]:
    if s.get("rating") is None or "rating" not in s:
        null_shops.append(s)
        if len(null_shops) >= 5:
            break

print(f"Found {len(null_shops)} null shops in {city_file}")
for s in null_shops:
    print(f"  - {s['name']} ({s.get('area', '')})")

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for shop in null_shops:
        name = shop["name"]
        area = shop.get("area", "")
        query = f"{name} {area}"
        print(f"\n搜尋 Google Maps: {query}")

        try:
            # Search Google Maps
            url = f"https://www.google.com/maps/search/{query}"
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(5)

            content = page.inner_text("body")
            lines = [l.strip() for l in content.split("\n") if l.strip()]

            rating = None
            reviews = None

            # Look for rating pattern "X.X" and review count "X,XXX 則評論"
            for i, line in enumerate(lines):
                # "4.2" standalone - likely a rating
                if re.match(r'^\d\.\d$', line) and rating is None:
                    rating = float(line)
                    # Look for reviews in nearby lines
                    for j in range(max(0, i-5), min(i+10, len(lines))):
                        m = re.search(r'([\d,]+)\s*(則評論|則Google評論|reviews|篇評論|評論)', lines[j])
                        if m:
                            reviews = int(m.group(1).replace(",", ""))
                            break
                    break

            # Also search for review pattern anywhere
            if reviews is None:
                for line in lines:
                    m = re.search(r'([\d,]+)\s*則\s*(?:Google\s*)?評論', line)
                    if m:
                        reviews = int(m.group(1).replace(",", ""))
                        break

            # Try aria-label approach - sometimes rating is in aria attributes
            try:
                rating_elements = page.query_selector_all('[aria-label*="顆星"]')
                for el in rating_elements:
                    label = el.get_attribute("aria-label")
                    if label:
                        m = re.search(r'(\d\.\d)\s*顆星', label)
                        if m and rating is None:
                            rating = float(m.group(1))
                        m2 = re.search(r'([\d,]+)\s*則評論', label)
                        if m2 and reviews is None:
                            reviews = int(m2.group(1).replace(",", ""))
            except:
                pass

            # Print first 20 lines for debugging
            print(f"  First 20 lines:")
            for idx, line in enumerate(lines[:20]):
                print(f"    [{idx}] {line[:100]}")

            result = {"name": name, "area": area, "rating": rating, "reviews": reviews}
            results.append(result)
            print(f"  => rating={rating}, reviews={reviews}")

        except Exception as e:
            result = {"name": name, "area": area, "rating": None, "reviews": None, "error": str(e)}
            results.append(result)
            print(f"  => ERROR: {e}")

        time.sleep(3)

    browser.close()

print("\n=== Final Results ===")
print(json.dumps(results, ensure_ascii=False, indent=2))

# Save results
with open("scripts/cron_supplement_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# Now update the JSON file if we got any ratings
updated = 0
for result in results:
    if result["rating"] is not None:
        for s in data["spots"]:
            if s["name"] == result["name"]:
                s["rating"] = result["rating"]
                if result["reviews"] is not None:
                    s["reviews"] = result["reviews"]
                else:
                    s["reviews"] = 0
                updated += 1
                print(f"Updated: {s['name']} -> rating={s['rating']}, reviews={s['reviews']}")
                break

if updated > 0:
    with open(city_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\nUpdated {updated} shops in {city_file}")
else:
    print("\nNo shops to update (all null results)")