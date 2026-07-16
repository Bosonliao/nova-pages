import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

saves = []

# === TAIPEI ===
path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/taipei.json'
data = json.load(open(path, 'r', encoding='utf-8'))
for f in data['food']:
    n = f['name']
    if n == '西門町阿宗麵線':
        f['dishes'] = ['阿宗麵線', '綜合麵線', '大腸麵線', '蒜泥麵線', '辣椒麵線']
        saves.append(n)
    elif n == '金峰魯肉飯':
        f['dishes'] = ['魯肉飯', '雞肉飯', '控肉飯', '白菜魯', '油豆腐']
        saves.append(n)
    elif n == '熊一頂級燒肉-西門店':
        f['dishes'] = ['美國Choice牛小排', '豬梅花', '雞腿肉', '霜淇淋', '哈根達斯冰淇淋']
        saves.append(n)
    elif n == '今日魚市-南京店-原丼賞和食':
        f['dishes'] = ['海鮮丼', '生魚片拼盤', '鮭魚親子丼', '味噌湯', '握壽司']
        saves.append(n)
    elif n == '林美如 海鮮 熱炒 燒烤 酒場':
        f['dishes'] = ['熱炒海鮮', '烤鮮蚵', '炒牛肉', '三杯雞', '生啤酒']
        saves.append(n)
    elif '金洹苑' in n:
        f['dishes'] = ['日本和牛', '海鮮拼盤', '牛小排', '豬梅花', '霜淇淋']
        saves.append(n)
json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# === NEW TAIPEI ===
path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/newtaipei.json'
data = json.load(open(path, 'r', encoding='utf-8'))
for f in data['food']:
    n = f['name']
    if n == '三重今大滷肉飯':
        f['dishes'] = ['滷肉飯', '雞肉飯', '控肉飯', '白菜魯', '油豆腐']
        saves.append(n)
    elif n == '今大魯肉飯':
        f['dishes'] = ['滷肉飯', '雞肉飯', '控肉飯', '白菜魯', '油豆腐']
        saves.append(n)
    elif n == '我家牛排 中和旗艦店':
        f['dishes'] = ['牛排', '豬排', '雞排', '酥皮濃湯', '自助吧']
        saves.append(n)
    elif n == '吉哆火鍋百匯':
        f['dishes'] = ['麻辣鍋', '石頭火鍋', '涮涮鍋', '海鮮拼盤', '冰淇淋']
        saves.append(n)
    elif n == '水灣餐廳 榕堤店':
        f['dishes'] = ['景觀下午茶', '火鍋', '鬆餅', '咖啡', '海鮮拼盤']
        saves.append(n)
    elif '焼肉スマイル' in n and '樹林' in n:
        f['dishes'] = ['牛小排', '豬梅花', '雞腿肉', '松阪豬', '霜淇淋']
        saves.append(n)
json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# === TAICHUNG ===
path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/taichung.json'
data = json.load(open(path, 'r', encoding='utf-8'))
for f in data['food']:
    n = f['name']
    if n == '茶六燒肉堂 新朝富店':
        f['dishes'] = ['豪華全牛套餐', '美國安格斯牛小排', '澳洲和牛牛舌', '松阪豚', '哈根達斯冰淇淋']
        saves.append(n)
    elif n == '三山燒肉 文心店':
        f['dishes'] = ['牛小排', '豬梅花', '雞腿肉', '松阪豬', '海鮮拼盤']
        saves.append(n)
    elif n == 'les aqua 水相餐聚苑':
        f['dishes'] = ['海鮮百匯', '生蠔', '牛排', '握壽司', '甜點拼盤']
        saves.append(n)
    elif n == '泰丘鍋物':
        f['dishes'] = ['泰式鍋底', '海鮮拼盤', '牛肉盤', '手工丸子', '蔬菜自助吧']
        saves.append(n)
    elif '嵐山熟成牛' in n:
        f['dishes'] = ['熟成牛炸豬排', '熟成牛菲力', '咖哩飯', '味噌湯', '高麗菜絲']
        saves.append(n)
    elif n == '淇里思崇德店':
        f['dishes'] = ['泰式奶茶', '打拋豬', '綠咖哩雞', '摩摩喳喳', '月亮蝦餅']
        saves.append(n)
json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# === KAOHSIUNG ===
path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/kaohsiung.json'
data = json.load(open(path, 'r', encoding='utf-8'))
for f in data['food']:
    n = f['name']
    if '汕頭泉成沙茶火鍋' in n:
        f['dishes'] = ['沙茶火鍋', '牛肉盤', '魚餃', '手工丸子', '凍豆腐']
        saves.append(n)
    elif '田季發爺燒肉' in n:
        f['dishes'] = ['牛小排', '豬梅花', '雞腿肉', '松阪豬', '冰淇淋']
        saves.append(n)
    elif n == '森森燒肉 高雄中正店':
        f['dishes'] = ['美國Choice牛小排', '豬梅花', '雞腿肉', '北海道干貝', '霜淇淋']
        saves.append(n)
json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# === TAINAN ===
path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/tainan.json'
data = json.load(open(path, 'r', encoding='utf-8'))
for f in data['food']:
    n = f['name']
    if '桂田酒店' in n:
        f['dishes'] = ['生蠔', '牛排', '握壽司', '螃蟹', '哈根達斯冰淇淋']
        saves.append(n)
    elif 'TASTY西堤牛排 仁德' in n:
        f['dishes'] = ['牛排', '鴨胸', '沙拉', '酥皮濃湯', '甜點']
        saves.append(n)
json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# === KEELUNG ===
path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/keelung.json'
data = json.load(open(path, 'r', encoding='utf-8'))
for f in data['food']:
    n = f['name']
    if '西堤牛排 基隆' in n:
        f['dishes'] = ['牛排', '鴨胸', '沙拉', '酥皮濃湯', '甜點']
        saves.append(n)
json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# === YILAN ===
path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/yilan.json'
data = json.load(open(path, 'r', encoding='utf-8'))
for f in data['food']:
    n = f['name']
    if n == '柯氏蔥油餅':
        f['dishes'] = ['蔥油餅', '加蛋蔥油餅', '蔥油餅加辣', '蔥油餅加九層塔']
        saves.append(n)
    elif '火山爆發雞' in n:
        f['dishes'] = ['火山爆發雞', '雞油飯', '烤雞翅', '雞湯', '雞皮']
        saves.append(n)
    elif '西堤牛排 宜蘭' in n:
        f['dishes'] = ['牛排', '鴨胸', '沙拉', '酥皮濃湯', '甜點']
        saves.append(n)
json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# === CHANGHUA ===
path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/changhua.json'
data = json.load(open(path, 'r', encoding='utf-8'))
for f in data['food']:
    n = f['name']
    if '阿璋肉圓' in n:
        f['dishes'] = ['肉圓', '排骨湯', '龍骨髓湯', '糯米腸', '肉粽']
        saves.append(n)
    elif '西堤牛排 彰化' in n:
        f['dishes'] = ['牛排', '鴨胸', '沙拉', '酥皮濃湯', '甜點']
        saves.append(n)
json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# === HSINCHU ===
path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/hsinchu.json'
data = json.load(open(path, 'r', encoding='utf-8'))
for f in data['food']:
    n = f['name']
    if '海底撈火鍋 新竹' in n:
        f['dishes'] = ['番茄鍋底', '麻辣鍋底', '撈麵', '蝦滑', '肥牛']
        saves.append(n)
    elif '西堤牛排 新竹' in n:
        f['dishes'] = ['牛排', '鴨胸', '沙拉', '酥皮濃湯', '甜點']
        saves.append(n)
    elif n == '柒伍無煙燒肉':
        f['dishes'] = ['牛小排', '豬梅花', '雞腿肉', '松阪豬', '海鮮拼盤']
        saves.append(n)
json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# === TAOYUAN ===
path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/taoyuan.json'
data = json.load(open(path, 'r', encoding='utf-8'))
for f in data['food']:
    n = f['name']
    if '石頭燒烤-桃園' in n:
        f['dishes'] = ['石頭火鍋', '沙茶牛肉', '魚餃', '蛋餃', '豬肉片']
        saves.append(n)
    elif n == '武田信玄':
        f['dishes'] = ['拉麵', '煎餃', '叉燒飯', '味噌湯', '日式炸雞']
        saves.append(n)
    elif '藝奇' in n:
        f['dishes'] = ['生魚片拼盤', '握壽司', '烤物', '茶碗蒸', '甜點']
        saves.append(n)
json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# === MIAOLI ===
path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/miaoli.json'
data = json.load(open(path, 'r', encoding='utf-8'))
for f in data['food']:
    n = f['name']
    if '泰安洗水坑' in n:
        f['dishes'] = ['手工豆腐', '豆干', '豆漿', '豆腐冰', '臭豆腐']
        saves.append(n)
    elif '西堤牛排 頭份' in n:
        f['dishes'] = ['牛排', '鴨胸', '沙拉', '酥皮濃湯', '甜點']
        saves.append(n)
json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# === PINGTUNG ===
path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/pingtung.json'
data = json.load(open(path, 'r', encoding='utf-8'))
for f in data['food']:
    n = f['name']
    if 'TASTY西堤牛排 屏東' in n:
        f['dishes'] = ['牛排', '鴨胸', '沙拉', '酥皮濃湯', '甜點']
        saves.append(n)
json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# === HUALIEN ===
path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/hualien.json'
data = json.load(open(path, 'r', encoding='utf-8'))
for f in data['food']:
    n = f['name']
    if '立川漁場' in n:
        f['dishes'] = ['黃金蜆', '蜆精', '炒蜆仔', '蜆仔湯', '黃金蜆餅乾']
        saves.append(n)
json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# Skip non-restaurant entries (malls, streets, markets, cultural parks)
skip_entries = [
    ('kaohsiung', ['夢時代購物中心/統一時代百貨高雄店']),
    ('newtaipei', ['金山老街', '鶯歌陶瓷老街', '鶯歌陶瓷老街麵線']),
    ('taichung', ['一中街必吃']),
    ('pingtung', ['東港漁港漁產品直銷中心（華僑市場）', '六堆客家文化園區']),
    ('chiayi', ['布袋高跟鞋教堂周邊小吃']),
]
for county, names in skip_entries:
    path2 = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/' + county + '.json'
    d2 = json.load(open(path2, 'r', encoding='utf-8'))
    for f in d2['food']:
        if f['name'] in names:
            f['dishes'] = []
            saves.append('SKIP:' + f['name'])
    json.dump(d2, open(path2, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print('Total processed: ' + str(len(saves)))
for s in saves:
    print('  - ' + s)