import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\USER\.openclaw\workspace\nova-pages\west-end-brisbane.html', 'r', encoding='utf-8') as f:
    content = f.read()

names = re.findall(r'name:\s*"([^"]+)"', content)
unique_names = sorted(set(names))
print(f"Total: {len(unique_names)}")
for n in unique_names:
    print(n)