"""Yahoo Search helper - bypass DuckDuckGo bot detection"""
import urllib.request, urllib.parse, re, html

def yahoo_search(query, max_results=10):
    """Search via Yahoo and return list of {title, url, snippet}"""
    encoded = urllib.parse.quote(query)
    url = f'https://search.yahoo.com/search?p={encoded}'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8'
    })
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        html_content = resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f"Search error: {e}")
        return []
    
    results = []
    # Parse search result blocks
    blocks = re.findall(r'<div class="dd[^"]*".*?</div>\s*</div>\s*</div>', html_content, re.DOTALL)
    if not blocks:
        blocks = re.findall(r'<li class="[^"]*".*?</li>', html_content, re.DOTALL)
    
    for block in blocks[:max_results]:
        title_m = re.search(r'<a[^>]*class="[^"]*title[^"]*"[^>]*>(.*?)</a>', block, re.DOTALL)
        url_m = re.search(r'<a[^>]*href="(https?://[^"]+)"', block)
        snippet_m = re.search(r'<p[^>]*>(.*?)</p>', block, re.DOTALL)
        
        title = html.unescape(re.sub(r'<[^>]+>', '', title_m.group(1))) if title_m else ''
        link = url_m.group(1) if url_m else ''
        snippet = html.unescape(re.sub(r'<[^>]+>', '', snippet_m.group(1))) if snippet_m else ''
        
        if title and link:
            results.append({'title': title, 'url': link, 'snippet': snippet})
    
    return results

def fetch_page(url, max_chars=5000):
    """Fetch a page and return readable text"""
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8'
    })
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        content = resp.read().decode('utf-8', errors='replace')
        # Strip HTML tags
        text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = html.unescape(text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:max_chars]
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else '阿三肉圓 彰化 推薦菜'
    results = yahoo_search(query)
    for i, r in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(f"Title: {r['title']}")
        print(f"URL: {r['url']}")
        print(f"Snippet: {r['snippet'][:200]}")