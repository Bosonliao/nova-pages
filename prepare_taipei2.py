import json

with open('data/taipei.json', encoding='utf-8') as f:
    d = json.load(f)

food = d.get('food', [])
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

need_dishes.sort(key=lambda x: x['reviews'], reverse=True)
batch = need_dishes[50:100]

with open('taipei_batch_02.json', 'w', encoding='utf-8') as f:
    json.dump(batch, f, ensure_ascii=False, indent=2)

print(f'Batch 2: 50 restaurants (rank 51-100 by reviews)')
