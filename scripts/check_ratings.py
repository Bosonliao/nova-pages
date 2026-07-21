import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food',[])

has_rating = sum(1 for f in foods if f.get('rating',0) > 0)
no_rating = sum(1 for f in foods if not f.get('rating',0) > 0)
has_reviews = sum(1 for f in foods if (f.get('reviews') or 0) > 0)

print(f'桃園 total: {len(foods)}')
print(f'有評分: {has_rating}')
print(f'無評分: {no_rating}')
print(f'有評論數: {has_reviews}')

drink = [f for f in foods if any('飲品' in c for c in f.get('categories',[]))]
drink_rated = sum(1 for f in drink if f.get('rating',0) > 0)
print(f'\n飲料店: {len(drink)}')
print(f'飲料店有評分: {drink_rated}')
print(f'飲料店無評分: {len(drink) - drink_rated}')

# Show some without rating
no_rate = [f for f in drink if not f.get('rating',0) > 0][:10]
print(f'\n無評分範例:')
for f in no_rate:
    n = f.get('name','')
    r = f.get('rating',0)
    rv = f.get('reviews',0)
    print(f'  {n} | rating={r} reviews={rv}')

# Show some with rating
rated = [f for f in drink if f.get('rating',0) > 0][:5]
print(f'\n有評分範例:')
for f in rated:
    n = f.get('name','')
    r = f.get('rating',0)
    rv = f.get('reviews',0)
    print(f'  {n} | rating={r} reviews={rv}')
