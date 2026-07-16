"""
菜色補充批次處理 v2
直接用 web_fetch 抓食記網站搜尋結果，提取菜色
"""
import json, os, sys, io, re, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data_dir = 'C:/Users/USER/.openclaw/workspace/nova-pages/data'

skip_keywords = ['百貨', '購物中心', '夜市', '市場', '商商', 'outlet', 'Outlet', '美食街',
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
                        'county': county,
                        'categories': r.get('categories', []),
                        'reviews': r.get('reviews', 0)
                    })
        except:
            pass

all_need.sort(key=lambda x: x.get('reviews') or 0, reverse=True)

# 輸出前 30 家供 Nova 逐家搜尋
print(f'TOTAL: {len(all_need)}')
for i, r in enumerate(all_need[:30]):
    print(f'{i+1}\t{r["name"]}\t{r["county"]}\t{r["area"]}\t{",".join(r["categories"])}')