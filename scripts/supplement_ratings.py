"""
用 Playwright 爬 Google Maps 評分和評論數 - 批次補資料版
"""
from playwright.sync_api import sync_playwright
import json
import time
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def scrape_rating(query):
    """搜尋 Google Maps 並提取評分和評論數"""
    result = {"query": query, "rating": None, "reviews": None}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        url = f"https://www.google.com/maps/search/{query}"
        try:
            page.goto(url, wait_until="networkidle", timeout=30000)
        except Exception as e:
            print(f"  頁面載入超時，繼續嘗試...")
        
        time.sleep(5)
        
        # 取得完整頁面內容
        content = page.inner_text("body")
        lines = [l.strip() for l in content.split("\n") if l.strip()]
        
        # 找評分 - Google Maps 評分通常顯示為 "4.5" 單獨一行
        for i, line in enumerate(lines):
            if re.match(r'^\d\.\d$', line):
                result["rating"] = float(line)
                # 往下找評論數
                for j in range(i+1, min(i+10, len(lines))):
                    next_line = lines[j]
                    m = re.search(r'\(([\d,]+)\)', next_line)
                    if m:
                        result["reviews"] = int(m.group(1).replace(',', ''))
                        break
                    m = re.search(r'([\d,]+)\s*(?:reviews|則評論|篇評論)', next_line)
                    if m:
                        result["reviews"] = int(m.group(1).replace(',', ''))
                        break
                break
        
        # 嘗試 aria-label
        if result["rating"] is None:
            try:
                rating_elements = page.query_selector_all('[aria-label*="星"]')
                for el in rating_elements:
                    label = el.get_attribute('aria-label')
                    if label:
                        m = re.search(r'(\d\.\d)', label)
                        if m:
                            result["rating"] = float(m.group(1))
                            m2 = re.search(r'([\d,]+)\s*(?:則|篇|個)?(?:評論|評分|review)', label)
                            if m2:
                                result["reviews"] = int(m2.group(1).replace(',', ''))
                            break
            except:
                pass
        
        # 嘗試 span
        if result["rating"] is None:
            try:
                spans = page.query_selector_all('span')
                for span in spans:
                    text = span.inner_text().strip()
                    if re.match(r'^\d\.\d$', text):
                        result["rating"] = float(text)
                        break
            except:
                pass
        
        # 嘗試找評論數
        if result["rating"] is not None and result["reviews"] is None:
            try:
                spans = page.query_selector_all('span, div, button')
                for el in spans:
                    text = el.inner_text().strip()
                    m = re.search(r'\(([\d,]+)\)', text)
                    if m:
                        result["reviews"] = int(m.group(1).replace(',', ''))
                        break
                    m = re.search(r'([\d,]+)\s*(?:則評論|篇評論|reviews)', text)
                    if m:
                        result["reviews"] = int(m.group(1).replace(',', ''))
                        break
            except:
                pass
        
        print(f"  評分: {result['rating']}, 評論數: {result['reviews']}")
        if result["rating"] is None:
            print(f"  未找到評分，前30行：")
            for line in lines[:30]:
                if len(line) > 1:
                    print(f"    {line}")
        
        browser.close()
    
    return result

if __name__ == "__main__":
    # 5 spots with null ratings from different cities
    spots = [
        ("三仙台 台東景點", "taitung", "三仙台"),
        ("石雨傘 台東景點", "taitung", "石雨傘"),
        ("石梯坪 花蓮景點", "hualien", "石梯坪"),
        ("橋頭糖廠 高雄景點", "kaohsiung", "橋頭糖廠"),
        ("羅東夜市 宜蘭景點", "yilan", "羅東夜市"),
    ]
    
    results = {}
    for query, city, name in spots:
        print(f"\n搜尋: {query}")
        r = scrape_rating(query)
        results[f"{city}/{name}"] = r
        time.sleep(3)
    
    print("\n=== 最終結果 ===")
    print(json.dumps(results, ensure_ascii=False, indent=2))