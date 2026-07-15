import json
from collections import Counter

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

all_areas = Counter()
for city in data:
    if not isinstance(data[city], dict):
        continue
    for section in ['food', 'spots', 'indoor', 'souvenirs']:
        items = data[city].get(section, [])
        for item in items:
            a = item.get('area', '')
            if a:
                all_areas[a] += 1

keep = {'東區', '北區', '西區', '南區', '中區'}
changes = 0
lines = [f'Total unique areas: {len(all_areas)}', '']

for area, count in sorted(all_areas.items()):
    if area.endswith('區') and area not in keep:
        new = area[:-1]
        flag = ' -> ' + new
        changes += 1
    elif area.endswith('区') and area.replace('区', '區') not in keep:
        new = area[:-1]
        flag = ' -> ' + new + ' (simp)'
        changes += 1
    else:
        flag = ''
    lines.append(f'  {area}: {count}{flag}')

lines.append(f'\nTotal to change: {changes}')

with open('area_audit.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'Done. {changes} areas to change. See area_audit.txt')
