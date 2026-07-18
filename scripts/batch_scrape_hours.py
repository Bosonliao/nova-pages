"""
批次爬取 Google Maps 營業時間
使用 Playwright，不需要 LLM，不需要 API
"""
import csv
import json
import time
import re
import sys
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

INPUT_CSV = r'C:\Users\USER\.openclaw\workspace\nova-pages\data\restaurants.csv'
OUTPUT_CSV = r'C:\Users\USER\.openclaw\workspace\nova-pages\data\restaurants_with_hours.csv'
BATCH_SIZE = 50  # 每次跑 50 筆，避免被封
DELAY = 3  # 每筆間隔 3 秒

def scrape_hours(page, query):
    try:
        url = f"https://www.google.com/maps/search/{query}"
        page.goto(url, wait_until="domcontentloaded", timeout=15000)
        time.sleep(2)
        content = page.inner_text("body")
        lines = content.split("\n")
        
        hours_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # 找營業時間相關行
            if any(k in line for k in ["營業", "時間", "星期", "週", "已打烊", "營業中", "開始營業", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]):
                hours_lines.append(line)
        
        return "; ".join(hours_lines[:5]) if hours_lines else ""
    except Exception as e:
        print(f"  Error: {e}")
        return ""

def main():
    # 讀取 CSV
    rows = []
    with open(INPUT_CSV, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        for row in reader:
            rows.append(row)
    
    if 'business_hours' not in fieldnames:
        fieldnames.append('business_hours')
    
    # 找出缺 business_hours 的筆數
    missing = [r for r in rows if not r.get('business_hours') or r.get('business_hours').strip() == '']
    print(f"總共 {len(rows)} 筆，缺營業時間 {len(missing)} 筆")
    print(f"本次處理前 {BATCH_SIZE} 筆")
    
    to_process = missing[:BATCH_SIZE]
    if not to_process:
        print("全部都有營業時間了！")
        return
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for i, row in enumerate(to_process):
            name = row.get('name', '')
            county = row.get('county', '')
            district = row.get('district', '')
            query = f"{name} {county}{district}"
            
            print(f"[{i+1}/{len(to_process)}] {name} ({county})")
            
            hours = scrape_hours(page, query)
            if hours:
                print(f"  -> {hours}")
                row['business_hours'] = hours
            else:
                print(f"  -> 查不到")
                row['business_hours'] = ''
            
            time.sleep(DELAY)
        
        browser.close()
    
    # 寫回 CSV
    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    found = sum(1 for r in to_process if r.get('business_hours'))
    print(f"\n完成！本次查到 {found}/{len(to_process)} 筆營業時間")
    print(f"結果寫入: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()