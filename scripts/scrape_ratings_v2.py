"""
用 Playwright 爬 Google Maps 評分和評論數 - 批次查詢，直接寫檔
"""
from playwright.sync_api import sync_playwright
import json
import time
import sys
import io
import re

def scrape_rating(query, page, browser):
    url = f"https://www.google.com/maps/search/{query}"
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(5)
    
    content = page.inner_text("body")
    lines = [l.strip() for l in content.split("\n") if l.strip()]
    
    rating = None
    reviews = None
    
    # Print first 40 lines for debugging
    output = []
    output.append(f"=== {query} ===")
    for i, line in enumerate(lines[:40]):
        output.append(f"  [{i}] {line}")
    
    # Pattern 1: "X.X" on its own line, followed by review count
    for i, line in enumerate(lines):
        try:
            val = float(line)
            if 1.0 <= val <= 5.0 and "." in line:
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
    
    # Try to find reviews count separately
    if rating and not reviews:
        for line in lines:
            nums = re.findall(r'\(([\d,]+)\s*(?:則評論|reviews?)\)', line)
            if nums:
                reviews = nums[0].replace(",", "")
                break
            # Also try "XXXX 則評論" without parens
            nums2 = re.findall(r'([\d,]+)\s*(?:則評論|reviews?)', line)
            if nums2:
                reviews = nums2[0].replace(",", "")
                break
    
    result = {"query": query, "rating": rating, "reviews": reviews}
    output.append(f"\nRESULT: {json.dumps(result, ensure_ascii=False)}")
    return result, "\n".join(output)

if __name__ == "__main__":
    queries = [
        "馬祖新村眷村文創園區 中壢",
        "三坑老街 桃園龍潭",
        "郭元益糕餅博物館 桃園蘆竹",
        "雅聞魅力博覽館 桃園大溪",
        "楊梅故事園區 桃園楊梅",
    ]
    
    all_output = []
    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for q in queries:
            try:
                r, text = scrape_rating(q, page, browser)
                results.append(r)
                all_output.append(text)
            except Exception as e:
                err = f"Error for {q}: {e}"
                all_output.append(err)
                results.append({"query": q, "rating": None, "reviews": None, "error": str(e)})
            time.sleep(3)
        
        browser.close()
    
    # Write output to file
    with open("scripts/ratings_output.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_output))
        f.write("\n\n=== FINAL RESULTS ===\n")
        f.write(json.dumps(results, ensure_ascii=False, indent=2))
    
    print("Done! Results written to scripts/ratings_output.txt")