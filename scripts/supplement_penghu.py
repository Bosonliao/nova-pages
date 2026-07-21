"""
補澎湖飲料店評分
"""
from playwright.sync_api import sync_playwright
import json
import time
import sys
import io
import re
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATA_DIR = 'C:/Users/USER/.openclaw/workspace/nova-pages/data'

def scrape_rating(query):
    result = {"rating": None, "reviews": None}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        url = f"https://www.google.com/maps/search/{query}"
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
        except:
            print(f"  頁面載入超時，繼續嘗試...")
        
        time.sleep(5)
        
        try:
            content = page.inner_text("body")
        except:
            content = ""
        lines = [l.strip() for l in content.split("\n") if l.strip()]
        
        for i, line in enumerate(lines):
            if re.match(r'^\d\.\d$', line):
                result["rating"] = float(line)
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
        
        if result["rating"] is not None and result["reviews"] is None:
            try:
                all_elements = page.query_selector_all('span, div, button')
                for el in all_elements:
                    text = el.inner_text().strip()
                    m = re.search(r'\(([\d,]+)\)', text)
                    if m:
                        val = int(m.group(1).replace(',', ''))
                        if val > 0:
                            result["reviews"] = val
                            break
                    m = re.search(r'([\d,]+)\s*(?:則評論|篇評論|reviews)', text)
                    if m:
                        result["reviews"] = int(m.group(1).replace(',', ''))
                        break
            except:
                pass
        
        print(f"  評分: {result['rating']}, 評論數: {result['reviews']}")
        if result["rating"] is None:
            print(f"  未找到評分，前20行：")
            for line in lines[:20]:
                if len(line) > 1:
                    print(f"    {line}")
        
        browser.close()
    
    return result

# 澎湖-drinks-final.json
filepath = os.path.join(DATA_DIR, '澎湖-drinks-final.json')
with open(filepath, encoding='utf-8') as f:
    shops = json.load(f)

print(f"=== 處理 澎湖-drinks-final.json ({len(shops)} 家) ===")
query = f"{shops[0]['name']} {shops[0]['area']} 澎湖 台灣"
print(f"搜尋: {query}")

r = scrape_rating(query)
if r["rating"] is not None:
    shops[0]["rating"] = r["rating"]
    shops[0]["reviews"] = r["reviews"] or 0
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(shops, f, ensure_ascii=False, indent=2)
    print(f"已更新: rating={r['rating']}, reviews={r['reviews'] or 0}")
else:
    print("未找到評分，跳過")