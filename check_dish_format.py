import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open('data-zh.json', encoding='utf-8') as f:
    data = json.load(f)

# Check dish formats
total_dishes = 0
empty_desc = 0
has_desc = 0
string_dishes = 0
dict_dishes = 0

for city, d in data.items():
    if not isinstance(d, dict):
        continue
    for r in d.get('food', []):
        for dish in r.get('dishes', []):
            total_dishes += 1
            if isinstance(dish, str):
                string_dishes += 1
            elif isinstance(dish, dict):
                dict_dishes += 1
                desc = (dish.get('description') or '').strip()
                if not desc:
                    empty_desc += 1
                else:
                    has_desc += 1

print(f'Total dishes: {total_dishes}')
print(f'String type: {string_dishes}')
print(f'Dict type: {dict_dishes}')
print(f'Empty description: {empty_desc} ({empty_desc*100//max(dict_dishes,1)}%)')
print(f'Has description: {has_desc} ({has_desc*100//max(dict_dishes,1)}%)')

# Show a few examples of each type
print('\n--- String type examples ---')
count = 0
for city, d in data.items():
    if not isinstance(d, dict) or count >= 3:
        continue
    for r in d.get('food', []):
        for dish in r.get('dishes', []):
            if isinstance(dish, str):
                print(f'  {city} {r.get("name","")}: {dish[:100]}')
                count += 1
                break
        if count >= 3:
            break
    if count >= 3:
        break

print('\n--- Dict with description examples ---')
count = 0
for city, d in data.items():
    if not isinstance(d, dict) or count >= 3:
        continue
    for r in d.get('food', []):
        for dish in r.get('dishes', []):
            if isinstance(dish, dict) and (dish.get('description') or '').strip():
                print(f'  {city} {r.get("name","")}: {dish.get("name","")} -> {dish.get("description","")[:80]}')
                count += 1
                break
        if count >= 3:
            break
    if count >= 3:
        break
