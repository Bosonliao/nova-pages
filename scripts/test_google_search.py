import time
import sys
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # 用 Google 搜尋而不是 Google Maps
    page.goto("https://www.google.com/search?q=光嶼咖啡+楊梅+營業時間", wait_until="domcontentloaded", timeout=15000)
    time.sleep(3)
    
    content = page.inner_text("body")
    lines = content.split("\n")
    
    print("=== Google 搜尋結果 ===")
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or len(line) > 100:
            continue
        if any(k in line for k in ["星期", "週一", "週二", "週三", "週四", "週五", "週六", "週日", "營業", "休息", "公休", "打烊", "11:30", "18:00", "光嶼"]):
            print(f"  [{i}] {line}")
    
    # 也用 aria-label 找
    print("\n=== aria-label ===")
    elements = page.query_selector_all("[aria-label*='星期'], [aria-label*='營業'], [aria-label*='hour']")
    for el in elements:
        aria = el.get_attribute('aria-label')
        text = el.inner_text().strip()[:100]
        print(f"  aria={aria}, text={text}")
    
    # 截圖存檔看看
    page.screenshot(path=r"C:\Users\USER\.openclaw\workspace\nova-pages\scripts\google_search_screenshot.png")
    print("\n截圖已存檔")
    
    browser.close()