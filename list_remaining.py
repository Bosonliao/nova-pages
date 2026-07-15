import json, sys
sys.stdout.reconfigure(encoding='utf-8')
data = json.load(open('data-zh.json', 'r', encoding='utf-8'))
foods = data['台北']['food']
eligible = json.load(open('eligible_indices.json'))
remaining = [i for i in eligible if not foods[i].get('dishes')]
# Write full remaining list to file for reliable access
with open('remaining_list.txt', 'w', encoding='utf-8') as f:
    for i in remaining:
        r = foods[i]
        nm = r.get('name', '?')
        rt = r.get('rating', 0)
        rv = r.get('reviews', 0)
        f.write(f'{i}|{nm}|{rt}|{rv}\n')
print(f'Remaining: {len(remaining)}')
for i in remaining[:30]:
    try:
        r = foods[i]
        nm = r.get('name', '?')
        rt = r.get('rating', 0)
        rv = r.get('reviews', 0)
        print(f'{i}|{nm}|{rt}|{rv}')
    except Exception as e:
        print(f'{i}|(encoding error)|{e}')