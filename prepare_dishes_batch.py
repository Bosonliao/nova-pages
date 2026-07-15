import json
import time
import os
import sys

def get_restaurants_needing_dishes(data, city, batch_size=50):
    """Get restaurants without dishes for a city."""
    food = data[city].get('food', [])
    need = []
    for i, r in enumerate(food):
        if not r.get('dishes') or len(r['dishes']) == 0:
            need.append((i, r))
    return need

def generate_dishes_for_restaurant(restaurant):
    """Generate 3 recommended dishes for a restaurant using web_search data."""
    name = restaurant.get('name', '')
    category = restaurant.get('category', '') or restaurant.get('categories', '')
    area = restaurant.get('area', '')
    
    # Build search query
    query = f"{name} {area} 推薦 必吃 招牌菜"
    if category:
        query += f" {category}"
    
    return query

# Main
with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get all restaurants needing dishes, sorted by rating (highest first)
all_need = []
for city in data:
    if not isinstance(data[city], dict):
        continue
    food = data[city].get('food', [])
    for i, r in enumerate(food):
        if not r.get('dishes') or len(r['dishes']) == 0:
            try:
                rating = float(r.get('rating') or 0)
            except:
                rating = 0
            try:
                reviews = int(r.get('reviews') or 0)
            except:
                reviews = 0
            all_need.append((city, i, r, rating, reviews))

# Sort by rating desc, then reviews desc
all_need.sort(key=lambda x: (-x[3], -x[4]))

print(f"Total restaurants needing dishes: {len(all_need)}")
print(f"Top 5 by rating:")
for c, i, r, rating, reviews in all_need[:5]:
    print(f"  {c} [{i}] {r.get('name','')} rating={rating} reviews={reviews}")

# Save the list for batch processing
with open('need_dishes_list.json', 'w', encoding='utf-8') as f:
    json.dump([{
        'city': c,
        'index': i,
        'name': r.get('name', ''),
        'rating': rating,
        'reviews': reviews,
        'category': r.get('category', '') or r.get('categories', ''),
        'area': r.get('area', '')
    } for c, i, r, rating, reviews in all_need], f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(all_need)} restaurants to need_dishes_list.json")
print("Ready for batch processing.")
