import json

path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/yunlin.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

food = data.get('food', [])

# Dishes for 千巧谷牛樂園牧場
qianqiaogu_dishes = [
    {"name": "窯烤披薩", "description": "招牌必吃，現點現做手工窯烤，切口偏小適合孩子"},
    {"name": "鮮奶酪", "description": "榮獲十大伴手禮，崙背鮮奶製成"},
    {"name": "鮮奶乳酪蛋糕", "description": "千巧谷烘培坊招牌伴手禮，使用崙背酪農區直送鮮乳"},
    {"name": "焦糖布蕾堡", "description": "必買伴手禮，鮮奶系列烘焙品"},
    {"name": "鮮奶茶", "description": "彩繪屋販售，使用崙背在地鮮奶"},
    {"name": "鮮奶霜淇淋", "description": "鮮奶製成的霜淇淋，天氣不冷來一根"},
    {"name": "國王蛋糕", "description": "千巧谷烘培坊創意麵包伴手禮"},
    {"name": "崙背鮮奶派", "description": "鮮奶系列伴手禮，崙背酪農區直送鮮乳"}
]

# Dishes for 西堤牛排 - known chain
saite_dishes = [
    {"name": "法式香煎鴨胸", "description": "西堤招牌前菜，鴨胸肉質鮮嫩"},
    {"name": "原塊牛排", "description": "西堤主餐招牌，原塊現烤牛排"},
    {"name": "杏鮑菇南瓜濃湯", "description": "經典開胃湯品"},
    {"name": "蒜香菲力牛排", "description": "人氣主餐，菲力搭配蒜香"},
    {"name": "德式豬腳", "description": "酥脆德式豬腳，外脆內嫩"}
]

# Dishes for 色鼎燒肉
seding_dishes = [
    {"name": "和牛燒肉", "description": "招牌頂級和牛，現烤薄片"},
    {"name": "鹽蔥牛舌", "description": "牛舌搭配鹽蔥，口感Q彈"},
    {"name": "特選五花肉", "description": "燒肉必點，油脂豐富"},
    {"name": "霜降豬肉", "description": "店家人氣選擇"},
    {"name": "雞腿肉", "description": "醬燒雞腿肉，多汁入味"}
]

# Dishes for 嗑肉石鍋
kerou_dishes = [
    {"name": "石鍋拌飯", "description": "招牌石鍋拌飯，鍋巴焦香"},
    {"name": "韓式部隊鍋", "description": "石鍋部隊鍋，料多味美"},
    {"name": "起司燒肉石鍋", "description": "燒肉搭配起司的石鍋料理"}
]

# Dishes for 新千葉火鍋
xinqianye_dishes = [
    {"name": "蒙古清香鍋", "description": "招牌湯底，多種香料熬製"},
    {"name": "和牛火鍋", "description": "頂級和牛搭配火鍋"},
    {"name": "手切鮮牛肉", "description": "現切鮮牛肉盤"}
]

# Dishes for 野川堂秘境鍋物
yechuan_dishes = [
    {"name": "秘境牛奶鍋", "description": "招牌牛奶鍋，鮮奶熬製湯頭"},
    {"name": "和牛鍋物", "description": "頂級和牛搭配火鍋"},
    {"name": "石頭火鍋", "description": "先炒後煮的石頭火鍋"}
]

dish_map = {
    "千巧谷牛樂園牧場": qianqiaogu_dishes,
    "西堤牛排 斗六萬家福店": saite_dishes,
    "色鼎燒肉斗六店": seding_dishes,
    "嗑肉石鍋斗六上海店(二代店)": kerou_dishes,
    "新千葉火鍋-斗六店": xinqianye_dishes,
    "色鼎燒肉虎尾店": seding_dishes,
    "野川堂秘境鍋物 虎尾店": yechuan_dishes,
}

updated = 0
for r in food:
    name = r.get('name', '')
    if name in dish_map and not r.get('dishes'):
        r['dishes'] = dish_map[name]
        updated += 1
        print(f'Updated: {name} ({len(dish_map[name])} dishes)')

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\nTotal updated: {updated}')
print(f'File saved')
