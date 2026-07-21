"""
批次查詢餐廳營業時間 — 使用 DuckDuckGo 搜尋 snippet
V2: 改進提取邏輯，能解析多種格式
"""
import csv
import time
import re
import sys
import io
import urllib.request
import urllib.parse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CSV_PATH = r'C:\Users\USER\.openclaw\workspace\nova-pages\data\restaurants.csv'

def search_ddg(query):
    """DuckDuckGo HTML 搜尋，回傳 snippet 列表"""
    url = "https://html.duckduckgo.com/html/"
    data = urllib.parse.urlencode({"q": query}).encode()
    try:
        req = urllib.request.Request(url, data=data, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8')
        snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
        result = []
        for s in snippets:
            clean = re.sub(r'<[^>]+>', '', s).strip()
            if clean:
                result.append(clean)
        return result
    except:
        return []

def extract_hours(snippets, shop_name):
    """從 snippet 列表裡提取結構化營業時間"""
    
    # 關鍵字：必須包含店名或營業時間相關詞
    relevant = []
    for s in snippets:
        if any(k in s for k in ["營業", "公休", "休", "星期", "週一", "週二", "週三", "週四", "週五", "週六", "週日", ":30", ":00"]):
            relevant.append(s)
    
    if not relevant:
        return ""
    
    # 合併所有 relevant snippets
    text = " ".join(relevant)
    
    # 提取公休日
    holiday = ""
    holiday_patterns = [
        r'公休日[：:為]?每週([一二三四五六日])',
        r'公休[：:為]?每週([一二三四五六日])',
        r'〈週([一二三四五六日])公休〉',
        r'週([一二三四五六日])公休',
        r'每週([一二三四五六日])休',
        r'休息[：:為]?每週([一二三四五六日])',
    ]
    for pattern in holiday_patterns:
        m = re.search(pattern, text)
        if m:
            holiday = f"週{m.group(1)}公休"
            break
    
    # 提取營業時間（各種格式）
    hours = ""
    time_patterns = [
        r'營業時間[：:\-~至到]*\s*(\d{1,2}[:：]\d{2})\s*(?:至|~|-|到)\s*(\d{1,2}[:：]\d{2})',
        r'(\d{1,2}[:：]\d{2})\s*(?:至|~|-|到)\s*(\d{1,2}[:：]\d{2})',
        r'(\d{1,2}[:：]\d{2})\s*-\s*(\d{1,2}[:：]\d{2})',
    ]
    for pattern in time_patterns:
        m = re.search(pattern, text)
        if m:
            start = m.group(1).replace('：', ':')
            end = m.group(2).replace('：', ':')
            hours = f"{start}-{end}"
            break
    
    # 提取最後點餐時間
    last_order = ""
    last_match = re.search(r'最後(?:點餐|出餐|點餐時間)[：:為]*?(\d{1,2}[:：]\d{2})', text)
    if last_match:
        last_order = f"（最後點餐{last_match.group(1).replace('：', ':')}）"
    
    # 組合
    parts = []
    if hours:
        parts.append(hours)
    if holiday:
        parts.append(holiday)
    if last_order:
        parts.append(last_order)
    
    if parts:
        return "；".join(parts)
    
    # 如果提取失敗，回傳第一個 relevant snippet 的前 100 字
    return relevant[0][:100] if relevant else ""

def main():
    rows = []
    with open(CSV_PATH, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        for row in reader:
            rows.append(row)
    
    # 篩出缺營業時間的
    missing = [r for r in rows if not r.get('business_hours','').strip()]
    print(f"總共 {len(rows)} 筆，缺營業時間 {len(missing)} 筆")
    
    # 測試：先跑楊梅區
    targets = [r for r in missing if r.get('county','') == '桃園' and r.get('district','') == '楊梅區']
    if not targets:
        targets = missing[:10]
    
    print(f"本次處理: {len(targets)} 筆")
    
    for i, row in enumerate(targets):
        name = row.get('name', '')
        district = row.get('district', '')
        query = f"{name} {district} 營業時間"
        
        print(f"[{i+1}/{len(targets)}] {name} ({district})")
        
        snippets = search_ddg(query)
        hours = extract_hours(snippets, name)
        
        if hours:
            print(f"  -> {hours}")
            row['business_hours'] = hours
        else:
            print(f"  -> 查不到")
        
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