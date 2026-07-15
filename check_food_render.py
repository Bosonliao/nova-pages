import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open('data/taipei.json', encoding='utf-8') as f:
    d = json.load(f)
food = d['food']

# Measure actual HTML size for 100 cards
total_html = '<div>'
for r in food[:100]:
    total_html += '<div class=food-card>'
    total_html += '<div class=name>' + r.get('name','') + '</div>'
    total_html += '<div class=desc>' + r.get('description','') + '</div>'
    for d2 in r.get('dishes', []):
        if isinstance(d2, dict):
            total_html += '<div class=dish>' + d2.get('name','') + ' ' + d2.get('description','') + '</div>'
    total_html += '</div>'
total_html += '</div>'

size_100 = len(total_html.encode('utf-8'))
print(f'100 cards: {size_100 // 1024} KB')
print(f'1271 cards estimate: {size_100 * 1271 // 100 // 1024} KB')

# Check the actual renderTab food section in the HTML
with open('taiwan-travel.html', encoding='utf-8') as f:
    html = f.read()
start = html.find("if(currentTab==='food')")
end = html.find("if(currentTab==='souvenirs')") 
if end < 0:
    end = html.find("if(currentTab", start + 20)
section = html[start:end]
print(f'\nrenderTab food section: {len(section)} chars')
print(f'Section ends with: ...{section[-100:]}')
