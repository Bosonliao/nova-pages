"""快速測試 DuckDuckGo 搜尋光嶼咖啡營業時間"""
import sys, io, re, urllib.request, urllib.parse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

query = "光嶼咖啡 楊梅 營業時間 公休日"
url = "https://html.duckduckgo.com/html/"
data = urllib.parse.urlencode({"q": query}).encode()

req = urllib.request.Request(url, data=data, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
})

with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8')

# 提取所有 snippet
snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
print(f"找到 {len(snippets)} 個 snippet")
for i, s in enumerate(snippets):
    clean = re.sub(r'<[^>]+>', '', s).strip()
    if clean:
        print(f"\n[{i}] {clean[:200]}")