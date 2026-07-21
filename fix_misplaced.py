import json, sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 從 taipei.json 移除新埔粄條大王
tp = json.load(open('data/taipei.json', 'r', encoding='utf-8'))
removed = None
for i, item in enumerate(tp['food']):
    if isinstance(item, dict) and item.get('name') == '新埔粄條大王':
        removed = tp['food'].pop(i)
        break
print(f'Removed from taipei.json: {removed["name"]}')
print(f'taipei.json food count: {len(tp["food"])}')

with open('data/taipei.json.tmp', 'w', encoding='utf-8') as f:
    json.dump(tp, f, ensure_ascii=False, indent=2)
os.replace('data/taipei.json.tmp', 'data/taipei.json')

# 加入 hsinchu.json
hc = json.load(open('data/hsinchu.json', 'r', encoding='utf-8'))
removed['area'] = '新埔鎮'
hc['food'].append(removed)
print(f'Added to hsinchu.json: {removed["name"]}')
print(f'hsinchu.json food count: {len(hc["food"])}')

with open('data/hsinchu.json.tmp', 'w', encoding='utf-8') as f:
    json.dump(hc, f, ensure_ascii=False, indent=2)
os.replace('data/hsinchu.json.tmp', 'data/hsinchu.json')

print('Done!')