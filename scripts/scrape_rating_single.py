"""
用 Playwright 爬 Google Maps 評分和評論數 - 單筆查詢
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
        
        # Print first 30 lines for debugging
        print(f"=== {query} ===")
        for i, line in enumerate(lines[:30]):
            print(f"  [{i}] {line}")
        
        # Pattern 1: "X.X" on its own line, followed by "(X,XXX 則評論)" or "(X,XXX reviews)"
        for i, line in enumerate(lines):
            try:
                val = float(line)
                if 1.0 <= val <= 5.0 and "." in line:
                    # Look for review count in next 5 lines
                    for j in range(i+1, min(i+6, len(lines))):
                        nxt = lines[j]
                        if "則評論" in nxt or "reviews" in nxt.lower() or "評論" in nxt:
                            nums = re.findall(r'[\d,]+', nxt)
                            if nums:
                                reviews = nums[0].replace(",", "")
                            break
                    if rating is None:
                        rating = str(val)
                        break
            except ValueError:
                pass
        
        # Pattern 2: regex on full content
        if not rating:
            pattern = r'(\d\.\d)\s*\(([\d,]+)\s*(?:則評論|reviews?)\)'
            matches = re.findall(pattern, content)
            if matches:
                rating = matches[0][0]
                reviews = matches[0][1].replace(",", "")
        
        # Pattern 3: "X.X 顆星" 
        if not rating:
            pattern2 = r'(\d\.\d)\s*(?:顆星|星|stars?)'
            matches2 = re.findall(pattern2, content)
            if matches2:
                rating = matches2[0]
        
        result = {"query": query, "rating": rating, "reviews": reviews}
        print(f"\nRESULT: {json.dumps(result, ensure_ascii=False)}")
        browser.close()
        return result

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "馬祖新村眷村文創園區 中壢"
    try:
        scrape_rating(query)
    except Exception as e:
        print(f"Error: {e}")