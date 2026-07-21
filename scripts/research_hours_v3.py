"""
方法：攔截 Google Maps 內部 API 請求，抓取營業時間 JSON
"""
import time
import sys
import io
import json
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

api_responses = []

def handle_response(response):
    url = response.url
    if "search" in url and "google" in url:
        try:
            body = response.text()
            if "opening" in body.lower() or "hour" in body.lower() or "星期" in body or "營業" in body:
                api_responses.append({"url": url[:200], "body": body[:5000]})
        except:
            pass

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # 監聽所有回應
    page.on("response", handle_response)
    
    page.goto("https://www.google.com/maps/search/光嶼咖啡+楊梅", wait_until="networkidle", timeout=30000)
    time.sleep(5)
    
    # 點「已打烊」
    try:
        page.click("text=已打烊", timeout=5000)
        time.sleep(2)
    except:
        pass
    
    # 點「顯示本週營業時間」
    try:
        page.click("[aria-label='顯示本週營業時間']", timeout=5000)
        time.sleep(5)
    except:
        pass
    
    print(f"攔截到 {len(api_responses)} 個含營業時間資訊的回應")
    
    for i, resp in enumerate(api_responses):
        print(f"\n=== Response {i} ===")
        print(f"URL: {resp['url']}")
        # 搜尋星期相關內容
        body = resp['body']
        for day in ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]:
            if day in body:
                idx = body.index(day)
                print(f"  找到 {day}: ...{body[max(0,idx-20):idx+50]}...")
    
    # 也試試直接從 page 的內部資料結構抓
    print("\n=== 嘗試從 JS 內部資料抓 ===")
    js_result = page.evaluate("""
    () => {
        // Google Maps 內部可能把資料存在 window 或某個全域變數
        const result = [];
        
        // 搜尋所有 script 標籤
        const scripts = document.querySelectorAll('script');
        for (const s of scripts) {
            const text = s.textContent || '';
            if (text.includes('星期') || text.includes('opening_hour')) {
                result.push(text.substring(0, 500));
            }
        }
        
        // 也搜尋頁面上所有文字節點
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );
        const texts = [];
        let node;
        while (node = walker.nextNode()) {
            const t = node.textContent.trim();
            if (t.includes('星期') && t.length < 50) {
                texts.push(t);
                // 也抓 parent 的 HTML
                if (node.parentElement) {
                    texts.push("parent: " + node.parentElement.outerHTML.substring(0, 200));
                }
            }
        }
        result.push(...texts);
        return result;
    }
    """)
    for r in js_result:
        print(f"  {r}")
    
    browser.close()