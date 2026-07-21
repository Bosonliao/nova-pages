import time
import sys
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def scrape_full_hours(page, query):
    page.goto(f"https://www.google.com/maps/search/{query}", wait_until="domcontentloaded", timeout=15000)
    time.sleep(4)
    
    # 點「已打烊」展開營業時間
    try:
        page.click("text=已打烊", timeout=5000)
        time.sleep(2)
    except:
        try:
            page.click("text=營業中", timeout=3000)
            time.sleep(2)
        except:
            pass
    
    # 用 aria 標籤抓每日營業時間
    hours = []
    try:
        elements = page.query_selector_all("[aria-label*='星期'], [aria-label*='週']")
        for el in elements:
            label = el.get_attribute('aria-label') or ''
            if '星期' in label or '週' in label:
                hours.append(label)
    except:
        pass
    
    return hours

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # 測試光嶼咖啡
    print("=== 光嶼咖啡 ===")
    hours = scrape_full_hours(page, "光嶼咖啡 楊梅")
    for h in hours:
        print(f"  {h}")
    
    if not hours:
        print("  查不到完整營業時間")
    
    # 測試 50嵐
    print("\n=== 50嵐 楊梅 ===")
    hours = scrape_full_hours(page, "50嵐 楊梅")
    for h in hours:
        print(f"  {h}")
    
    if not hours:
        print("  查不到完整營業時間")
    
    browser.close()