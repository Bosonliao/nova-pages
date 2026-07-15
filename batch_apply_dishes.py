#!/usr/bin/env python3
"""Batch apply dishes to data-zh.json for Taichung restaurants.
Reads a JSON mapping of index -> dishes and applies them."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

def load_data():
    with open('data-zh.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open('data-zh.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def apply_batch(dishes_map):
    """Apply a batch of dishes. dishes_map = {index: [dish objects]}"""
    data = load_data()
    foods = data['台中']['food']
    applied = 0
    skipped = 0
    for idx_str, dishes in dishes_map.items():
        idx = int(idx_str)
        if idx >= len(foods):
            skipped += 1
            continue
        r = foods[idx]
        if r.get('rating', 0) < 4.0 or r.get('reviews', 0) < 1000:
            skipped += 1
            continue
        existing = r.get('dishes')
        if existing and isinstance(existing, list) and len(existing) > 0:
            skipped += 1
            continue
        foods[idx]['dishes'] = dishes
        applied += 1
    save_data(data)
    return applied, skipped

if __name__ == '__main__':
    import json
    # Read dishes from stdin
    dishes_map = json.loads(sys.argv[1])
    applied, skipped = apply_batch(dishes_map)
    print(f'Applied: {applied}, Skipped: {skipped}')