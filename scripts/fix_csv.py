import csv

path = r'C:\Users\USER\.openclaw\workspace\nova-pages\data\restaurants.csv'

# 讀取
rows = []
with open(path, 'r', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    for row in reader:
        rows.append(row)

print(f"Fields: {fieldnames}")
print(f"Total: {len(rows)}")

# 檢查 business_hours 和 source 的值
for r in rows[:5]:
    print(f"  name={r.get('name','')}, business_hours={r.get('business_hours','')}, source={r.get('source','')}")

# 修正：把 business_hours 的值移回 source，business_hours 設空
fixed = 0
for r in rows:
    bh = r.get('business_hours', '').strip()
    src = r.get('source', '').strip()
    # 如果 business_hours 有值但 source 是空的，表示值跑位了
    if bh and not src:
        r['source'] = bh
        r['business_hours'] = ''
        fixed += 1
    # 如果 business_hours 看起來像是 source 值（manual/agy/google_places 等）
    elif bh and bh in ['manual', 'agy', 'google_places', 'google_geocoding', 'government', 'chatgpt']:
        r['source'] = bh
        r['business_hours'] = ''
        fixed += 1

print(f"\nFixed {fixed} rows")

# 寫回
with open(path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# 統計
empty = sum(1 for r in rows if not r.get('business_hours', '').strip())
has = sum(1 for r in rows if r.get('business_hours', '').strip())
print(f"Empty hours: {empty}, Has hours: {has}")