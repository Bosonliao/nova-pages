"""
用 Playwright 爬 Google Maps 評分和評論數 - UTF-8 版本
"""
from playwright.sync_api import sync_playwright
import json
import time
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def scrape_rating(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = f"https://www.google.com/maps/search/{query}"
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(5)
        
        content = page.inner_text("body")
        browser.close()
        
        # 找評分模式
        rating = None
        reviews = None
        
        # 模式1: "4.5 (2,067)"
        m = re.search(r'(\d\.\d)\s*\(([\d,]+)\)', content)
        if m:
            rating = float(m.group(1))
            reviews = int(m.group(2).replace(',', ''))
        
        # 模式2: separate patterns
        if not rating:
            m = re.search(r'(\d\.\d)\s*星', content)
            if m:
                rating = float(m.group(1))
        if not reviews:
            m = re.search(r'([\d,]+)\s*則評論', content)
            if m:
                reviews = int(m.group(1).replace(',', ''))
        
        return rating, reviews, content[:500]

shops = [
    ("白蛇廟", "楊梅"),
    ("鑊篤陂塘生態公園", "楊梅"),
    ("大坑缺石駁生態園區", "楊梅"),
    ("楊梅夜市", "楊梅"),
    ("仙草花田", "楊梅"),
]

results = []
for name, area in shops:
    query = f"{name} {area}"
    print(f"搜尋: {query}")
    try:
        rating, reviews, preview = scrape_rating(query)
        print(f"  -> rating: {rating}, reviews: {reviews}")
        print(f"  -> preview: {preview[:200]}")
        results.append({"name": name, "area": area, "rating": rating, "reviews": reviews})
    except Exception as e:
        print(f"  -> Error: {e}")
        results.append({"name": name, "area": area, "rating": None, "reviews": None})
    time.sleep(3)

print("\n=== Results ===")
print(json.dumps(results, ensure_ascii=False, indent=2))