import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = 'C:/Users/USER/.openclaw/workspace/nova-pages/data/tainan.json'
data = json.load(open(path, 'r', encoding='utf-8'))
for f in data['food']:
    if f['name'] == '文章牛肉湯 安平總店':
        d = f.get('dishes')
        print('Name:', f['name'])
        print('Dishes:', d)
        print('Type:', type(d[0]) if d else 'empty')
        break

for f in data['food']:
    if f['name'] == '麻豆阿蘭碗粿':
        d = f.get('dishes')
        print('Name:', f['name'])
        print('Dishes:', d)
        break