"""
Batch script to search for signature dishes for Taipei restaurants.
Uses DuckDuckGo HTML search via web_fetch, extracts dish info from snippets.
"""
import json
import time
import re
import os
import urllib.parse

# This script will be called by the agent - it generates the search URLs and
# the agent will use web_fetch to get results, then feed them back.
# Actually, since we can't make HTTP requests directly from Python (no requests lib guaranteed),
# let's just output the list of restaurants to process in order.

data_path = r'C:\Users\USER\.openclaw\workspace\nova-pages\data-zh.json'

with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

taipei = data['台北']
food = taipei['food']

need_dishes = []
for i, r in enumerate(food):
    has_michelin = r.get('tags') and 'michelin' in r.get('tags', [])
    is_popular = r.get('rating', 0) >= 4.0 and r.get('reviews', 0) >= 1000
    has_dishes = r.get('dishes') and len(r.get('dishes', [])) > 0
    if (has_michelin or is_popular) and not has_dishes:
        need_dishes.append({'index': i, 'name': r['name']})

print(f"Total needing dishes: {len(need_dishes)}")
# Output as JSON for the agent to process
print(json.dumps(need_dishes[:20], ensure_ascii=False))  # First 20 for first batch
