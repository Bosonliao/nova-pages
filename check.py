import json, sys
sys.stdout.reconfigure(encoding='utf-8')
data = json.load(open('data-zh.json', encoding='utf-8'))
foods = data['台北']['food']
for i in range(28, 36):
    r = foods[i]
    name = r['name']
    rating = r.get('rating', 0)
    reviews = r.get('reviews', 0)
    michelin = r.get('michelin', '')
    tags = r.get('tags', [])
    has_dishes = 'dishes' in r
    print(f'{i}: {name} | rating={rating} reviews={reviews} michelin={michelin} tags={tags} has_dishes={has_dishes}')