import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Mark INPARADISE as dishes_searched (buffet, no fixed menu)
path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/taipei.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for r in data['food']:
    if r['name'] == 'INPARADISE 饗饗 微風信義店':
        r['dishes_searched'] = True
        print(f"Skipped: INPARADISE 饗饗 (buffet, no fixed menu)")
        break

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved!")