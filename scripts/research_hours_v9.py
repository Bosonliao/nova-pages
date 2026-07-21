"""
直接從 Google Maps 頁面的 JavaScript 裡抓內部資料
Google Maps 會在 window 物件或 script 標籤裡初始化店家資料
"""
import time
import sys
import io
import re
import json
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.goto("https://www.google.com/maps?cid=0x346823c67dab675f:0xba9c838c8f44a362", wait_until="domcontentloaded", timeout=15000)
    time.sleep(8)
    
    # 方法 1: 從所有 script 標籤裡找營業時間 JSON
    print("=== 方法 1: Script 標籤搜尋 ===")
    scripts = page.evaluate("""
    () => {
        const scripts = document.querySelectorAll('script');
        const found = [];
        for (const s of scripts) {
            const text = s.textContent || '';
            // 搜尋包含多天營業時間的資料
            if (text.includes('11:30') && text.includes('18:00')) {
                // 找 11:30 和 18:00 附近的內容
                const idx = text.indexOf('11:30');
                if (idx >= 0) {
                    found.push(text.substring(Math.max(0, idx - 200), idx + 500));
                }
            }
        }
        return found;
    }
    """)
    for s in scripts:
        print(f"  {s[:500]}")
    
    # 方法 2: 搜尋頁面 HTML 原始碼裡的營業時間
    print("\n=== 方法 2: HTML 原始碼搜尋 ===")
    html = page.content()
    # 搜尋 "11:30" 出現的所有位置
    positions = [m.start() for m in re.finditer("11:30", html)]
    print(f"找到 {len(positions)} 處 11:30")
    for pos in positions[:5]:
        context = html[max(0,pos-100):pos+100]
        # 清理換行
        context = context.replace("\n", " ")
        print(f"  ...{context}...")
    
    # 方法 3: 搜尋 "星期一" 在 HTML 裡
    print("\n=== 方法 3: HTML 搜尋星期一 ===")
    monday_positions = [m.start() for m in re.finditer("星期一", html)]
    print(f"找到 {len(monday_positions)} 處星期一")
    for pos in monday_positions[:3]:
        context = html[max(0,pos-50):pos+100]
        context = context.replace("\n", " ")
        print(f"  ...{context}...")
    
    # 方法 4: 搜尋 "週一" 在 HTML 裡
    print("\n=== 方法 4: HTML 搜尋週一 ===")
    mon_positions = [m.start() for m in re.finditer("週一", html)]
    print(f"找到 {len(mon_positions)} 處週一")
    for pos in mon_positions[:3]:
        context = html[max(0,pos-50):pos+100]
        context = context.replace("\n", " ")
        print(f"  ...{context}...")
    
    # 方法 5: 搜尋 "11:30" 和 "18:00" 同時出現的 JSON 結構
    print("\n=== 方法 5: JSON 結構搜尋 ===")
    # 找包含 11:30 的 JSON 物件
    json_patterns = re.findall(r'\{[^}]*11:30[^}]*\}', html)
    for jp in json_patterns[:3]:
        print(f"  {jp[:300]}")
    
    browser.close()