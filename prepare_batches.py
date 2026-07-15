"""
Fetch real dishes for restaurants using web_search tool via subagent.
Each subagent processes a batch of ~100 restaurants.
"""
import json
import sys
import os

# Generate batch files for subagent processing
with open('need_dishes_list.json', 'r', encoding='utf-8') as f:
    need_list = json.load(f)

# Filter out ones that already have dishes in data-zh.json
with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

still_need = []
for item in need_list:
    city = item['city']
    idx = item['index']
    if city in data and isinstance(data[city], dict):
        food = data[city].get('food', [])
        if idx < len(food):
            dishes = food[idx].get('dishes', [])
            if not dishes or len(dishes) == 0:
                still_need.append(item)

print(f"Still need dishes: {len(still_need)}")

# Split into batches of 50
batch_size = 50
batches = []
for i in range(0, len(still_need), batch_size):
    batch = still_need[i:i+batch_size]
    batches.append(batch)

print(f"Total batches: {len(batches)}")

# Write each batch to a file
for i, batch in enumerate(batches):
    filename = f'batch_{i:03d}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(batch, f, ensure_ascii=False, indent=2)

print(f"Written {len(batches)} batch files")

# Write summary
with open('batch_summary.txt', 'w', encoding='utf-8') as f:
    f.write(f"Total restaurants needing dishes: {len(still_need)}\n")
    f.write(f"Batch size: {batch_size}\n")
    f.write(f"Total batches: {len(batches)}\n")
    f.write(f"\nBatches by city:\n")
    from collections import Counter
    for i, batch in enumerate(batches):
        cities = Counter(item['city'] for item in batch)
        f.write(f"  Batch {i:03d}: {dict(cities)}\n")
