import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\USER\.openclaw\workspace\nova-pages\west-end-new-batch2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total entries: {len(data)}")
print(f"With ratings: {sum(1 for d in data if d['rating'] is not None)}")
print(f"Popular: {sum(1 for d in data if d['popular'])}")

# Check for duplicates within the batch
names = [d['name'] for d in data]
seen = set()
dups = []
for n in names:
    if n in seen:
        dups.append(n)
    seen.add(n)
if dups:
    print(f"DUPLICATES WITHIN BATCH: {dups}")
else:
    print("No duplicates within batch.")

# Cross-check against existing list
import re
with open(r'C:\Users\USER\.openclaw\workspace\nova-pages\west-end-brisbane.html', 'r', encoding='utf-8') as f:
    content = f.read()
existing_names = set(re.findall(r'name:\s*"([^"]+)"', content))

overlaps = [n for n in names if n in existing_names]
if overlaps:
    print(f"OVERLAPS WITH EXISTING LIST: {overlaps}")
else:
    print("No overlaps with existing list.")

print("\nAll entries:")
for d in data:
    r = f" ({d['rating']}, {d['reviews']})" if d['rating'] else ""
    p = " [POPULAR]" if d['popular'] else ""
    print(f"  {d['name']} - {d['cat']}/{d['tag']}{r}{p}")