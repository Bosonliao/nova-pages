import urllib.request, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = 'https://upload.wikimedia.org/wikipedia/zh/e/ed/Chattime_logo.svg'
req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
data = urllib.request.urlopen(req, timeout=10).read()
content = data.decode('utf-8')
print('Size:', len(data))
fills = re.findall(r'fill="([^"\'>]+)"', content)
print('Fills:', set(fills))
print()
print(content[:2000])
