import re

with open('taiwan-travel.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 食物卡片：把 distBadge 從 name 行移到 food-tags 行
# 原本：${distBadge(f.lat, f.lng)}<span class="card-actions">
# 改成：<span class="card-actions">  （移除 distBadge）
# 原本：${michelinTag}${popularTag}${sstcTag}${cats}</div>
# 改成：${michelinTag}${popularTag}${sstcTag}${cats}${distBadge(f.lat, f.lng)}</div>

# 有兩處 food card（line 674 和 706）
old1 = '${distBadge(f.lat, f.lng)}<span class="card-actions">'
new1 = '<span class="card-actions">'
old1_esc = '${distBadge(f.lat, f.lng)}\\u003cspan class="card-actions"\\u003e'
new1_esc = '\\u003cspan class="card-actions"\\u003e'

old2 = '${michelinTag}${popularTag}${sstcTag}${cats}</div>'
new2 = '${michelinTag}${popularTag}${sstcTag}${cats}${distBadge(f.lat, f.lng)}</div>'

count = 0
# HTML 版本
c1 = content.count(old1)
content = content.replace(old1, new1)
count += c1
print(f'Food card name 行移除 distBadge: {c1}')

# escaped 版本
c1b = content.count(old1_esc)
content = content.replace(old1_esc, new1_esc)
count += c1b
print(f'Food card name 行移除 distBadge (escaped): {c1b}')

c2 = content.count(old2)
content = content.replace(old2, new2)
print(f'Food card tags 行加入 distBadge: {c2}')

# 伴手禮卡片也同樣處理 (s.lat, s.lng)
old3 = '${distBadge(s.lat, s.lng)}<span class="card-actions">'
new3 = '<span class="card-actions">'
old3_esc = '${distBadge(s.lat, s.lng)}\\u003cspan class="card-actions"\\u003e'
new3_esc = '\\u003cspan class="card-actions"\\u003e'

c3 = content.count(old3)
content = content.replace(old3, new3)
print(f'Souvenir card name 行移除 distBadge: {c3}')

c3b = content.count(old3_esc)
content = content.replace(old3_esc, new3_esc)
print(f'Souvenir card name 行移除 distBadge (escaped): {c3b}')

# 伴手禮的 tags 行 — 找看看格式
# 需要找到伴手禮的 tags 行
# 從 line 751 附近看
old4 = content[content.find('${distBadge(s.lat, s.lng)')-200:content.find('${distBadge(s.lat, s.lng)')+200] if '${distBadge(s.lat, s.lng)}' in content else 'NOT FOUND'

with open('taiwan-travel.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Saved.')