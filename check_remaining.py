import json, glob, os, sys
sys.stdout.reconfigure(encoding='utf-8')
for f in glob.glob('data/*.json'):
    if f.endswith('meta.json') or f.endswith('nightmarkets.json'): continue
    with open(f, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    for key in ['food','foods','restaurants']:
        for item in data.get(key, []):
            if item.get('description') == '新鮮海鮮料理專賣，超人氣的海味選擇':
                print(f'{os.path.basename(f)}: {item.get("name","")}')