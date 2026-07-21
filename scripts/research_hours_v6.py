"""
用非 headless 模式開瀏覽器，看是否能抓到完整營業時間
"""
import time
import sys
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with sync_playwright() as p:
    # headless=False 開真實瀏覽器視窗
    browser = p.chromium.launch(headless=False, args=["--window-position=-2000,0"])  # 放到螢幕外
    page = browser.new_page()
    
    page.goto("https://www.google.com/maps/search/光嶼咖啡+楊梅", wait_until="domcontentloaded", timeout=15000)
    time.sleep(5)
    
    # 點「已打烊」
    try:
        page.click("text=已打烊", timeout=5000)
        time.sleep(3)
        print("點了「已打烊」")
    except:
        print("找不到「已打烊」")
    
    # 點「顯示本週營業時間」
    try:
        page.click("[aria-label='顯示本週營業時間']", timeout=5000)
        time.sleep(5)
        print("點了「顯示本週營業時間」")
    except:
        print("找不到「顯示本週營業時間」")
    
    # 抓 table
    tables = page.query_selector_all("table")
    print(f"\n找到 {len(tables)} 個 table")
    for t in tables:
        text = t.inner_text().strip()
        if "星期" in text:
            print(f"\n=== 營業時間表 ===")
            rows = t.query_selector_all("tr")
            print(f"共 {len(rows)} 行")
            for row in rows:
                cells = row.query_selector_all("td, th")
                cell_texts = [c.inner_text().strip() for c in cells]
                print(f"  {' | '.join(cell_texts)}")
    
    # JS 搜尋所有星期
    print("\n=== JS 搜尋星期 ===")
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
    
    browser.close()