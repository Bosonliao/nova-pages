import csv

path = r'C:\Users\USER\.openclaw\workspace\nova-pages\data\restaurants.csv'
rows = []
with open(path, 'r', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    for row in reader:
        if row.get('county','') == '桃園' and row.get('district','') == '楊梅區' and row.get('name','') == '大苑子' and not row.get('business_hours','').strip():
            row['business_hours'] = '已打烊 · 開始營業時間：週日10:00'
            print(f"Updated: {row['name']} -> {row['business_hours']}")
        rows.append(row)

with open(path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# 確認楊梅區全部都有營業時間了
yangmei = [r for r in rows if r.get('county','') == '桃園' and r.get('district','') == '楊梅區']
has = sum(1 for r in yangmei if r.get('business_hours','').strip())
print(f"\n楊梅區: {has}/{len(yangmei)} 筆有營業時間")