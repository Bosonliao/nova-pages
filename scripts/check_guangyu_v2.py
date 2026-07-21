import time
import sys
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Google Maps 完整頁面截取
    page.goto("https://www.google.com/maps/search/光嶼咖啡+楊梅", wait_until="domcontentloaded", timeout=15000)
    time.sleep(4)
    
    # 截取完整頁面文字
    content = page.inner_text("body")
    lines = content.split("\n")
    
    # 找星期一到星期日的營業時間
    print("=== 完整頁面資訊 ===")
    capture = False
    for i, line in enumerate(lines):
        line = line.strip()
        if "星期" in line or "週" in line or "營業" in line or "休息" in line or "已打烊" in line or "公休" in line:
            capture = True
            print(f"  {line}")
            # 也印下一行
            if i+1 < len(lines) and lines[i+1].strip():
                print(f"    next: {lines[i+1].strip()}")
    
    browser.close()