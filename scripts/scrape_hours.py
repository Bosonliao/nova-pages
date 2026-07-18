"""
直接用 Playwright 爬 Google Maps 營業時間，不需要 LLM
"""
from playwright.sync_api import sync_playwright
import json
import time

def scrape_business_hours(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print(f"搜尋: {query}")
        url = f"https://www.google.com/maps/search/{query}"
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        
        time.sleep(3)
        
        # 截取頁面文字
        content = page.inner_text("body")
        
        # 找營業時間
        lines = content.split("\n")
        hours_lines = []
        for i, line in enumerate(lines):
            if any(k in line.lower() for k in ["hour", "open", "營業", "時間", "星期", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "週", "日"]):
                hours_lines.append(line.strip())
        
        print(f"\n=== 找到可能的營業時間資訊 ===")
        for h in hours_lines[:20]:
            print(f"  {h}")
        
        if not hours_lines:
            print("找不到營業時間，印出前 50 行頁面內容：")
            for line in lines[:50]:
                if line.strip():
                    print(f"  {line.strip()}")
        
        browser.close()

if __name__ == "__main__":
    scrape_business_hours("光嶼咖啡 楊梅")