"""菜色補充批次處理 - 自動搜尋並補上菜色"""
import json, os, sys, io, time, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data_dir = 'C:/Users/USER/.openclaw/workspace/nova-pages/data'

# 要跳過的關鍵字
skip_keywords = ['百貨', '購物中心', '夜市', '市場', '商場', 'outlet', 'Outlet', '美食街',
                 '老街', '商圈', '一中街', '周邊小吃', '文化園區', '高跟鞋教堂']

# 讀取所有需要補菜色的餐廳
all_need = []
for fn in os.listdir(data_dir):
    if fn.endswith('.json') and fn not in ['meta.json', 'cities.json', 'nightmarkets.json']:
        path = os.path.join(data_dir, fn)
        try:
            city = json.load(open(path, 'r', encoding='utf-8'))
            food = city.get('food', [])
            county = fn.replace('.json', '')
            for r in food:
                if not r.get('dishes'):
                    name = r.get('name', '')
                    if any(kw in name for kw in skip_keywords):
                        continue
                    all_need.append({
                        'name': name,
                        'area': r.get('area', ''),
                        'reviews': r.get('reviews', 0),
                        'rating': r.get('rating', 0),
                        'county': county,
                        'categories': r.get('categories', [])
                    })
        except:
            pass

all_need.sort(key=lambda x: x.get('reviews') or 0, reverse=True)

# 輸出前 30 家
print(f'TOTAL_NEED: {len(all_need)}')
print(f'Processing top 30...')
print('---')
for i, r in enumerate(all_need[:30]):
    print(f'{i+1}|{r["name"]}|{r["county"]}|{r["area"]}|{r["reviews"]}|{",".join(r["categories"])}')