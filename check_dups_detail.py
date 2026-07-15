import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find all duplicates in souvenirs and spots
for city in data:
    if not isinstance(data[city], dict):
        continue
    for section in ['souvenirs', 'spots', 'food', 'indoor']:
        items = data[city].get(section, [])
        seen = {}
        for i, item in enumerate(items):
            name = item.get('name', '')
            if name in seen:
                j = seen[name]
                print(f'DUP [{city}.{section}] "{name}" at [{j}] and [{i}]')
                print(f'  [{j}] keys={list(items[j].keys())}')
                print(f'  [{i}] keys={list(items[i].keys())}')
                # Show brief content
                for k in items[j]:
                    vj = str(items[j][k])[:80]
                    vi = str(items[i].get(k,''))[:80]
                    if vj != vi:
                        print(f'  diff {k}: [{j}]={vj} vs [{i}]={vi}')
            else:
                seen[name] = i
