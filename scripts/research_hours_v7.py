"""
方法：先搜尋取得 place URL，再訪問 place 詳情頁
"""
import time
import sys
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Step 1: 搜尋取得 place URL
    page.goto("https://www.google.com/maps/search/光嶼咖啡+楊梅", wait_until="domcontentloaded", timeout=15000)
    time.sleep(5)
    
    current_url = page.url
    print(f"當前 URL: {current_url}")
    
    # 點進店家名稱
    try:
        page.click("text=光嶼咖啡", timeout=5000)
        time.sleep(5)
    except:
        print("無法點進店家")
    
    # 取得 place 詳情 URL
    place_url = page.url
    print(f"Place URL: {place_url}")
    
    # Step 2: 在 place 詳情頁找營業時間
    # 點「已打烊」
    try:
        page.click("text=已打烊", timeout=5000)
        time.sleep(2)
    except:
        try:
            page.click("text=營業中", timeout=3000)
            time.sleep(2)
        except:
            pass
    
    # 點「顯示本週營業時間」
    try:
        page.click("[aria-label='顯示本週營業時間']", timeout=5000)
        time.sleep(3)
    except:
        pass
    
    # 抓 table
    tables = page.query_selector_all("table")
    print(f"\n找到 {len(tables)} 個 table")
    for t in tables:
        text = t.inner_text().strip()
        if "星期" in text:
            rows = t.query_selector_all("tr")
            print(f"營業時間表共 {len(rows)} 行:")
            for row in rows:
                cells = row.query_selector_all("td, th")
                cell_texts = [c.inner_text().strip() for c in cells]
                print(f"  {' | '.join(cell_texts)}")
    
    # JS 搜尋所有星期
    print("\n=== JS 搜尋 ===")
    js_result = page.evaluate("""
    () => {
        const walker = document.createTreeWalker(
            document.body, NodeFilter.SHOW_TEXT, null, false
        );
        const texts = [];
        let node;
        while (node = walker.nextNode()) {
            const t = node.textContent.trim();
            if (t.includes('星期') && t.length < 30) {
                texts.push(t);
            }
        }
        return texts;
    }
    """)
    for t in js_result:
        print(f"  {t}")
    
    # 也截圖
    page.screenshot(path=r"C:\Users\USER\.openclaw\workspace\nova-pages\scripts\place_detail_screenshot.png", full_page=True)
    print("\n截圖已存檔")
    
    browser.close()