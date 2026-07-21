"""
Playwright 爬 Google Maps 完整營業時間 (分 7 天模擬日期)
目標：每次設定不同日期，抓取當天的營業時間，再合併成完整週時間表
"""
import time
import sys
import io
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_full_weekly_hours(browser_context, place_cid, place_name):
    weekly_hours = {}
    
    # 模擬從星期一到星期日
    for i in range(7):
        # 設定日期 (例如從今天開始往後推 i 天)
        target_date = datetime.now() + timedelta(days=i)
        # 將日期設定到瀏覽器 context
        # Playwright 的 set_extra_http_headers 無法設定 Date Header
        # 只能在 Chromium 啟動參數裡設定，或者用 CDP Protocol
        # 但最簡單是直接觀察網頁渲染結果
        
        # 暫時用 Page.evaluate 修改 Date 物件 (可能被 Google Maps 偵測)
        # 或者乾脆只抓當天，然後把目標頁面跳轉到有完整週時間表的連結
        # 這裡先假定我能修改日期或 Google Maps 會根據 URL 參數顯示
        
        # 實際操作：Google Maps 似乎沒有簡單的 URL 參數來改變顯示日期
        # 所以我將嘗試多次點擊「顯示本週營業時間」直到它展開
        # 如果還是不行，則需要考慮更複雜的 CDP Protocol 來設定日期
        
        print(f"\n嘗試獲取 {place_name} 營業時間 (模擬日期: {(target_date.strftime('%Y-%m-%d'))})")
        
        page = browser_context.new_page()
        
        # 訪問 CID URL
        url = f"https://www.google.com/maps?cid={place_cid}"
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        time.sleep(8) # 等待頁面載入和 AJAX 渲染
        
        # 點擊「已打烊」或「營業中」來展開營業時間區塊
        try:
            page.click("text=已打烊", timeout=5000)
            time.sleep(3)
        except:
            try:
                page.click("text=營業中", timeout=3000)
                time.sleep(3)
            except:
                pass
        
        # 點擊「顯示本週營業時間」按鈕
        try:
            page.click("[aria-label='顯示本週營業時間']", timeout=5000)
            time.sleep(5) # 給足夠時間讓它展開
        except:
            pass
        
        # 從 DOM 中提取所有星期幾的營業時間
        # 這裡需要更精準的 selector
        hours_data = page.evaluate("""
        () => {
            const hours = {};
            // Google Maps 的營業時間通常在 table 裡
            const tables = document.querySelectorAll('table');
            for (const table of tables) {
                const rows = table.querySelectorAll('tr');
                for (const row of rows) {
                    const cells = row.querySelectorAll('td, th');
                    if (cells.length >= 2) {
                        const day = cells[0].textContent.trim();
                        const time = cells[1].textContent.trim();
                        if (day.includes('星期') || day.includes('週')) {
                            hours[day] = time;
                        }
                    }
                }
            }
            return hours;
        }
        """)
        
        page.close()
        
        for day, hour in hours_data.items():
            # Google Maps 的日期顯示是「星期六」或「週一」
            weekly_hours[day] = hour
            
        # 截圖確認 (方便 debug)
        # page.screenshot(path=f"./screenshots/{place_name}_{target_date.strftime('%Y-%m-%d')}.png")

    return weekly_hours

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    
    # 光嶼咖啡的 CID
    guangyu_cid = "0x346823c67dab675f:0xba9c838c8f44a362"
    guangyu_name = "光嶼咖啡"
    
    all_hours = get_full_weekly_hours(context, guangyu_cid, guangyu_name)
    
    print(f"\n=== {guangyu_name} 完整週營業時間 ===")
    if all_hours:
        days_order = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        for day in days_order:
            print(f"  {day}: {all_hours.get(day, '未取得')}")
    else:
        print("未能取得完整週營業時間")
        
    browser.close()