import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/taipei.json', encoding='utf-8') as f:
    d = json.load(f)

food = d.get('food', [])
# Sort by reviews desc, filter out ones that already have dishes
need_dishes = []
for i, r in enumerate(food):
    if not r.get('dishes'):
        need_dishes.append({
            'city': '台北',
            'index': i,
            'name': r.get('name', ''),
            'rating': r.get('rating', 0),
            'reviews': r.get('reviews', 0),
            'area': r.get('area', ''),
            'category': r.get('category', ''),
        })

# Sort by reviews desc
need_dishes.sort(key=lambda x: x['reviews'], reverse=True)

# Take top 50
batch = need_dishes[:50]

with open('taipei_batch_01.json', 'w', encoding='utf-8') as f:
    json.dump(batch, f, ensure_ascii=False, indent=2)

print(f'Total needing dishes: {len(need_dishes)}')
print(f'Batch 1: 50 restaurants (top by reviews)')
for r in batch[:5]:
    print(f"  {r['name']} ({r['reviews']} reviews, {r['area']})")
print(f"  ... and {len(batch)-5} more")
