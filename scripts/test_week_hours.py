import time
import sys
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.goto("https://www.google.com/maps/search/光嶼咖啡+楊梅", wait_until="domcontentloaded", timeout=15000)
    time.sleep(4)
    
    # 點「已打烊」展開
    try:
        page.click("text=已打烊", timeout=5000)
        time.sleep(2)
    except:
        pass
    
    # 點「顯示本週營業時間」展開完整週
    try:
        page.click("[aria-label='顯示本週營業時間']", timeout=5000)
        time.sleep(2)
        print("點了「顯示本週營業時間」")
    except:
        print("找不到「顯示本週營業時間」")
    
    # 抓 table 裡的所有行
    tables = page.query_selector_all("table")
    for t in tables:
        text = t.inner_text().strip()
        if "星期" in text or "週" in text:
            print(f"\n=== 營業時間表 ===")
            rows = t.query_selector_all("tr")
            for row in rows:
                cells = row.query_selector_all("td, th")
                cell_texts = [c.inner_text().strip() for c in cells]
                print(f"  {' | '.join(cell_texts)}")
    
    # 也用 aria-label 抓
    print("\n=== aria-label ===")
    elements = page.query_selector_all("[aria-label*='星期'], [aria-label*='複製營業']")
    for el in elements:
        aria = el.get_attribute('aria-label')
        print(f"  {aria}")
    
    browser.close()