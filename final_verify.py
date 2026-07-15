import json

# Final verification for both files
for fn in ['data-zh.json', 'data-ja.json']:
    with open(fn, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    keep_zh = {'東區', '北區', '西區', '南區', '中區'}
    keep_ja = {'東区', '北区', '西区', '南区', '中区'}
    
    issues = 0
    for city in data:
        if not isinstance(data[city], dict):
            continue
        for section in ['food', 'spots', 'indoor', 'souvenirs']:
            for item in data[city].get(section, []):
                a = item.get('area', '')
                if not a:
                    continue
                if a.endswith('區') and a not in keep_zh:
                    issues += 1
                if a.endswith('区') and a not in keep_ja:
                    issues += 1
    
    status = 'CLEAN' if issues == 0 else f'{issues} issues'
    print(f'{fn}: {status}')
