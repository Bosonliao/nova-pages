import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

target_cities = ['花蓮', '台東', '雲林', '澎湖', '金馬']
results = []

for city in target_cities:
    if city not in data:
        continue
    food = data[city].get('food', [])
    updated = 0
    total_candidates = 0
    for r in food:
        tags = r.get('tags', [])
        rating = r.get('rating', 0)
        reviews = r.get('reviews', 0)
        dishes = r.get('dishes', [])
        is_michelin = 'michelin' in tags
        is_popular = rating >= 4.0 and reviews >= 1000
        if (is_michelin or is_popular):
            total_candidates += 1
            if dishes and len(dishes) > 0:
                updated += 1
    results.append(f'{city}: {updated}/{total_candidates} restaurants have dishes')

with open('final_report.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))
    f.write(f'\n\nTotal: {sum(int(r.split(": ")[1].split("/")[0]) for r in results)}/{sum(int(r.split(": ")[1].split("/")[1]) for r in results)} restaurants have dishes\n')

print('Done')