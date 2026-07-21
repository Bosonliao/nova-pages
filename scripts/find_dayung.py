import time
import sys
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def scrape(page, query):
    try:
        url = f"https://www.google.com/maps/search/{query}"
        page.goto(url, wait_until="domcontentloaded", timeout=15000)
        time.sleep(3)
        content = page.inner_text("body")
        lines = content.split("\n")
        hours_lines = []
        for line in lines:
            line = line.strip()
            if not line or len(line) > 100:
                continue
            if any(k in line for k in ["營業", "時間", "星期", "週", "已打烊", "營業中", "開始營業", "打烊時間"]):
                hours_lines.append(line)
        return "; ".join(hours_lines[:3]) if hours_lines else "查不到"
    except Exception as e:
        return f"Error: {e}"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # 嘗試不同搜尋方式
    queries = [
        "大苑子 楊梅店",
        "大苑子 桃園楊梅",
        "大苑子 楊梅區",
        "DaYung's 楊梅",
    ]
    
    for q in queries:
        print(f"搜尋: {q}")
        result = scrape(page, q)
        print(f"  -> {result}")
        print()
        time.sleep(3)
    
    browser.close()