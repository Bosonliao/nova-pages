"""
研究 Google Maps 營業時間展開機制
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
    
    # 先找出所有可點擊的元素和它們的屬性
    print("=== 所有 button 和 role=button ===")
    buttons = page.evaluate("""
    () => {
        const btns = document.querySelectorAll('button, [role="button"], [aria-label]');
        const result = [];
        for (const b of btns) {
            const aria = b.getAttribute('aria-label') || '';
            const text = b.textContent.trim().substring(0, 50);
            const tag = b.tagName;
            if (aria.includes('營業') || aria.includes('星期') || aria.includes('週') || 
                text.includes('營業') || text.includes('已打烊') || text.includes('營業中') ||
                aria.includes('顯示') || aria.includes('展開')) {
                result.push({tag, aria, text});
            }
        }
        return result;
    }
    """)
    for b in buttons:
        print(f"  tag={b['tag']}, aria={b['aria']}, text={b['text']}")
    
    # 找到「已打烊」區塊，點它
    print("\n=== 點擊「已打烊」===")
    try:
        page.click("text=已打烊", timeout=5000)
        time.sleep(2)
        print("點擊成功")
    except:
        print("點擊失敗")
    
    # 點擊後再找一次所有相關按鈕
    print("\n=== 點擊後的按鈕 ===")
    buttons2 = page.evaluate("""
    () => {
        const btns = document.querySelectorAll('button, [role="button"], [aria-label]');
        const result = [];
        for (const b of btns) {
            const aria = b.getAttribute('aria-label') || '';
            const text = b.textContent.trim().substring(0, 50);
            if (aria.includes('營業') || aria.includes('星期') || aria.includes('週') || 
                aria.includes('顯示') || aria.includes('展開') || aria.includes('更多')) {
                result.push({aria, text});
            }
        }
        return result;
    }
    """)
    for b in buttons2:
        print(f"  aria={b['aria']}, text={b['text']}")
    
    # 嘗試用 JS 直接點擊「顯示本週營業時間」
    print("\n=== JS 點擊「顯示本週營業時間」===")
    clicked = page.evaluate("""
    () => {
        const el = document.querySelector("[aria-label='顯示本週營業時間']");
        if (el) {
            el.click();
            return true;
        }
        return false;
    }
    """)
    print(f"  點擊結果: {clicked}")
    time.sleep(3)
    
    # 再查 table
    print("\n=== 點擊後 table 內容 ===")
    tables = page.query_selector_all("table")
    for t in tables:
        rows = t.query_selector_all("tr")
        print(f"  table 共 {len(rows)} 行:")
        for ri, row in enumerate(rows):
            cells = row.query_selector_all("td, th")
            cell_texts = [c.inner_text().strip() for c in cells]
            print(f"    [{ri}] {cell_texts}")
    
    # 嘗試找下拉式選單的箭頭按鈕（可能是一個 img 或 svg）
    print("\n=== 尋找下拉箭頭 ===")
    arrows = page.evaluate("""
    () => {
        const all = document.querySelectorAll('img, svg, span, div');
        const result = [];
        for (const el of all) {
            const aria = el.getAttribute('aria-label') || '';
            const cls = el.className || '';
            const style = window.getComputedStyle(el);
            // 找含有 down arrow 或 expand 的元素
            if (aria.includes('down') || aria.includes('展開') || aria.includes('更多') ||
                aria.includes('expand') || aria.includes('展開營業')) {
                result.push({tag: el.tagName, aria, cls: cls.toString().substring(0, 50)});
            }
        }
        return result;
    }
    """)
    for a in arrows:
        print(f"  {a}")
    
    browser.close()