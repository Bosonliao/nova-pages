"""
方法：攔截 Google Maps 內部 API + 更長等待 + 多次點擊展開
"""
import time
import sys
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

api_responses = []

def handle_response(response):
    url = response.url
    try:
        if "google.com/maps" in url:
            body = response.text()
            if any(k in body for k in ["星期", "opening", "hour", "營業"]):
                api_responses.append({"url": url[:150], "size": len(body)})
    except:
        pass

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.on("response", handle_response)
    
    page.goto("https://www.google.com/maps/search/光嶼咖啡+楊梅", wait_until="domcontentloaded", timeout=15000)
    time.sleep(5)
    
    print(f"攔截到 {len(api_responses)} 個含營業時間的回應")
    for r in api_responses:
        print(f"  URL: {r['url']} (size: {r['size']})")
    
    # 點「已打烊」
    try:
        page.click("text=已打烊", timeout=5000)
        time.sleep(3)
    except:
        pass
    
    # 多次嘗試展開
    for attempt in range(3):
        try:
            page.click("[aria-label='顯示本週營業時間']", timeout=3000)
            time.sleep(3)
            print(f"展開嘗試 {attempt+1} 成功")
        except:
            print(f"展開嘗試 {attempt+1} 失敗")
    
    # 再攔截
    print(f"\n點擊後攔截到 {len(api_responses)} 個回應")
    
    # 最終嘗試：用 JS 找所有包含星期幾的文字節點
    print("\n=== JS 搜尋所有星期文字 ===")
    js_result = page.evaluate("""
    () => {
        const walker = document.createTreeWalker(
            document.body, NodeFilter.SHOW_TEXT, null, false
        );
        const texts = [];
        let node;
        while (node = walker.nextNode()) {
            const t = node.textContent.trim();
            if (t.includes('星期') && t.length < 30) {
                texts.push(t);
            }
        }
        return texts;
    }
    """)
    for t in js_result:
        print(f"  {t}")
    
    # 也看看 table 的 HTML 結構
    print("\n=== Table HTML ===")
    tables = page.query_selector_all("table")
    for t in tables:
        html = t.inner_html()
        if "星期" in html or "hour" in html:
            print(html[:1000])
    
    # 最後試一招：找所有帶 data-hour 或類似屬性的元素
    print("\n=== data 屬性搜尋 ===")
    data_elements = page.evaluate("""
    () => {
        const all = document.querySelectorAll('*');
        const found = [];
        for (const el of all) {
            for (const attr of el.attributes) {
                if (attr.name.startsWith('data-') && (attr.value.includes('hour') || attr.value.includes('星期') || attr.value.includes('open'))):
                    found.push({tag: el.tagName, attr: attr.name, val: attr.value.substring(0, 100)});
                end
            }
        }
        return found;
    }
    """)
    for d in data_elements:
        print(f"  {d}")
    
    browser.close()