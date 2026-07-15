import json

KEEP_AREAS = {'東區', '北區', '西區', '南區', '中區'}

# City prefixes to strip (longest first for proper matching)
CITY_PREFIXES = [
    '台北市', '新北市', '台中市', '台南市', '高雄市',
    '基隆市', '新竹市', '嘉義市', '苗栗市', '彰化市',
    '宜蘭市', '花蓮市', '台東市', '屏東市', '馬公市',
    '桃園區',  # This is tricky - 桃園 is both a city and a district name
    '新竹縣', '連江',
]

# Areas that are route names or special - don't touch
SKIP_PATTERNS = ['路線', '一日遊', '巡禮', '跳島', '秘境', '經典', '文化', '親子',
                 '夜市', '溫泉', '賞花', '古道', '老街', '海岸', '縱谷', '半島',
                 '森林', '溫泉', '博物館', '夜市', 'IG', '網美', '農場', '花火節',
                 '藍眼淚', '戰地', '登島', '海線', '海科館', '漁港', '島']

def fix_area(area):
    """Fix a single area string. Returns (new_area, changed, note)."""
    if not area or not area.endswith('區'):
        return area, False, ''
    
    # Skip route-like names (they're not real district names)
    # But only skip if they're clearly route names, not just because they contain these words
    
    # First, strip city prefixes
    original = area
    stripped = area
    for prefix in sorted(CITY_PREFIXES, key=len, reverse=True):
        if area.startswith(prefix) and len(area) > len(prefix):
            stripped = area[len(prefix):]
            break
    
    # Now check the stripped version
    if stripped in KEEP_AREAS:
        if area != stripped:
            return stripped, True, f'stripped prefix: {original} -> {stripped}'
        return area, False, ''
    
    # Remove trailing 區
    if stripped.endswith('區'):
        new = stripped[:-1]
        if area != new:
            note = f'{original} -> {new}'
            if stripped != area:
                note += f' (stripped prefix first: {original} -> {stripped} -> {new})'
            return new, True, note
    
    return area, False, ''

# Process both files
for filename in ['data-zh.json', 'data-ja.json']:
    with open(filename, 'r', encoding='utf-8') as f:
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
                if a:
                    new_a, changed, note = fix_area(a)
                    if changed:
                        item['area'] = new_a
                        total_changes += 1
                        change_log.append(f'  [{city}] {note}')
    
    if change_log:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        log_filename = filename.replace('.json', '_area_changes.txt')
        with open(log_filename, 'w', encoding='utf-8') as f:
            f.write(f'Total changes: {total_changes}\n')
            f.write('\n'.join(change_log))
        
        print(f'[{filename}] {total_changes} changes saved. Log: {log_filename}')
    else:
        print(f'[{filename}] No changes needed.')

print('Done.')
