"""
從 Google Maps 的 JS 回應裡搜尋營業時間資料
"""
import time
import sys
import io
import re
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

captured_bodies = []

def handle_response(response):
    url = response.url
    try:
        if "google.com/maps" in url and response.request.resource_type == "script":
            body = response.text()
            if any(k in body for k in ["星期一", "星期二", "星期三", "opening", "opening_hours"]):
                captured_bodies.append({"url": url[:100], "size": len(body), "body": body})
    except:
        pass

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.on("response", handle_response)
    
    page.goto("https://www.google.com/maps/search/光嶼咖啡+楊梅", wait_until="domcontentloaded", timeout=15000)
    time.sleep(8)
    
    # 點「已打烊」
    try:
        page.click("text=已打烊", timeout=5000)
        time.sleep(3)
    except:
        pass
    
    # 點「顯示本週營業時間」
    try:
        page.click("[aria-label='顯示本週營業時間']", timeout=5000)
        time.sleep(5)
    except:
        pass
    
    print(f"攔截到 {len(captured_bodies)} 個含營業時間的 JS 回應")
    
    for i, resp in enumerate(captured_bodies):
        print(f"\n=== Response {i} (size: {resp['size']}) ===")
        body = resp['body']
        
        # 搜尋星期一到星期日
        for day in ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]:
            if day in body:
                idx = body.index(day)
                context = body[max(0,idx-30):idx+100]
                print(f"  {day}: {context}")
        
        # 搜尋 opening_hours 或類似 JSON 結構
        for pattern in ["opening_hours", "openingHour", "openHours", "weekday", "weekday_text"]:
            if pattern in body:
                idx = body.index(pattern)
                context = body[max(0,idx-20):idx+200]
                print(f"  {pattern}: {context}")
    
    # 也從 page DOM 裡找所有隱藏的營業時間資料
    print("\n=== 從 DOM 找隱藏資料 ===")
    hidden = page.evaluate("""
    () => {
        const result = [];
        // 找所有 aria-label 含星期幾的元素（包括隱藏的）
        const all = document.querySelectorAll('[aria-label]');
        for (const el of all) {
            const aria = el.getAttribute('aria-label') || '';
            if (aria.includes('星期') || aria.includes('營業時間')) {
                const visible = el.offsetParent !== null;
                result.push({aria, visible, text: el.textContent.trim().substring(0, 50)});
            }
        }
        return result;
    }
    """)
    for h in hidden:
        print(f"  visible={h['visible']}, aria={h['aria']}, text={h['text']}")
    
    browser.close()