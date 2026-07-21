import time
import sys
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # 搜尋光嶼咖啡
    page.goto("https://www.google.com/maps/search/光嶼咖啡+楊梅", wait_until="domcontentloaded", timeout=15000)
    time.sleep(3)
    
    # 點擊店家名稱進入詳情頁
    try:
        page.click("text=光嶼咖啡", timeout=5000)
        time.sleep(3)
    except:
        print("無法點進詳情頁")
    
    # 截取完整頁面
    content = page.inner_text("body")
    lines = content.split("\n")
    
    print("=== 詳情頁完整內容 ===")
    for i, line in enumerate(lines):
        line = line.strip()
        if line and len(line) < 100:
            # 找星期相關的行和前後行
            if any(k in line for k in ["星期", "週", "營業", "休息", "公休", "已打烊", "營業中", "開始營業", "打烊"]):
                print(f"  [{i}] {line}")
                # 印前後各一行
                if i > 0 and lines[i-1].strip() and len(lines[i-1].strip()) < 100:
                    print(f"  [{i-1}] {lines[i-1].strip()}")
                if i+1 < len(lines) and lines[i+1].strip() and len(lines[i+1].strip()) < 100:
                    print(f"  [{i+1}] {lines[i+1].strip()}")
    
    # 也試試直接截取所有文字看有沒有星期一到星期日
    print("\n=== 搜尋星期關鍵字 ===")
    for i, line in enumerate(lines):
        line = line.strip()
        if any(k in line for k in ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]):
            print(f"  [{i}] {line}")
            if i+1 < len(lines) and lines[i+1].strip():
                print(f"  [{i+1}] {lines[i+1].strip()}")
    
    browser.close()