"""把搜尋到的菜色寫入 yunlin.json"""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read dish data from stdin
# Format: RESTAURANT_NAME|dish1:desc1;dish2:desc2;...
line = sys.stdin.readline().strip()
if not line or line == 'NO_DATA':
    print('NO_DATA')
    sys.exit(0)

parts = line.split('|')
if len(parts) < 2:
    print('FORMAT_ERROR')
    sys.exit(1)

restaurant_name = parts[0]
dish_str = parts[1]

dishes = []
for item in dish_str.split(';'):
    item = item.strip()
    if not item:
        continue
    if ':' in item:
        name, desc = item.split(':', 1)
        dishes.append({"name": name.strip(), "description": desc.strip()})
    else:
        dishes.append({"name": item, "description": ""})

if not dishes:
    print('NO_DISHES_FOUND')
    sys.exit(0)

path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/yunlin.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

food = data.get('food', [])
updated = False
for r in food:
    if r.get('name', '') == restaurant_name and not r.get('dishes'):
        r['dishes'] = dishes
        updated = True
        break

if updated:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'SAVED:{restaurant_name}:{len(dishes)} dishes')
else:
    print(f'NOT_FOUND_OR_HAS_DISHES:{restaurant_name}')
