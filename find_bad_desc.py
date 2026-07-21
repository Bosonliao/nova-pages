import json, glob, os

count = 0
results = []
for f in glob.glob('data/*.json'):
    if f.endswith('meta.json') or f.endswith('nightmarkets.json'): continue
    with open(f, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    for key in ['food','foods','restaurants']:
        items = data.get(key, [])
        for item in items:
            desc = item.get('description','')
            if desc == '新鮮海鮮料理專賣，超人氣的海味選擇':
                count += 1
                name = item.get('name','')
                results.append(f'{os.path.basename(f)}: {name}')

with open('bad_descriptions.txt', 'w', encoding='utf-8') as out:
    for r in results:
        out.write(r + '\n')
    out.write(f'\nTotal: {count}\n')
print(f'Found {count} items with generic seafood description')