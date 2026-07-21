import csv
import time
import sys
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CSV_PATH = r'C:\Users\USER\.openclaw\workspace\nova-pages\data\restaurants.csv'

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
            if any(k in line for k in ["營業", "時間", "星期", "週", "已打烊", "營業中", "開始營業", "打烊時間"]):
                # 過濾掉太長的行（可能是部落格文章）
                if len(line) < 100:
                    hours_lines.append(line)
        return "; ".join(hours_lines[:3]) if hours_lines else ""
    except Exception as e:
        return ""

def main():
    rows = []
    with open(CSV_PATH, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        for row in reader:
            rows.append(row)
    
    # 篩出楊梅區缺營業時間的
    targets = [r for r in rows if r.get('county','') == '桃園' and r.get('district','') == '楊梅區' and not r.get('business_hours','').strip()]
    print(f"楊梅區缺營業時間: {len(targets)}筆")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for i, row in enumerate(targets):
            name = row.get('name', '')
            query = f"{name} 楊梅"
            print(f"[{i+1}/{len(targets)}] {name}")
            hours = scrape_hours(page, query)
            if hours:
                print(f"  -> {hours}")
                row['business_hours'] = hours
            else:
                print(f"  -> 查不到")
            time.sleep(3)
        
        browser.close()
    
    # 寫回 CSV
    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    found = sum(1 for r in targets if r.get('business_hours','').strip())
    print(f"\n完成！{found}/{len(targets)} 筆成功")

if __name__ == "__main__":
    main()