#!/usr/bin/env python3
"""Helper to apply dishes to data-zh.json"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

DISHES_MAP = {}  # Will be filled by search results

def load_data():
    with open('data-zh.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open('data-zh.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def apply_dishes(dishes_map):
    """Apply dishes to restaurants by index"""
    data = load_data()
    foods = data['台中']['food']
    applied = 0
    for idx_str, dishes in dishes_map.items():
        idx = int(idx_str)
        if idx < len(foods) and foods[idx].get('rating', 0) >= 4.0 and foods[idx].get('reviews', 0) >= 1000:
            existing = foods[idx].get('dishes')
            if not existing or (isinstance(existing, list) and len(existing) == 0):
                foods[idx]['dishes'] = dishes
                applied += 1
    save_data(data)
    return applied

if __name__ == '__main__':
    # Test: load and show status
    data = load_data()
    foods = data['台中']['food']
    need = 0
    has = 0
    for r in foods:
        if r.get('rating', 0) >= 4.0 and r.get('reviews', 0) >= 1000:
            d = r.get('dishes')
            if not d or (isinstance(d, list) and len(d) == 0):
                need += 1
            else:
                has += 1
    print(f'Has dishes: {has}, Need dishes: {need}')