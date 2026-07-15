import json
import time
import sys

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

target_cities = ['花蓮', '台東', '雲林', '澎湖', '金馬']

# Collect all candidates with city info
candidates = []
for city in target_cities:
    if city not in data:
        continue
    food = data[city].get('food', [])
    for i, r in enumerate(food):
        tags = r.get('tags', [])
        rating = r.get('rating', 0)
        reviews = r.get('reviews', 0)
        dishes = r.get('dishes', [])
        is_michelin = 'michelin' in tags
        is_popular = rating >= 4.0 and reviews >= 1000
        if (is_michelin or is_popular) and (not dishes or len(dishes) == 0):
            # Clean up name for search - remove marketing fluff
            name = r.get('name', '')
            # Keep original name but create a search-friendly version
            search_name = name.split('|')[0].split('（')[0].split('(')[0].strip()
            if len(search_name) > 20:
                # Try to extract just the core name
                parts = search_name.split('-')
                if len(parts) > 1:
                    search_name = parts[0].strip()
            if len(search_name) > 15:
                # Cut at common separators
                for sep in ['｜', ' ', ' - ', '·']:
                    if sep in search_name:
                        search_name = search_name.split(sep)[0].strip()
                        break
            candidates.append({
                'city': city,
                'index': i,
                'name': name,
                'search_name': search_name,
                'rating': rating,
                'reviews': reviews,
                'is_michelin': is_michelin
            })

print(f"Total candidates to process: {len(candidates)}")
# Write candidate list for reference
with open('all_candidates.json', 'w', encoding='utf-8') as f:
    json.dump(candidates, f, ensure_ascii=False, indent=2)
print("Candidates written to all_candidates.json")