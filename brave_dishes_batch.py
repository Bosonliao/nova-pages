#!/usr/bin/env python3
"""
Brave Search 菜色補充批次腳本
用 web_fetch brave search 搜尋餐廳推薦菜色，然後存入 JSON
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.parse
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    """簡易 HTML 文字提取器"""
    def __init__(self):
        super().__init__()
        self.result = []
        self.skip = False
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'):
            self.skip = True
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'):
            self.skip = False
    def handle_data(self, data):
        if not self.skip:
            self.result.append(data)
    def get_text(self):
        return ' '.join(self.result)

def fetch_url(url, max_chars=20000):
    """用 urllib 抓網頁"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        # 提取純文字
        parser = TextExtractor()
        parser.feed(html)
        text = parser.get_text()
        # 清理
        text = re.sub(r'\s+', ' ', text)
        return text[:max_chars]
    except Exception as e:
        return f"ERROR: {e}"

def search_brave(query):
    """用 Brave Search 搜尋"""
    encoded = urllib.parse.quote(query)
    url = f"https://search.brave.com/search?q={encoded}&source=web"
    return fetch_url(url)

def find_next_restaurant():
    """找出下一家需要補菜色的餐廳"""
    result = subprocess.run(
        ['python', 'C:/Users/USER/.openclaw/workspace/nova-pages/find_next_restaurant_all.py'],
        capture_output=True, text=True, timeout=30
    )
    lines = result.stdout.strip().split('\n')
    info = {}
    for line in lines:
        if ':' in line:
            key, val = line.split(':', 1)
            info[key.strip()] = val.strip()
    return info

def save_dishes(county, restaurant_name, dishes):
    """存菜色到 JSON"""
    path = f'C:/Users/USER/.openclaw/workspace/nova-pages/data/{county}.json'
    data = json.load(open(path, 'r', encoding='utf-8'))
    for f in data['food']:
        if f['name'] == restaurant_name:
            f['dishes'] = dishes
            break
    json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"  ✅ Saved: {restaurant_name} -> {dishes}")

def extract_dishes_from_text(text, restaurant_name):
    """從搜尋結果文字中提取菜色關鍵字"""
    # 搜尋常見食記用語
    dishes = []
    
    # 搜尋「必點」「推薦」「招牌」附近的菜名
    patterns = [
        r'必點[：: ]*([^\n。]{2,30})',
        r'招牌[：: ]*([^\n。]{2,30})',
        r'推薦[：: ]*([^\n。]{2,30})',
        r'必吃[：: ]*([^\n。]{2,30})',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for m in matches[:3]:
            m = m.strip()
            if len(m) > 2 and len(m) < 30 and m not in dishes:
                dishes.append(m)
    
    return dishes[:5]

# 主程式
if __name__ == '__main__':
    count = 0
    max_restaurants = 30
    
    while count < max_restaurants:
        info = find_next_restaurant()
        if 'NEXT_RESTAURANT' not in info:
            print("No more restaurants need dishes.")
            break
        
        name = info['NEXT_RESTAURANT']
        county = info['COUNTY']
        area = info.get('AREA', '')
        
        print(f"\n[{count+1}/{max_restaurants}] {name} ({county})")
        
        # 搜尋
        query = f"{name} {area} 推薦菜 必點"
        text = search_brave(query)
        
        if text.startswith("ERROR"):
            print(f"  ❌ Search failed: {text[:100]}")
            count += 1
            continue
        
        # 提取菜色
        dishes = extract_dishes_from_text(text, name)
        
        if not dishes:
            # 嘗試另一個搜尋
            query2 = f"{name} 必點 招牌 菜單"
            text2 = search_brave(query2)
            dishes = extract_dishes_from_text(text2, name)
        
        if dishes:
            save_dishes(county, name, dishes)
        else:
            print(f"  ⏭️ No dishes found, skipping")
        
        count += 1
        time.sleep(2)  # 避免太頻繁
    
    print(f"\nDone! Processed {count} restaurants.")