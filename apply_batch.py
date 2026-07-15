# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# Load the data
with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load batch dishes
with open('batch_dishes.json', 'r', encoding='utf-8') as f:
    batch = json.load(f)

foods = data['台北']['food']
count = 0

for idx_str, dishes in batch.items():
    idx = int(idx_str)
    if idx < len(foods) and not foods[idx].get('dishes'):
        foods[idx]['dishes'] = dishes
        count += 1
        nm = foods[idx].get('name', '?')[:40]
        print(f"Added {len(dishes)} dishes to idx={idx}: {nm}")
    elif idx < len(foods) and foods[idx].get('dishes'):
        print(f"Skipped idx={idx} (already has dishes): {foods[idx].get('name','?')[:40]}")
    else:
        print(f"Skipped idx={idx} (out of range)")

with open('data-zh.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSaved data-zh.json ({count} restaurants updated)")