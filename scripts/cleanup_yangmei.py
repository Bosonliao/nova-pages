import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

# Remove old Yangmei drink entries that have no rating and no address (the old ones without branch names)
to_remove = []
for i, f in enumerate(foods):
    if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or [])):
        # Remove if it has no rating AND no address (old incomplete entries)
        if (f.get('rating', 0) == 0 or not f.get('rating')) and not f.get('address'):
            # But keep ones that have a proper branch name
            name = f.get('name', '')
            if '店' not in name and '站' not in name:
                to_remove.append(i)

print(f'Removing {len(to_remove)} old incomplete entries:')
for i in reversed(to_remove):
    print(f'  - {foods[i]["name"]} ({foods[i].get("rating","?")}★)')
    del foods[i]

data['food'] = foods
with open('data/taoyuan.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Count remaining
yangmei_drinks = [f for f in foods if f.get('area') == '楊梅區' and any('飲品' in c for c in (f.get('categories') or []))]
print(f'\nRemaining 楊梅 drinks: {len(yangmei_drinks)}')
