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
        time.sleep(3)
    except:
        print("找不到已打烊按鈕")
    
    # 用 JavaScript 直接抓所有包含星期或時間的文字
    result = page.evaluate("""
    () => {
        const all = document.querySelectorAll('*');
        const found = [];
        for (const el of all) {
            const text = el.textContent.trim();
            const aria = el.getAttribute('aria-label') || '';
            if ((text.includes('星期') || aria.includes('星期') || aria.includes('週')) && text.length < 100) {
                found.push({tag: el.tagName, text: text, aria: aria});
            }
        }
        return found;
    }
    """)
    
    print("=== DOM 中所有星期相關元素 ===")
    for item in result:
        print(f"  tag={item['tag']}, text={item['text']}, aria={item['aria']}")
    
    # 也試試抓 table 元素
    tables = page.query_selector_all("table")
    print(f"\n=== 找到 {len(tables)} 個 table ===")
    for t in tables:
        text = t.inner_text().strip()
        if text:
            print(f"  table: {text[:300]}")
    
    # 也試試 aria-label 含 "複製" 的
    print("\n=== aria 含複製 ===")
    elements = page.query_selector_all("[aria-label*='複製']")
    for el in elements:
        aria = el.get_attribute('aria-label')
        print(f"  aria: {aria}")
    
    browser.close()