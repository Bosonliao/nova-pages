import json, glob, os

# 根據店名關鍵字生成合理描述
def make_desc(name, category):
    name_lower = name.lower()
    if any(k in name for k in ['燒肉','燒烤','烤肉','Yakiniku','yakiniku']):
        if '吃到飽' in name:
            return '超人氣燒肉吃到飽，多種肉品選擇，讓你烤得過癮'
        return '人氣燒肉餐廳，提供多種肉品與配菜，適合聚餐'
    if any(k in name for k in ['火鍋','鍋物','涮涮鍋','涮鍋','shabu','鍋吃到飽']):
        if '吃到飽' in name:
            return '超人氣火鍋吃到飽，多種湯底與食材選擇'
        return '人氣火鍋餐廳，提供新鮮食材與多種湯底'
    if any(k in name for k in ['牛排','steak','Steak']):
        return '人氣牛排餐廳，提供多種熟成牛排與配餐'
    if any(k in name for k in ['串燒','居酒屋']):
        return '人氣串燒居酒屋，提供多種烤串與酒飲'
    if any(k in name for k in ['雞','烤雞','甕雞']):
        return '超人氣烤雞專賣，外酥內嫩的經典美味'
    if any(k in name for k in ['海鮮','海產','生魚片','sashimi','Sashimi']):
        return '新鮮海鮮料理專賣，超人氣的海味選擇'
    if any(k in name for k in ['壽司','sushi','Sushi','日本料理']):
        return '人氣日本料理餐廳，提供新鮮壽司與日式料理'
    if any(k in name for k in ['丼飯','don','Don']):
        return '人氣丼飯專賣，提供多種豐盛的日式丼飯'
    if any(k in name for k in ['台菜','臺菜','熱炒']):
        return '人氣台菜餐廳，提供道地台灣料理與熱炒'
    if any(k in name for k in ['什鍋','鍋']):
        return '人氣鍋物餐廳，提供多種湯底與新鮮食材'
    if any(k in name for k in ['咖啡','cafe','Cafe','咖啡廳']):
        return '人氣咖啡廳，提供咖啡、輕食與甜點'
    # 預設：根據 category
    if category:
        return f'超人氣{category}餐廳，提供多樣化的美味料理選擇'
    return '超人氣餐廳，提供多樣化的美味料理選擇'

count = 0
for f in glob.glob('data/*.json'):
    if f.endswith('meta.json') or f.endswith('nightmarkets.json'): continue
    with open(f, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    modified = False
    for key in ['food','foods','restaurants']:
        items = data.get(key, [])
        for item in items:
            desc = item.get('description','')
            if desc == '新鮮海鮮料理專賣，超人氣的海味選擇':
                name = item.get('name','')
                cat = item.get('category','') or item.get('cuisine','') or item.get('tags','')
                if isinstance(cat, list):
                    cat = cat[0] if cat else ''
                new_desc = make_desc(name, cat)
                item['description'] = new_desc
                modified = True
                count += 1
                print(f'{os.path.basename(f)}: {name}')
                print(f'  -> {new_desc}')
    if modified:
        with open(f, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)

print(f'\nFixed {count} items')