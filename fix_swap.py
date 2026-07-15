import json, sys
sys.stdout.reconfigure(encoding='utf-8')
data = json.load(open('data-zh.json', encoding='utf-8'))

foods = data['台北']['food']

# Fix: move 小王煮瓜 dishes from idx 29 to idx 30, and give idx 29 correct 醉楓園 dishes
xiaowang_dishes = foods[29].get('dishes', [])

# 醉楓園小館 correct dishes
zuifeng_dishes = [
    {"name": "芋泥香酥鴨", "desc": "家族傳承粵菜招牌，芋泥裹鴨肉炸至金黃酥脆"},
    {"name": "當紅炸子雞", "desc": "脆皮雞皮脆肉嫩多汁，彭家手藝傳統粵式炸雞"},
    {"name": "瓊山豆腐", "desc": "功夫粵菜豆腐料理，滑嫩入味清甜鮮香"}
]

# Set idx 29 (醉楓園小館) to correct dishes
foods[29]['dishes'] = zuifeng_dishes

# Set idx 30 (小王煮瓜) to 小王煮瓜 dishes
foods[30]['dishes'] = xiaowang_dishes

# Also fix idx 28 (天下三絕) - it's a duplicate of idx 3 (天下三絕麵食館)
# But since they're separate entries, the dishes are fine

with open('data-zh.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Fixed!')
print('idx 29:', foods[29]['name'], '->', [d['name'] for d in foods[29]['dishes']])
print('idx 30:', foods[30]['name'], '->', [d['name'] for d in foods[30]['dishes']])