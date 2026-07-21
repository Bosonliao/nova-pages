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
    
    # 嘗試點擊「已打烊」或「營業時間」按鈕展開
    try:
        page.click("text=已打烊", timeout=5000)
        time.sleep(2)
        print("點了「已打烊」")
    except:
        print("找不到「已打烊」按鈕")
    
    # 截取展開後的內容
    content = page.inner_text("body")
    lines = content.split("\n")
    
    print("\n=== 展開後內容 ===")
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or len(line) > 100:
            continue
        if any(k in line for k in ["星期", "週一", "週二", "週三", "週四", "週五", "週六", "週日", "營業", "休息", "公休", "打烊", "開始"]):
            print(f"  [{i}] {line}")
    
    # 也試用 aria-label 找營業時間表格
    print("\n=== 搜尋 aria 標籤 ===")
    try:
        elements = page.query_selector_all("[aria-label*='營業'], [aria-label*='hour'], [aria-label*='open']")
        for el in elements:
            print(f"  aria: {el.get_attribute('aria-label')}")
            print(f"  text: {el.inner_text()[:200]}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # 試試找所有 button 和 role=button
    print("\n=== 按鈕 ===")
    try:
        buttons = page.query_selector_all("button, [role='button']")
        for btn in buttons:
            text = btn.inner_text().strip()
            if text and len(text) < 50 and any(k in text for k in ["營業", "時間", "hour", "已打烊"]):
                print(f"  button: {text}")
    except:
        pass
    
    browser.close()