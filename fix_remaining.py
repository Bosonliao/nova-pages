import json, sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 1. taichung -> taipei (大安區 lat>25.0 = 台北大安區)
tc = json.load(open('data/taichung.json','r',encoding='utf-8'))
tp = json.load(open('data/taipei.json','r',encoding='utf-8'))

moved_to_taipei = []
tc_food = []
for item in tc['food']:
    if isinstance(item, dict) and item.get('lat') and item.get('lat', 0) > 25.0 and item.get('area') == '大安':
        moved_to_taipei.append(item)
    else:
        tc_food.append(item)
tc['food'] = tc_food
tp['food'].extend(moved_to_taipei)

print(f'taichung -> taipei: {len(moved_to_taipei)} items')
for m in moved_to_taipei:
    nm = m.get('name','')[:30]
    print(f'  {nm} lat={m.get("lat")}')

with open('data/taichung.json.tmp','w',encoding='utf-8') as f:
    json.dump(tc, f, ensure_ascii=False, indent=2)
os.replace('data/taichung.json.tmp', 'data/taichung.json')

with open('data/taipei.json.tmp','w',encoding='utf-8') as f:
    json.dump(tp, f, ensure_ascii=False, indent=2)
os.replace('data/taipei.json.tmp', 'data/taipei.json')

# 2. kaohsiung -> taoyuan (內壢/永安 lat>24.9 = 桃園)
kh = json.load(open('data/kaohsiung.json','r',encoding='utf-8'))
ty = json.load(open('data/taoyuan.json','r',encoding='utf-8'))

moved_to_taoyuan = []
kh_food = []
for item in kh['food']:
    if isinstance(item, dict) and item.get('lat') and item.get('lat', 0) > 24.9 and item.get('area','') in ['內門','永安']:
        moved_to_taoyuan.append(item)
    else:
        kh_food.append(item)
kh['food'] = kh_food
ty['food'].extend(moved_to_taoyuan)

print(f'kaohsiung -> taoyuan: {len(moved_to_taoyuan)} items')
for m in moved_to_taoyuan:
    nm = m.get('name','')[:30]
    print(f'  {nm} lat={m.get("lat")} area={m.get("area")}')

with open('data/kaohsiung.json.tmp','w',encoding='utf-8') as f:
    json.dump(kh, f, ensure_ascii=False, indent=2)
os.replace('data/kaohsiung.json.tmp', 'data/kaohsiung.json')

with open('data/taoyuan.json.tmp','w',encoding='utf-8') as f:
    json.dump(ty, f, ensure_ascii=False, indent=2)
os.replace('data/taoyuan.json.tmp', 'data/taoyuan.json')

# 3. hsinchu -> tainan (lat<23.1 = 台南)
hc = json.load(open('data/hsinchu.json','r',encoding='utf-8'))
tn = json.load(open('data/tainan.json','r',encoding='utf-8'))

moved_to_tainan = []
hc_food = []
for item in hc['food']:
    if isinstance(item, dict) and item.get('lat') and item.get('lat', 99) < 23.1:
        moved_to_tainan.append(item)
    else:
        hc_food.append(item)
hc['food'] = hc_food
tn['food'].extend(moved_to_tainan)

print(f'hsinchu -> tainan: {len(moved_to_tainan)} items')
for m in moved_to_tainan:
    nm = m.get('name','')[:30]
    print(f'  {nm} lat={m.get("lat")}')

with open('data/hsinchu.json.tmp','w',encoding='utf-8') as f:
    json.dump(hc, f, ensure_ascii=False, indent=2)
os.replace('data/hsinchu.json.tmp', 'data/hsinchu.json')

with open('data/tainan.json.tmp','w',encoding='utf-8') as f:
    json.dump(tn, f, ensure_ascii=False, indent=2)
os.replace('data/tainan.json.tmp', 'data/tainan.json')

# Summary
print()
print('=== Final counts ===')
for f in ['data/taipei.json','data/taichung.json','data/tainan.json','data/kaohsiung.json','data/taoyuan.json','data/hsinchu.json','data/chiayi.json']:
    d = json.load(open(f,'r',encoding='utf-8'))
    print(f'{f}: food={len(d.get("food",[]))}')