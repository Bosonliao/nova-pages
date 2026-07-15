import json

for fn in ['data-zh.json', 'data-ja.json']:
    try:
        with open(fn, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f'{fn}: OK ({len(str(data))} chars)')
    except Exception as e:
        print(f'{fn}: CORRUPT - {e}')
