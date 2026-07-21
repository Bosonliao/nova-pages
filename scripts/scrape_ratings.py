"""
用 Playwright 爬 Google Maps 評分和評論數 - 改良版
"""
from playwright.sync_api import sync_playwright
import json
import time
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def scrape_rating(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = f"https://www.google.com/maps/search/{query}"
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        
        time.sleep(5)
        
        content = page.inner_text("body")
        lines = [l.strip() for l in content.split("\n") if l.strip()]
        
        rating = None
        reviews = None
        
        # Strategy: find lines that look like "X.X" (rating) and nearby lines with review count
        for i, line in enumerate(lines):
            # Match rating pattern: a number like 4.5, 3.9, etc.
            if re.match(r'^\d\.\d$', line):
                val = float(line)
                if 0 <= val <= 5:
                    # Look in next 5 lines for review count
                    for j in range(i+1, min(len(lines), i+6)):
                        candidate = lines[j]
                        # Match patterns like "123 則評論" or "1,234 reviews" or just "123則評論"
                        m = re.search(r'([\d,]+)\s*(則評論|reviews|則評價)', candidate)
                        if m:
                            reviews = int(m.group(1).replace(",", ""))
                            rating = val
                            break
                    # Also check if rating line itself contains reviews
                    if reviews is None:
                        m = re.search(r'([\d,]+)\s*(則評論|reviews|則評價)', line)
                        if m:
                            reviews = int(m.group(1).replace(",", ""))
                    if rating is None:
                        rating = val
        
        # If still no rating found, try broader approach
        if rating is None:
            for i, line in enumerate(lines):
                # Look for "X.X 星" pattern
                m = re.match(r'^(\d\.\d)\s*星?$', line)
                if m:
                    rating = float(m.group(1))
                    for j in range(i+1, min(len(lines), i+6)):
                        m2 = re.search(r'([\d,]+)\s*(則評論|reviews|則評價)', lines[j])
                        if m2:
                            reviews = int(m2.group(1).replace(",", ""))
                            break
                    break
        
        browser.close()
        return rating, reviews

if __name__ == "__main__":
    queries = [
        "白蛇廟 楊梅 桃園",
        "鑊篤陂塘生態公園 楊梅",
        "大坑缺石駁生態園區 楊梅",
        "楊梅夜市 桃園",
        "仙草花田 楊梅 桃園",
    ]
    
    results = {}
    for q in queries:
        print(f"\n搜尋: {q}")
        rating, reviews = scrape_rating(q)
        results[q] = {"rating": rating, "reviews": reviews}
        print(f"  → rating: {rating}, reviews: {reviews}")
        time.sleep(3)
    
    print("\n=== 結果 ===")
    print(json.dumps(results, ensure_ascii=False, indent=2))