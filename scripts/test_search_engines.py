"""
嘗試用 requests 直接呼叫 Google Maps 的內部 API
或者用 DuckDuckGo 搜尋光嶼咖啡的營業時間
"""
import sys
import io
import json
import urllib.request
import urllib.parse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 方法 1: DuckDuckGo 搜尋
print("=== DuckDuckGo 搜尋 ===")
ddg_url = "https://html.duckduckgo.com/html/"
data = urllib.parse.urlencode({"q": "光嶼咖啡 楊梅 營業時間 公休日"}).encode()
try:
    req = urllib.request.Request(ddg_url, data=data, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    })
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8')
        # 搜尋營業時間相關內容
        import re
        # 找包含星期幾的段落
        for day in ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日", "週一", "週二", "公休", "11:30", "18:00"]:
            if day in html:
                idx = html.index(day)
                context = html[max(0,idx-100):idx+100]
                # 去掉 HTML 標籤
                clean = re.sub(r'<[^>]+>', '', context)
                print(f"  {day}: {clean.strip()}")
except Exception as e:
    print(f"  Error: {e}")

# 方法 2: Bing 搜尋
print("\n=== Bing 搜尋 ===")
bing_url = "https://www.bing.com/search?q=" + urllib.parse.quote("光嶼咖啡 楊梅 營業時間")
try:
    req = urllib.request.Request(bing_url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8')
        import re
        for day in ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日", "週一", "公休", "11:30", "18:00"]:
            if day in html:
                idx = html.index(day)
                context = html[max(0,idx-100):idx+100]
                clean = re.sub(r'<[^>]+>', '', context)
                print(f"  {day}: {clean.strip()}")
except Exception as e:
    print(f"  Error: {e}")