import time
import sys
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # 先試 Google Maps 詳細頁面
    page.goto("https://www.google.com/maps/search/光嶼咖啡+楊梅", wait_until="domcontentloaded", timeout=15000)
    time.sleep(3)
    
    # 點擊營業時間區塊
    try:
        page.click("text=已打烊", timeout=5000)
        time.sleep(2)
        content = page.inner_text("body")
        lines = content.split("\n")
        print("=== Google Maps 詳細營業時間 ===")
        for line in lines:
            line = line.strip()
            if line and len(line) < 100:
                if any(k in line for k in ["星期", "週", "營業", "公休", "休息", "關閉", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]):
                    print(f"  {line}")
    except:
        print("無法展開營業時間")
    
    # 也試 Instagram
    print("\n=== Instagram ===")
    page.goto("https://www.instagram.com/guangyu_coffee/", wait_until="domcontentloaded", timeout=15000)
    time.sleep(3)
    content = page.inner_text("body")
    lines = content.split("\n")
    for line in lines[:30]:
        line = line.strip()
        if line and len(line) < 200:
            print(f"  {line}")
    
    browser.close()