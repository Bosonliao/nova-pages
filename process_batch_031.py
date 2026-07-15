#!/usr/bin/env python3
"""Process batch_031 restaurants using agy CLI to find recommended dishes."""
import json
import subprocess
import time
import os
import re
import pathlib
import sys

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(line_buffering=True, encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

AGY_BIN = str(pathlib.Path.home() / 'AppData' / 'Local' / 'agy' / 'bin' / 'agy.exe')

def search_with_agy(restaurant_name, area, category):
    """Use agy to search for restaurant recommended dishes."""
    prompt = (
        f"搜尋台灣餐廳「{restaurant_name}」（位置：{area}，類型：{category}）的推薦菜色。"
        f"請找出3道真實存在的招牌菜或必吃推薦，每道菜給菜名和一句簡短描述(30字內)。"
        f"只回覆JSON格式陣列：[{{\"name\":\"菜名\",\"desc\":\"描述\"}},...]，不要其他文字。"
        f"如果找不到資訊，回覆[]。"
    )
    
    env = os.environ.copy()
    env['Path'] = env.get('Path', '') + ';' + str(pathlib.Path.home() / 'AppData' / 'Local' / 'agy' / 'bin')
    env['PYTHONUTF8'] = '1'
    
    try:
        result = subprocess.run(
            [AGY_BIN, '--print', prompt, '--dangerously-skip-permissions', '--print-timeout', '3m'],
            capture_output=True, timeout=200, env=env
        )
        output = result.stdout.decode('utf-8', errors='replace').strip()
        
        # Try to extract JSON from output
        json_match = re.search(r'\[.*\]', output, re.DOTALL)
        if json_match:
            try:
                dishes = json.loads(json_match.group())
                if isinstance(dishes, list) and len(dishes) > 0:
                    valid_dishes = []
                    for d in dishes[:3]:
                        if isinstance(d, dict) and 'name' in d and 'desc' in d:
                            valid_dishes.append({"name": d['name'], "desc": d['desc']})
                    if valid_dishes:
                        return valid_dishes
            except json.JSONDecodeError:
                pass
        
        print(f"  Raw output: {output[:300]}...", flush=True)
        return None
    except subprocess.TimeoutExpired:
        print(f"  agy timeout for {restaurant_name}", flush=True)
        return None
    except Exception as e:
        print(f"  agy error: {e}", flush=True)
        return None

def save_results(results):
    with open('batch_031_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

# Main
batch_file = 'batch_031.json'
with open(batch_file, 'r', encoding='utf-8') as f:
    batch = json.load(f)

# Load existing results if any
results = {}
if os.path.exists('batch_031_results.json'):
    with open('batch_031_results.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
    print(f"Loaded existing results for {sum(len(v) for v in results.values())} restaurants", flush=True)

print(f"Processing {len(batch)} restaurants...", flush=True)

for i, restaurant in enumerate(batch):
    name = restaurant['name']
    area = restaurant.get('area', '')
    city = restaurant['city']
    idx = restaurant['index']
    category = restaurant.get('category', '')
    
    # Skip non-restaurant
    if '無店面' in name or '不提供餐點' in name:
        print(f"[{i+1}/{len(batch)}] SKIP: {name}", flush=True)
        continue
    
    # Check if already processed
    if city in results and str(idx) in results[city]:
        print(f"[{i+1}/{len(batch)}] ALREADY DONE: {name}", flush=True)
        continue
    
    # Clean name for search
    clean_name = name.split('｜')[0].split('（')[0].split('-')[0].strip()
    if len(clean_name) < 3:
        clean_name = name
    
    print(f"[{i+1}/{len(batch)}] {clean_name} ({city}, idx={idx})", flush=True)
    
    dishes = search_with_agy(clean_name, area, category)
    
    if dishes:
        print(f"  Found {len(dishes)} dishes: {[d['name'] for d in dishes]}", flush=True)
        if city not in results:
            results[city] = {}
        results[city][str(idx)] = dishes
        save_results(results)  # Save after each success
    else:
        print(f"  No dishes found", flush=True)
    
    time.sleep(1)

# Final save
save_results(results)
print(f"\nDone! Results saved to batch_031_results.json", flush=True)
print(f"Restaurants with dishes: {sum(len(v) for v in results.values())}/{len(batch)}", flush=True)