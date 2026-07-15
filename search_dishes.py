#!/usr/bin/env python3
"""Search for restaurant dishes using multiple methods."""
import json
import time
import requests
from urllib.parse import quote

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def search_ddg(query, max_results=5):
    """Search via DuckDuckGo HTML lite version."""
    url = f"https://lite.duckduckgo.com/lite/?q={quote(query)}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            # Parse results from HTML
            text = resp.text
            # Extract result links and snippets
            results = []
            # DDG lite has results in <a class="result-link" href="...">text</a>
            # and snippets in <td class="result-snippet">text</td>
            import re
            links = re.findall(r'class="result-link"[^>]*href="([^"]*)"[^>]*>([^<]*)', text)
            snippets = re.findall(r'class="result-snippet"[^>]*>(.*?)</td>', text, re.DOTALL)
            for i, (link, title) in enumerate(links[:max_results]):
                snippet = snippets[i] if i < len(snippets) else ""
                # Clean HTML tags from snippet
                snippet = re.sub(r'<[^>]+>', '', snippet).strip()
                results.append({"title": title.strip(), "url": link, "snippet": snippet})
            return results
    except Exception as e:
        print(f"  DDG error: {e}")
    return []

def search_bing(query, max_results=5):
    """Search via Bing."""
    url = f"https://www.bing.com/search?q={quote(query)}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            text = resp.text
            import re
            results = []
            # Bing results in <li class="b_algo">
            blocks = re.findall(r'<li class="b_algo">(.*?)</li>', text, re.DOTALL)
            for block in blocks[:max_results]:
                title_m = re.search(r'<h2><a[^>]*href="([^"]*)"[^>]*>(.*?)</a></h2>', block, re.DOTALL)
                if title_m:
                    url = title_m.group(1)
                    title = re.sub(r'<[^>]+>', '', title_m.group(2)).strip()
                    snippet_m = re.search(r'<p[^>]*>(.*?)</p>', block, re.DOTALL)
                    snippet = re.sub(r'<[^>]+>', '', snippet_m.group(1)).strip() if snippet_m else ""
                    results.append({"title": title, "url": url, "snippet": snippet})
            return results
    except Exception as e:
        print(f"  Bing error: {e}")
    return []

def fetch_url(url, max_chars=5000):
    """Fetch URL content."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15, max_chars=max_chars)
        if resp.status_code == 200:
            # Basic HTML to text
            text = resp.text
            import re
            # Remove scripts and styles
            text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            return text[:max_chars]
    except Exception as e:
        print(f"  Fetch error: {e}")
    return ""

def search_restaurant(name, area):
    """Search for restaurant recommended dishes."""
    query = f"{name} {area} 推薦菜 必吃"
    print(f"  Searching: {query}")
    
    # Try DDG first
    results = search_ddg(query)
    if not results:
        # Try Bing
        results = search_bing(query)
    
    if not results:
        print("  No search results found")
        return None
    
    # Fetch top 2 result pages for content
    all_text = ""
    for r in results[:3]:
        print(f"  Fetching: {r['title'][:50]}...")
        content = fetch_url(r['url'], 8000)
        all_text += content + "\n---\n"
        time.sleep(0.5)
    
    return all_text

# Main
with open('batch_031.json', 'r', encoding='utf-8') as f:
    batch = json.load(f)

for i, restaurant in enumerate(batch):
    name = restaurant['name']
    area = restaurant.get('area', '')
    city = restaurant['city']
    idx = restaurant['index']
    
    # Skip names that are clearly not restaurants with dishes
    skip_keywords = ['無店面', '不提供餐點', '咖啡廳']
    should_skip = any(kw in name for kw in ['無店面', '不提供餐點'])
    if should_skip:
        print(f"[{i+1}/{len(batch)}] SKIP: {name} (no restaurant)")
        continue
    
    print(f"[{i+1}/{len(batch)}] {name} ({city}, idx={idx})")
    content = search_restaurant(name, area)
    
    if content:
        # Save raw content for review
        safe_name = name.replace('/', '_').replace(' ', '_')[:30]
        with open(f'search_raw_{i}_{safe_name}.txt', 'w', encoding='utf-8') as f:
            f.write(content)
    
    time.sleep(1)  # Rate limiting
    
    # Only process first 5 for testing
    if i >= 4:
        print("Stopping at 5 for testing...")
        break

print("Done!")