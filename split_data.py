import json, os

with open('data-zh.json', encoding='utf-8') as f:
    data = json.load(f)

os.makedirs('data', exist_ok=True)

# Save each city as separate file
for city, d in data.items():
    if city.startswith('_') or city == 'nightmarkets':
        continue
    with open(f'data/{city}.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, separators=(',', ':'))

# Save nightmarkets separately
if 'nightmarkets' in data:
    with open('data/nightmarkets.json', 'w', encoding='utf-8') as f:
        json.dump(data['nightmarkets'], f, ensure_ascii=False, separators=(',', ':'))

# Save metadata
meta = {'_updatedAt': data.get('_updatedAt', '')}
with open('data/_meta.json', 'w', encoding='utf-8') as f:
    json.dump(meta, f, ensure_ascii=False, separators=(',', ':'))

print(f'Created {len(os.listdir("data"))} files')
for f in sorted(os.listdir('data')):
    size = os.path.getsize(f'data/{f}')
    print(f'  {f}: {size/1024:.0f} KB')
