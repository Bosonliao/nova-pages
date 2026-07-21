"""
Google Maps 完整營業時間 — 加大 viewport + 捲動側邊欄 + 更長等待
"""
import time
import sys
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # 加大 viewport 模擬桌面瀏覽器
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    
    page.goto("https://www.google.com/maps?cid=0x346823c67dab675f:0xba9c838c8f44a362", wait_until="domcontentloaded", timeout=15000)
    time.sleep(8)
    
    # 點「已打烊」
    try:
        page.click("text=已打烊", timeout=5000)
        time.sleep(3)
        print("點了「已打烊」")
    except:
        print("找不到「已打烊」")
    
    # 向下捲動側邊欄
    print("\n=== 捲動側邊欄 ===")
    for scroll in range(5):
        page.evaluate("document.querySelector('[role=main]')?.scrollBy(0, 300)")
        time.sleep(1)
    
    # 抓 table
    tables = page.query_selector_all("table")
    print(f"\n找到 {len(tables)} 個 table")
    for t in tables:
        text = t.inner_text().strip()
        if "星期" in text:
            rows = t.query_selector_all("tr")
            print(f"營業時間表: {len(rows)} 行")
            for row in rows:
                cells = row.query_selector_all("td, th")
                cell_texts = [c.inner_text().strip() for c in cells]
                print(f"  {' | '.join(cell_texts)}")
    
    # JS 搜尋所有星期
    print("\n=== JS 搜尋所有星期 ===")
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
    
    # 截圖
    page.screenshot(path=r"C:\Users\USER\.openclaw\workspace\nova-pages\scripts\big_viewport_screenshot.png", full_page=True)
    print("\n截圖已存")
    
    browser.close()