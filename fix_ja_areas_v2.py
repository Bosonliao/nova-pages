import json

# Fix data-ja.json - remove trailing 区 (Japanese shinjitai) except for keep set
KEEP_JA = {'東区', '北区', '西区', '南区', '中区'}

with open('data-ja.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

total_changes = 0
change_log = []

for city in data:
    if not isinstance(data[city], dict):
        continue
    for section in ['food', 'spots', 'indoor', 'souvenirs']:
        items = data[city].get(section, [])
        for item in items:
            a = item.get('area', '')
            if not a:
                continue
            # Strip city prefixes
            prefixes = ['台北市', '新北市', '台中市', '台南市', '高雄市',
                       '基隆市', '新竹市', '嘉義市', '苗栗市', '彰化市',
                       '宜蘭市', '花蓮市', '台東市', '屏東市', '馬公市',
                       '新竹縣', '連江', '桃園区']
            
            stripped = a
            for prefix in sorted(prefixes, key=len, reverse=True):
                if a.startswith(prefix) and len(a) > len(prefix):
                    stripped = a[len(prefix):]
                    break
            
            # Check if stripped version is in keep set
            if stripped in KEEP_JA:
                if a != stripped:
                    item['area'] = stripped
                    total_changes += 1
                    change_log.append(f'  [{city}] {a} -> {stripped} (stripped prefix)')
                continue
            
            # Remove trailing 区
            if stripped.endswith('区'):
                new = stripped[:-1]
                if a != new:
                    note = f'{a} -> {new}'
                    if stripped != a:
                        note += f' (stripped: {a} -> {stripped} -> {new})'
                    item['area'] = new
                    total_changes += 1
                    change_log.append(f'  [{city}] {note}')
            
            # Also check for trailing 區 (traditional, might still exist)
            elif stripped.endswith('區'):
                new = stripped[:-1]
                if a != new:
                    note = f'{a} -> {new} (traditional)'
                    if stripped != a:
                        note += f' (stripped: {a} -> {stripped} -> {new})'
                    item['area'] = new
                    total_changes += 1
                    change_log.append(f'  [{city}] {note}')

if change_log:
    with open('data-ja.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    with open('data-ja_area_changes_v2.txt', 'w', encoding='utf-8') as f:
        f.write(f'Total changes: {total_changes}\n')
        f.write('\n'.join(change_log))

print(f'data-ja.json: {total_changes} changes saved.')
