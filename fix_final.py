#!/usr/bin/env python3
"""
修正剩餘的真正分類錯誤
只修 HIGH 確定錯誤的，不動邊界城鎮
"""
import json, sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DATA = 'data'

def load(fname):
    with open(os.path.join(DATA, fname), 'r', encoding='utf-8') as f:
        return json.load(f)

def save(fname, data):
    tmp = os.path.join(DATA, fname + '.tmp')
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, os.path.join(DATA, fname))

moves = []

# 1. miaoli 公館鄉 lat>25.0 = 台北公館 (5筆)
miaoli = load('miaoli.json')
taipei = load('taipei.json')
miaoli_food = []
for item in miaoli['food']:
    if isinstance(item, dict) and item.get('lat', 0) > 25.0 and item.get('area') == '公館鄉':
        taipei['food'].append(item)
        moves.append(('miaoli', 'taipei', item.get('name','')[:25], item.get('lat')))
    else:
        miaoli_food.append(item)
miaoli['food'] = miaoli_food

# 2. nantou 信義鄉 lat>25.0 = 台北信義區 (4筆)
nantou = load('nantou.json')
nantou_food = []
for item in nantou['food']:
    if isinstance(item, dict) and item.get('lat', 0) > 25.0 and item.get('area') == '信義鄉':
        taipei['food'].append(item)
        moves.append(('nantou', 'taipei', item.get('name','')[:25], item.get('lat')))
    else:
        nantou_food.append(item)
nantou['food'] = nantou_food

# 3. pingtung 高樹鄉/里港鄉 lat>22.8 = 高雄美濃附近 (3筆)
pingtung = load('pingtung.json')
kaohsiung = load('kaohsiung.json')
pingtung_food = []
for item in pingtung['food']:
    if isinstance(item, dict) and item.get('area','') in ['高樹鄉','里港鄉'] and item.get('lat', 0) > 22.82:
        # 高樹鄉和里港鄉確實是屏東的，座標在22.8是正常的
        # 但如果 lat > 22.82 且靠近高雄，需要確認
        # 實際上高樹鄉 lat~22.82, 里港鄉 lat~22.82 這些是屏東沒錯
        # 腳本誤判，保留在屏東
        pingtung_food.append(item)
    else:
        pingtung_food.append(item)
pingtung['food'] = pingtung_food

# 4. changhua 埔心鄉 lat=24.91 = 桃園埔心 (1筆)
changhua = load('changhua.json')
taoyuan = load('taoyuan.json')
changhua_food = []
for item in changhua['food']:
    if isinstance(item, dict) and item.get('lat', 0) > 24.85 and '埔心' in item.get('name',''):
        taoyuan['food'].append(item)
        moves.append(('changhua', 'taoyuan', item.get('name','')[:25], item.get('lat')))
    else:
        changhua_food.append(item)
changhua['food'] = changhua_food

# 5. tainan 安平 lat=22.63 = 其實是台南安平沒錯，但腳本說 kaohsiung
# 台南安平 lat~22.99, 這個 lat=22.63 太低了，查一下
tainan = load('tainan.json')
tainan_food = []
for item in tainan['food']:
    if isinstance(item, dict) and item.get('lat', 99) < 22.7 and '安平' in item.get('area',''):
        # lat=22.63 是高雄的座標，但店名說台南安平店
        # 這可能是連鎖店的高雄分店被標錯
        # 先保留，標記為可疑
        print(f'SUSPECT: {item.get("name","")[:30]} lat={item.get("lat")} area={item.get("area")}')
        tainan_food.append(item)
    else:
        tainan_food.append(item)
tainan['food'] = tainan_food

# 6. miaoli 竹南/頭份 lat~24.7 = 這些確實是苗栗的，不動
# 但腳本說 hsinchu，因為座標靠近新竹。保留在苗栗。

# 7. hsinchu 尖石鄉 = 確實是新竹尖石鄉，座標靠近桃園是因為山區。不動。

# Save all
save('miaoli.json', miaoli)
save('nantou.json', nantou)
save('taipei.json', taipei)
save('pingtung.json', pingtung)
save('kaohsiung.json', kaohsiung)
save('changhua.json', changhua)
save('taoyuan.json', taoyuan)
save('tainan.json', tainan)

print(f'\nTotal moves: {len(moves)}')
for src, dst, name, lat in moves:
    print(f'  {src} -> {dst}: {name} lat={lat}')

print('\n=== Final counts ===')
for f in ['miaoli.json','nantou.json','taipei.json','changhua.json','taoyuan.json']:
    d = load(f)
    print(f'{f}: food={len(d.get("food",[]))}')