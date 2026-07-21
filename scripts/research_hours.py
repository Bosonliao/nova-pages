"""
研究 Google Maps 完整營業時間表的 DOM 結構
目標：抓到星期一到星期日的完整營業時間
"""
import time
import sys
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.goto("https://www.google.com/maps/search/光嶼咖啡+楊梅", wait_until="domcontentloaded", timeout=15000)
    time.sleep(5)
    
    # Step 1: 點「已打烊」展開營業時間區塊
    try:
        page.click("text=已打烊", timeout=5000)
        time.sleep(3)
        print("Step 1: 點了「已打烊」")
    except:
        print("Step 1: 找不到「已打烊」")
    
    # Step 2: 點「顯示本週營業時間」
    try:
        page.click("[aria-label='顯示本週營業時間']", timeout=5000)
        time.sleep(3)
        print("Step 2: 點了「顯示本週營業時間」")
    except:
        print("Step 2: 找不到「顯示本週營業時間」按鈕")
    
    # Step 3: 印出所有 table 的完整內容
    tables = page.query_selector_all("table")
    print(f"\nStep 3: 找到 {len(tables)} 個 table")
    for ti, t in enumerate(tables):
        text = t.inner_text().strip()
        if text:
            print(f"\n  Table {ti}:")
            rows = t.query_selector_all("tr")
            print(f"  共 {len(rows)} 行")
            for ri, row in enumerate(rows):
                cells = row.query_selector_all("td, th")
                cell_texts = [c.inner_text().strip() for c in cells]
                print(f"    [{ri}] {cell_texts}")
    
    # Step 4: 用 JS 抓所有 aria-label 含星期或複製營業的元素
    print("\nStep 4: aria-label 含星期或營業時間")
    aria_elements = page.evaluate("""
    () => {
        const all = document.querySelectorAll('*');
        const found = [];
        for (const el of all) {
            const aria = el.getAttribute('aria-label') || '';
            if (aria.includes('星期') || aria.includes('複製營業')) {
                found.push(aria);
            }
        }
        return found;
    }
    """)
    for a in aria_elements:
        print(f"  {a}")
    
    # Step 5: 抓整頁所有文字，搜尋星期一到星期日
    print("\nStep 5: 整頁搜尋星期")
    content = page.inner_text("body")
    lines = content.split("\n")
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        for day in ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]:
            if day in line:
                print(f"  [{i}] {line}")
                break
    
    # Step 6: 截圖看頁面狀態
    page.screenshot(path=r"C:\Users\USER\.openclaw\workspace\nova-pages\scripts\maps_detail_screenshot.png", full_page=True)
    print("\n截圖已存檔")
    
    browser.close()