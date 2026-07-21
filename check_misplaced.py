import json, sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
files = sorted([f for f in os.listdir(DATA) if f.endswith('.json') and f not in ['meta.json','cities.json','search_results_temp.json']])
keywords = ['新埔', '金山鴨肉', '紅毛港', '阿霞飯店', '城隍廟']
for f in files:
    d = json.load(open(os.path.join(DATA, f), 'r', encoding='utf-8'))
    for cat in ['food','spots','souvenirs','routes']:
        if cat in d and isinstance(d[cat], list):
            for item in d[cat]:
                if not isinstance(item, dict):
                    continue
                name = item.get('name', '')
                for kw in keywords:
                    if kw in name:
                        print(f'{f} [{cat}]: {name} | area={item.get("area","")} | lat={item.get("lat","N/A")}')