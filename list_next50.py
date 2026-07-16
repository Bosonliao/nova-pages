import sys, io, json, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data_dir = 'C:/Users/USER/.openclaw/workspace/nova-pages/data'
all_need = []
for fn in os.listdir(data_dir):
    if fn.endswith('.json') and fn not in ['meta.json', 'cities.json', 'nightmarkets.json']:
        path = os.path.join(data_dir, fn)
        try:
            city = json.load(open(path, 'r', encoding='utf-8'))
            county = fn.replace('.json', '')
            for r in city.get('food', []):
                if not r.get('dishes'):
                    all_need.append({
                        'name': r.get('name', ''),
                        'area': r.get('area', ''),
                        'reviews': r.get('reviews', 0),
                        'county': county,
                    })
        except:
            pass
all_need.sort(key=lambda x: x.get('reviews') or 0, reverse=True)
print(f'Remaining: {len(all_need)}')
print(f'Next 50:')
for i, r in enumerate(all_need[:50]):
    name = r['name']
    county = r['county']
    area = r['area']
    reviews = r['reviews']
    print(f'{i+1}. {name} | {county} | {area} | reviews={reviews}')