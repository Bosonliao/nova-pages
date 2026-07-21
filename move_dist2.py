with open('taiwan-travel.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 752 和 790 行 — 在描述後加 distBadge
for i in [751, 789]:  # 0-indexed
    if 's.description' in lines[i]:
        indent = lines[i].split('${')[0]
        lines[i] = lines[i].rstrip('\n') + f'\n{indent}            ' + '${distBadge(s.lat, s.lng)}\n'

with open('taiwan-travel.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Done')