import json

# Check data-ja.json for areas still ending with 区 (Japanese shinjitai)
with open('data-ja.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

keep = {'東区', '北区', '西区', '南区', '中区'}  # Japanese forms
keep_trad = {'東區', '北區', '西區', '南區', '中區'}

issues = []
for city in data:
    if not isinstance(data[city], dict):
        continue
    for section in ['food', 'spots', 'indoor', 'souvenirs']:
        items = data[city].get(section, [])
        for item in items:
            a = item.get('area', '')
            if not a:
                continue
            # Check for trailing 区 (Japanese) not in keep
            if a.endswith('区') and a not in keep and a not in keep_trad:
                issues.append(f'  JAP-SIMP [{city}.{section}] {item.get("name","")}: area={a}')
            # Check for trailing 區 (traditional) not in keep
            if a.endswith('區') and a not in keep_trad:
                issues.append(f'  TRAD [{city}.{section}] {item.get("name","")}: area={a}')

with open('ja_area_check.txt', 'w', encoding='utf-8') as f:
    f.write(f'data-ja.json area check\n')
    f.write(f'Issues: {len(issues)}\n\n')
    for line in issues[:50]:
        f.write(line + '\n')
    if len(issues) > 50:
        f.write(f'\n... and {len(issues)-50} more\n')

print(f'data-ja.json: ' + str(len(issues)) + ' areas still ending with qu (not in keep set)')
