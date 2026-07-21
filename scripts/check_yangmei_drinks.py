import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])
drinks = [f for f in foods if any('飲品' in c for c in (f.get('categories') or []))]
yangmei = [d for d in drinks if d.get('area') == '楊梅區']
print(f'楊梅區飲料店: {len(yangmei)} 家')
for d in yangmei:
    print(f'  {d["name"]} | lat:{d.get("lat")} lng:{d.get("lng")} | {d.get("rating","?")}★ ({d.get("reviews","?")})')

print()
# Also check if 麻古 楊梅文化 exists anywhere
magu = [d for d in drinks if '麻古' in d.get('name','') and '楊梅' in d.get('name','')]
print(f'麻古楊梅: {len(magu)}')
for d in magu:
    print(f'  {d["name"]} | {d.get("area")} | lat:{d.get("lat")} lng:{d.get("lng")}')

print()
all_magu = [d for d in drinks if '麻古' in d.get('name','')]
print(f'所有麻古: {len(all_magu)}')
for d in all_magu:
    print(f'  {d["name"]} | {d.get("area")} | lat:{d.get("lat")} lng:{d.get("lng")}')
