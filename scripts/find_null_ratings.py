import json, os, glob, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data_dir = r'C:\Users\USER\.openclaw\workspace\nova-pages\data'
city_files = [f for f in glob.glob(os.path.join(data_dir, '*.json')) 
              if '-' not in os.path.basename(f) 
              and 'meta' not in os.path.basename(f) 
              and 'cities' not in os.path.basename(f) 
              and 'search' not in os.path.basename(f) 
              and '97_' not in os.path.basename(f) 
              and 'drinks' not in os.path.basename(f) 
              and 'nightmarkets' not in os.path.basename(f)]

# Focus on spots with explicit rating: null (has the key but value is null)
for f in sorted(city_files):
    fname = os.path.basename(f)
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
    except:
        continue
    
    if isinstance(data, dict):
        for key in ['food', 'spots']:
            val = data.get(key, [])
            if isinstance(val, list):
                null_rated = [item for item in val 
                             if isinstance(item, dict) 
                             and 'rating' in item 
                             and item.get('rating') is None]
                if null_rated:
                    print(f'{fname}[{key}]: {len(null_rated)} explicit null ratings')
                    for item in null_rated:
                        name = item.get('name', '?')
                        area = item.get('area', '?')
                        has_reviews = 'reviews' in item
                        print(f'  - {name} | area: {area} | has reviews key: {has_reviews}')