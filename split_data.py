import json, os

# Process both zh and ja
for lang_file, prefix in [('data-zh.json', ''), ('data-ja.json', '')]:
    with open(lang_file, encoding='utf-8') as f:
        data = json.load(f)
    
    CITY_MAP = {
        '基隆': 'keelung', '台北': 'taipei', '新北': 'newtaipei',
        '宜蘭': 'yilan', '桃園': 'taoyuan', '新竹': 'hsinchu',
        '苗栗': 'miaoli', '台中': 'taichung', '南投': 'nantou',
        '彰化': 'changhua', '雲林': 'yunlin', '嘉義': 'chiayi',
        '台南': 'tainan', '高雄': 'kaohsiung', '屏東': 'pingtung',
        '花蓮': 'hualien', '台東': 'taitung', '澎湖': 'penghu',
        '金馬': 'kinmen',
    }
    
    subdir = f'data-ja' if lang_file == 'data-ja.json' else 'data'
    os.makedirs(subdir, exist_ok=True)
    
    # Clear old files
    for f in os.listdir(subdir):
        if f.endswith('.json'):
            os.remove(f'{subdir}/{f}')
    
    for city, d in data.items():
        if city.startswith('_') or city == 'nightmarkets':
            continue
        en = CITY_MAP.get(city, city)
        with open(f'{subdir}/{en}.json', 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, separators=(',', ':'))
    
    if 'nightmarkets' in data:
        with open(f'{subdir}/nightmarkets.json', 'w', encoding='utf-8') as f:
            json.dump(data['nightmarkets'], f, ensure_ascii=False, separators=(',', ':'))
    
    meta = {'_updatedAt': data.get('_updatedAt', '')}
    with open(f'{subdir}/meta.json', 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, separators=(',', ':'))
    
    with open(f'{subdir}/cities.json', 'w', encoding='utf-8') as f:
        json.dump(CITY_MAP, f, ensure_ascii=False, separators=(',', ':'))
    
    print(f'{lang_file} -> {subdir}/: {len(os.listdir(subdir))} files')
