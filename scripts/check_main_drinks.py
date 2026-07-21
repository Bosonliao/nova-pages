import json, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Only check main county files used by the website
main_files = ['taipei','newtaipei','taoyuan','taichung','tainan','kaohsiung',
              'hsinchu','chiayi','changhua','pingtung','yunlin','miaoli',
              'nantou','yilan','hualien','taitung','keelung','penghu']

total_incomplete = 0
total_complete = 0
total_drinks = 0

for county in main_files:
    fpath = f'data/{county}.json'
    if not os.path.exists(fpath):
        continue
    data = json.load(open(fpath, 'r', encoding='utf-8'))
    foods = data.get('food', []) if isinstance(data, dict) else []
    
    incomplete = 0
    complete = 0
    for f in foods:
        cats = f.get('categories', [])
        if not any('飲品' in c or '飲料' in c for c in cats):
            continue
        total_drinks += 1
        name = f.get('name', '')
        has_branch = any(kw in name for kw in ['店', '站', '門市', '分店', '號'])
        if not has_branch:
            incomplete += 1
            total_incomplete += 1
        else:
            complete += 1
            total_complete += 1
    
    if incomplete > 0:
        print(f'{county}: {complete} complete, {incomplete} incomplete (total {complete+incomplete})')

print(f'\n=== 網站實際使用的資料 ===')
print(f'總飲料店: {total_drinks}')
print(f'有分店名: {total_complete}')
print(f'缺分店名: {total_incomplete}')
print(f'需補: {total_incomplete} 家')
