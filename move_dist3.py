with open('taiwan-travel.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 夜市卡片：把 distBadge 從 nm-name 移到 nm-loc
old = "${distBadge(m.lat, m.lng)}<span class=\"card-actions\">"
new = "<span class=\"card-actions\">"
content = content.replace(old, new, 1)

old2 = "📍 ${m.city}${m.district} · ${m.location||''}</div>"
new2 = "📍 ${m.city}${m.district} · ${m.location||''} ${distBadge(m.lat, m.lng)}</div>"
content = content.replace(old2, new2, 1)

with open('taiwan-travel.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')