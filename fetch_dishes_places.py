"""
Fetch real popular dishes for restaurants using Google Places API.
Uses Place Details API to get reviews mentioning dishes, and place photos.
"""
import json
import requests
import time
import sys
import os

API_KEY = "REDACTED"

def search_place(name, area, city):
    """Find a place using Google Places Text Search."""
    query = f"{name} {area} {city} ?啁"
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": API_KEY,
        "language": "zh-TW",
        "region": "tw"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            results = resp.json().get("results", [])
            if results:
                return results[0].get("place_id")
        elif resp.status_code == 429:
            print("  Rate limited, waiting 2s...")
            time.sleep(2)
            return search_place(name, area, city)
    except Exception as e:
        print(f"  Search error: {e}")
    return None

def get_place_details(place_id):
    """Get place details including reviews."""
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "key": API_KEY,
        "language": "zh-TW",
        "fields": "name,reviews,types,serves_dishes"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json().get("result", {})
            return data
    except Exception as e:
        print(f"  Details error: {e}")
    return None

def extract_dishes_from_reviews(reviews, restaurant_name):
    """Extract dish mentions from reviews."""
    dish_mentions = {}
    
    if not reviews:
        return []
    
    # Common dish keywords to look for
    dish_keywords = [
        "憌?, "暻?, "皝?, "??, "蝎?, "蝎?, "蝟?, "擗?, "??, "?脤?",
        "??, "??, "皛?, "??, "??, "??, "??, "??, "瘨潭?",
        "??, "鞊?, "??, "蝢?, "擳?, "??, "??, "暾?, "曀?,
        "鞊?", "??, "??", "瘝?", "??", "憌脣?", "??, "?",
        "?熊", "憯賢", "????, "摰?", "?", "?恍?",
        "瘞湧?", "??", "擗?", "??", "瘝寞?", "鞊撚",
        " ??暻?, "皛瑁?憌?, "??憌?, "?爸憌?, "??憌?,
    ]
    
    for review in reviews:
        text = review.get("text", "").lower()
        # Simple extraction: find sentences mentioning food
        for keyword in dish_keywords:
            if keyword in text:
                # Try to extract the dish name (surrounding context)
                idx = text.find(keyword)
                start = max(0, idx - 5)
                end = min(len(text), idx + len(keyword) + 5)
                context = text[start:end]
                dish_mentions[keyword] = dish_mentions.get(keyword, 0) + 1
    
    # Sort by mention count
    sorted_dishes = sorted(dish_mentions.items(), key=lambda x: -x[1])
    
    # Return top 3
    dishes = []
    for dish, count in sorted_dishes[:3]:
        # Clean up dish name
        clean_name = dish.strip()
        dishes.append({
            "name": clean_name,
            "desc": f"Google 閰?銝?{count} 甈⊥????刻??"
        })
    
    return dishes

def get_dishes_for_restaurant(name, area, city):
    """Main function to get dishes for a restaurant."""
    place_id = search_place(name, area, city)
    if not place_id:
        return None
    
    details = get_place_details(place_id)
    if not details:
        return None
    
    reviews = details.get("reviews", [])
    dishes = extract_dishes_from_reviews(reviews, name)
    
    # Also check serves_dishes if available
    if "serves_dishes" in details:
        popular = details["serves_dishes"].get("popular_dishes", [])
        for d in popular[:3]:
            dishes.append({
                "name": d.get("name", ""),
                "desc": d.get("description", "Google ?刻??")
            })
    
    return dishes[:3] if dishes else None

# Main batch processing
start = int(sys.argv[sys.argv.index('--start') + 1]) if '--start' in sys.argv else 0
count = int(sys.argv[sys.argv.index('--count') + 1]) if '--count' in sys.argv else 50

with open('need_dishes_list.json', 'r', encoding='utf-8') as f:
    need_list = json.load(f)

batch = need_list[start:start + count]
print(f"Processing {len(batch)} restaurants (index {start} to {start + len(batch) - 1})")

# Load current data
with open('data-zh.json', 'r', encoding='utf-8') as f:
    data_zh = json.load(f)
with open('data-ja.json', 'r', encoding='utf-8') as f:
    data_ja = json.load(f)

updated = 0
failed = 0

for idx, item in enumerate(batch):
    city = item['city']
    food_idx = item['index']
    name = item['name']
    area = item.get('area', '')
    
    # Skip if already has dishes
    if city in data_zh and food_idx < len(data_zh[city].get('food', [])):
        existing = data_zh[city]['food'][food_idx].get('dishes', [])
        if existing and len(existing) > 0:
            continue
    
    print(f"[{idx+1}/{len(batch)}] {city} {name}...", end=" ")
    
    dishes = get_dishes_for_restaurant(name, area, city)
    
    if dishes and len(dishes) > 0:
        # Update zh
        if city in data_zh and food_idx < len(data_zh[city].get('food', [])):
            data_zh[city]['food'][food_idx]['dishes'] = dishes
        # Update ja
        if city in data_ja and food_idx < len(data_ja[city].get('food', [])):
            data_ja[city]['food'][food_idx]['dishes'] = dishes
        updated += 1
        print(f"OK ({len(dishes)} dishes)")
    else:
        failed += 1
        print("NO DATA")
    
    time.sleep(0.3)  # Rate limit

# Save
if updated > 0:
    with open('data-zh.json', 'w', encoding='utf-8') as f:
        json.dump(data_zh, f, ensure_ascii=False, indent=2)
    with open('data-ja.json', 'w', encoding='utf-8') as f:
        json.dump(data_ja, f, ensure_ascii=False, indent=2)

print(f"\nDone. Updated: {updated}, Failed: {failed}")
print("Saved both files.")

