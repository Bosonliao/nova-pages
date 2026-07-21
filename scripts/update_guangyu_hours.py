import csv

path = r'C:\Users\USER\.openclaw\workspace\nova-pages\data\restaurants.csv'
rows = []
with open(path, 'r', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    for row in reader:
        if row.get('name','') == '光嶼咖啡':
            row['business_hours'] = '週一公休；週二至週日 11:30-18:00'
            print(f"Updated: {row['name']} -> {row['business_hours']}")
        rows.append(row)

with open(path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
print("Done")