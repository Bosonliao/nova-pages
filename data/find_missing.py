import json
import os
import glob

data_dir = r"C:\Users\USER\.openclaw\workspace\nova-pages\data"
exclude = ['drinks', 'osm', 'cities', 'meta', 'nightmarkets', 'search_results', 'geocoded']

for fp in sorted(glob.glob(os.path.join(data_dir, "*.json"))):
    fname = os.path.basename(fp)
    if any(ex in fname for ex in exclude):
        continue
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
        missing = []
        for item in data:
            r = item.get('rating', None)
            if r is None or r == 0:
                missing.append(item)
        if missing:
            print(f"{fname}: {len(missing)} missing")
            for m in missing:
                name = m.get('name', '?')
                area = m.get('area', '?')
                print(f"  - {name} | area: {area}")
    except Exception as e:
        print(f"{fname}: ERROR - {e}")