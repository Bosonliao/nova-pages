import urllib.request, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')

url = 'https://www.comebuy2002.com.tw'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')

# Find logo images
logos = re.findall(r'(?:src|href)="([^"]*(?:logo|icon|COME)[^"]*\.(?:png|jpg|svg|webp))"', html, re.I)
for l in logos:
    print(f'Found: {l}')

# Also check og:image
og = re.findall(r'og:image.*?content="([^"]*)"', html)
for o in og:
    print(f'OG: {o}')

# Check all img tags
imgs = re.findall(r'<img[^>]*src="([^"]*)"', html, re.I)
for i in imgs:
    if any(kw in i.lower() for kw in ['logo', 'comebuy', 'icon', 'brand']):
        print(f'IMG: {i}')
