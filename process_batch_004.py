import json, sys, time
sys.stdout.reconfigure(encoding='utf-8')

# Read batch
with open('batch_004.json', 'r', encoding='utf-8') as f:
    batch = json.load(f)

# Load data files
with open('data-zh.json', 'r', encoding='utf-8') as f:
    data_zh = json.load(f)
with open('data-ja.json', 'r', encoding='utf-8') as f:
    data_ja = json.load(f)

# Dishes mapping from search results will be stored here
# Format: {city_index: [{name, desc}, ...]}
dishes_map = {}

# Print batch info for reference
for i, r in enumerate(batch):
    print(f"{i}: city={r['city']} idx={r['index']} name={r['name']} area={r['area']}")