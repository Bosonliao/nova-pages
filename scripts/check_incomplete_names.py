import json, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Check all county JSON files for drink shops with incomplete names
base = 'data'
total_incomplete = 0
total_complete = 0
incomplete_by_county = {}

for fname in os.listdir(base):
    if not fname.endswith('.json') or fname == '97_5.json':
        continue
    fpath = os.path.join(base, fname)
    try:
        data = json.load(open(fpath, 'r', encoding='utf-8'))
    except:
        continue
    foods = data.get('food', []) if isinstance(data, dict) else data if isinstance(data, list) else []
    county = fname.replace('.json', '')
    
    for f in foods:
        cats = f.get('categories', [])
        if not any('飲品' in c or '飲料' in c for c in cats):
            continue
        name = f.get('name', '')
        # Check if name has branch info (contains 店/站/門市/分店)
        has_branch = any(kw in name for kw in ['店', '站', '門市', '分店', '號'])
        # Also check if name is just a brand (single word, no space/branch)
        if not has_branch:
            total_incomplete += 1
            if county not in incomplete_by_county:
                incomplete_by_county[county] = []
            incomplete_by_county[county].append(name)
        else:
            total_complete += 1

print(f'完整店名: {total_complete}')
print(f'不完整(只有品牌名): {total_incomplete}')
print(f'\n各縣市不完整數量:')
for county in sorted(incomplete_by_county.keys(), key=lambda k: len(incomplete_by_county[k]), reverse=True):
    names = incomplete_by_county[county]
    print(f'  {county}: {len(names)} 家')
    # Show unique brand names
    brands = set()
    for n in names:
        brand = n.split(' ')[0].split('-')[0].split('（')[0].split('(')[0].strip()
        brands.add(brand)
    print(f'    品牌: {", ".join(sorted(brands))}')
