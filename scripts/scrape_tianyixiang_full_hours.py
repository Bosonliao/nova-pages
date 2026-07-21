"""
方案 A: Playwright + headless=False + 精準點擊展開 + 視覺模型分析
目標：從 Google Maps 獲取完整週營業時間表 (以天一香肉羹順為例)
"""
import time
import sys
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 天一香肉羹順 的 Google Maps CID
tianyixiang_cid = "0x346d5c635b7501a1:0xa5f46399c0b297d0"
tianyixiang_name = "天一香肉羹順"

with sync_playwright() as p:
    # headless=False，並將視窗移到螢幕外，避免干擾
    browser = p.chromium.launch(headless=False, args=["--window-position=-2000,0"])
    page = browser.new_page(viewport={"width": 1280, "height": 800}) # 設定適當的 viewport
    
    # 訪問 Google Maps CID URL
    url = f"https://www.google.com/maps?cid={tianyixiang_cid}"
    print(f"訪問 URL: {url}")
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(10) # 等待頁面完全載入
    
    # 嘗試點擊營業時間區塊來展開
    # 這裡可以嘗試多種選擇器，例如包含「營業時間」文字的 div 或 span，或者向下箭頭圖案
    # 根據你的截圖，有一個向下箭頭在「營業時間: 週一00:00」旁邊
    print("\n嘗試點擊營業時間展開按鈕...")
    try:
        # 找到包含「營業時間」文字的父元素，然後點擊其中的展開箭頭
        # 由於箭頭可能不是獨立元素，先點擊包含營業時間文字的區域
        page.click("div:has-text('營業時間')", timeout=5000)
        time.sleep(3)
        
        # 再次嘗試點擊向下箭頭
        page.click("[aria-label*='顯示'][aria-label*='營業時間']", timeout=5000)
        time.sleep(5) # 再次等待展開
        print("成功點擊展開按鈕")
    except Exception as e:
        print(f"點擊展開按鈕失敗: {e}")
    
    # 捲動側邊欄，確保所有內容都已載入和顯示
    print("\n捲動側邊欄...")
    scrollable_selector = "[role='main'] div[tabindex='-1']"
    for _ in range(3):
        try:
            page.evaluate(f"document.querySelector('{scrollable_selector}').scrollBy(0, 500)")
            time.sleep(1)
        except: # 如果選擇器不對，嘗試捲動 body
            page.evaluate("document.body.scrollBy(0, 500)")
            time.sleep(1)
    
    # 截圖
    screenshot_path = r"C:\Users\USER\.openclaw\workspace\nova-pages\scripts\tianyixiang_full_hours.png"
    page.screenshot(path=screenshot_path, full_page=True)
    print(f"\n截圖已存檔: {screenshot_path}")
    
    browser.close()
    
    print("\n--- 視覺模型分析截圖 --- ")
    # 使用 image 工具分析截圖，提取營業時間
    # 這裡只呼叫工具，實際分析會在下一個 turn 執行
    print(f"請使用 image 工具分析 {screenshot_path} 並提取營業時間")