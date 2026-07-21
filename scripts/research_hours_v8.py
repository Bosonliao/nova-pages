"""
最後一招：用 Google Maps CID URL + Playwright，而且用 page.wait_for_selector 等待營業時間表完全載入
"""
import time
import sys
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # 用 CID URL 直接訪問 place 頁面
    url = "https://www.google.com/maps?cid=0x346823c67dab675f:0xba9c838c8f44a362"
    page.goto(url, wait_until="domcontentloaded", timeout=15000)
    time.sleep(8)
    
    print(f"URL: {page.url}")
    
    # 等待營業時間元素出現
    try:
        page.wait_for_selector("text=已打烊", timeout=10000)
        print("找到「已打烊」")
    except:
        try:
            page.wait_for_selector("text=營業中", timeout=5000)
            print("找到「營業中」")
        except:
            print("找不到營業狀態")
    
    # 點「已打烊」展開
    try:
        page.click("text=已打烊", timeout=5000)
        time.sleep(2)
    except:
        pass
    
    # 用 JS 找「顯示本週營業時間」並點擊
    clicked = page.evaluate("""
    () => {
        const els = document.querySelectorAll('[aria-label]');
        for (const el of els) {
            const aria = el.getAttribute('aria-label') || '';
            if (aria.includes('顯示') && aria.includes('營業')) {
                el.click();
                return aria;
            }
        }
        return false;
    }
    """)
    print(f"展開按鈕: {clicked}")
    time.sleep(3)
    
    # 再用 JS 找「顯示本週營業時間」第二次點擊
    clicked2 = page.evaluate("""
    () => {
        const els = document.querySelectorAll('[aria-label]');
        for (const el of els) {
            const aria = el.getAttribute('aria-label') || '';
            if (aria.includes('顯示') && aria.includes('營業')) {
                el.click();
                return aria;
            }
        }
        return false;
    }
    """)
    print(f"第二次展開: {clicked2}")
    time.sleep(3)
    
    # 抓 table 所有行
    tables = page.query_selector_all("table")
    for t in tables:
        text = t.inner_text().strip()
        if "星期" in text:
            rows = t.query_selector_all("tr")
            print(f"\n營業時間表: {len(rows)} 行")
            for row in rows:
                cells = row.query_selector_all("td, th")
                cell_texts = [c.inner_text().strip() for c in cells]
                print(f"  {' | '.join(cell_texts)}")
    
    # 也用 JS 直接搜所有星期文字
    print("\n=== 所有星期文字 ===")
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
    page.screenshot(path=r"C:\Users\USER\.openclaw\workspace\nova-pages\scripts\cid_page_screenshot.png", full_page=True)
    print("\n截圖已存")
    
    browser.close()