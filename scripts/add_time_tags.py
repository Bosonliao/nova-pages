import csv
from collections import Counter

path = r'C:\Users\USER\.openclaw\workspace\nova-pages\data\restaurants.csv'

def guess_time_tags(category, name=''):
    cat = (category or '').lower()
    name = (name or '').lower()
    tags = []
    
    if any(k in cat for k in ['早餐', '早午餐', 'brunch']) or any(k in name for k in ['早餐', '早午餐', '蛋餅', '豆漿', '油飯']):
        tags.append('早餐')
    
    if any(k in cat for k in ['中式', '台式', '日式', '韓式', '泰式', '越南', '印尼', '麻辣', '火鍋', '便當', '自助餐', '海鮮', '烤肉']):
        tags.extend(['午餐', '晚餐'])
    
    if any(k in cat for k in ['西式', '美式', '義式', '披薩', '漢堡', '牛排']):
        tags.extend(['午餐', '晚餐'])
    
    if any(k in cat for k in ['小吃', '麵食', '滷肉飯', '水餃', '牛肉麵']):
        tags.extend(['午餐', '晚餐', '宵夜'])
    
    if any(k in cat for k in ['咖啡', '咖啡廳', '甜點', '蛋糕', '冰淇淋', '飲料', '茶']):
        tags.append('下午茶')
    
    if any(k in name for k in ['宵夜', '夜', '酒吧', '居酒屋']):
        tags.append('宵夜')
    
    if any(k in cat for k in ['居酒屋', '酒吧', '串燒']):
        tags.append('宵夜')
    
    if not tags:
        tags = ['午餐', '晚餐']
    
    seen = set()
    result = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            result.append(t)
    return '|'.join(result)

rows = []
with open(path, 'r', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    for row in reader:
        row['time_tags'] = guess_time_tags(row.get('category', ''), row.get('name', ''))
        rows.append(row)

if 'time_tags' not in fieldnames:
    idx = fieldnames.index('tags') + 1 if 'tags' in fieldnames else len(fieldnames)
    fieldnames.insert(idx, 'time_tags')

with open(path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f'Updated {len(rows)} rows with time_tags')
tag_count = Counter()
for r in rows:
    for t in r['time_tags'].split('|'):
        tag_count[t] += 1
for tag, count in tag_count.most_common():
    print(f'  {tag}: {count}')