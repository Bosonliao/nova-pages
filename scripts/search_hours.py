"""
批次查詢餐廳營業時間 — 使用 web_search 搜尋結果 snippet
方法：搜尋「{店名} {區} 營業時間」，從結果 snippet 提取營業時間資訊
優點：免費、不需要 API、能拿到完整週營業時間
"""
import csv
import time
import re
import sys
import io
import json
import urllib.request
import urllib.parse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CSV_PATH = r'C:\Users\USER\.openclaw\workspace\nova-pages\data\restaurants.csv'

def search_hours(query):
    """用 DuckDuckGo HTML 搜尋，從 snippet 提取營業時間"""
    url = "https://html.duckduckgo.com/html/"
    data = urllib.parse.urlencode({"q": query}).encode()
    try:
        req = urllib.request.Request(url, data=data, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8')
        
        # 提取 snippet 文字
        snippets = re.findall(r'class="result__snippet">(.*?)</a>', html, re.DOTALL)
        clean_snippets = []
        for s in snippets:
            clean = re.sub(r'<[^>]+>', '', s).strip()
            if clean:
                clean_snippets.append(clean)
        
        # 從 snippets 裡找營業時間
        hours_info = ""
        for snippet in clean_snippets:
            # 搜尋營業時間相關關鍵字
            if any(k in snippet for k in ["營業", "公休", "11:30", "18:00", "星期", "週一", "週二", "週三", "週四", "週五", "週六", "週日"]):
                hours_info = snippet
                break
        
        return hours_info[:200] if hours_info else ""
    except Exception as e:
        return ""

def extract_hours_from_snippet(snippet):
    """從 snippet 文字裡提取結構化營業時間"""
    if not snippet:
        return ""
    
    # 找「XX:XX至XX:XX」或「XX:XX-XX:XX」格式
    time_pattern = re.findall(r'(\d{1,2}:\d{2})\s*(?:至|-|~|到)\s*(\d{1,2}:\d{2})', snippet)
    
    # 找公休日
    holiday = ""
    if "公休" in snippet or "休" in snippet:
        holiday_match = re.search(r'(?:公休|休息)[：:為]?(每週[一二三四五六日]|[週周][一二三四五六日])', snippet)
        if holiday_match:
            holiday = holiday_match.group(1)
    
    # 找星期幾的營業時間
    days_hours = {}
    day_pattern = re.findall(r'(星期[一二三四五六日]|[週周][一二三四五六日])\s*(\d{1,2}:\d{2})\s*(?:至|-|~|到)\s*(\d{1,2}:\d{2})', snippet)
    for day, start, end in day_pattern:
        days_hours[day] = f"{start}-{end}"
    
    # 組合結果
    parts = []
    if time_pattern:
        start, end = time_pattern[0]
        parts.append(f"{start}-{end}")
    if holiday:
        parts.append(f"{holiday}公休")
    if days_hours:
        for day, hours in days_hours.items():
            parts.append(f"{day} {hours}")
    
    return "；".join(parts) if parts else snippet[:100]

def main():
    rows = []
    with open(CSV_PATH, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        for row in reader:
            rows.append(row)
    
    # 篩出楊梅區缺營業時間的（作為測試）
    targets = [r for r in rows if r.get('county','') == '桃園' and r.get('district','') == '楊梅區' and not r.get('business_hours','').strip()]
    
    # 如果楊梅都已有，取前 10 筆缺的
    if not targets:
        targets = [r for r in rows if not r.get('business_hours','').strip()][:10]
    
    print(f"待查: {len(targets)} 筆")
    
    for i, row in enumerate(targets):
        name = row.get('name', '')
        district = row.get('district', '')
        county = row.get('county', '')
        query = f"{name} {district} 營業時間"
        
        print(f"[{i+1}/{len(targets)}] {name} ({district})")
        
        snippet = search_hours(query)
        if snippet:
            hours = extract_hours_from_snippet(snippet)
            print(f"  snippet: {snippet[:100]}")
            print(f"  extracted: {hours}")
            row['business_hours'] = hours
        else:
            print(f"  查不到")
        
        time.sleep(2)
    
    # 寫回 CSV
    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    found = sum(1 for r in targets if r.get('business_hours','').strip())
    print(f"\n完成！{found}/{len(targets)} 筆成功")

if __name__ == "__main__":
    main()