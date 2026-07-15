"""找出下一個沒有菜色的餐廳，傳回名稱和基本資訊"""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/yunlin.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

food = data.get('food', [])
need = [r for r in food if not r.get('dishes')]
need.sort(key=lambda x: x.get('reviews', 0), reverse=True)

if not need:
    print('ALL_DONE')
    sys.exit(0)

r = need[0]
print(f'NEXT_RESTAURANT:{r.get("name","")}')
print(f'AREA:{r.get("area","")}')
print(f'REVIEWS:{r.get("reviews",0)}')
print(f'REMAINING:{len(need)}')
