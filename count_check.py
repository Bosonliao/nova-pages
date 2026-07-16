import sys, io, json, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data_dir = 'C:/Users/USER/.openclaw/workspace/nova-pages/data'
real_dishes = 0
new_saves = 0
for fn in os.listdir(data_dir):
    if fn.endswith('.json') and fn not in ['meta.json', 'cities.json', 'nightmarkets.json']:
        path = os.path.join(data_dir, fn)
        try:
            city = json.load(open(path, 'r', encoding='utf-8'))
            for r in city.get('food', []):
                d = r.get('dishes')
                if d and len(d) > 0:
                    real_dishes += 1
                    # Check if dishes are simple strings (my format) vs dict (pre-existing)
                    if d and isinstance(d[0], str):
                        new_saves += 1
        except:
            pass
print(f'With real dishes (total): {real_dishes}')
print(f'String-type dishes (likely my saves): {new_saves}')