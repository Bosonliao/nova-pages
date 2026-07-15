import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open('data/taipei.json', encoding='utf-8') as f:
    d = json.load(f)

# Show first 15 food entries with dishes
for i, r in enumerate(d['food'][:15]):
    dishes = r.get('dishes', [])
    name = r.get('name', '')
    print(f'{i+1}. {name}')
    if dishes:
        for dish in dishes:
            dn = dish.get('name', '')
            dd = dish.get('description', '')[:80]
            print(f'   - {dn}: {dd}')
    else:
        print('   (無菜色)')
