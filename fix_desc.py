import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('taiwan-travel.html', encoding='utf-8') as f:
    html = f.read()

old = "${d.desc}"
new = "${d.description||''}"
count = html.count(old)
print(f"Found {count} occurrences of d.desc")

html = html.replace(old, new)
remaining = html.count("${d.desc}")
print(f"After: {remaining} occurrences remaining")

with open('taiwan-travel.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Done!")
