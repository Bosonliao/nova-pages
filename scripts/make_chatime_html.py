import urllib.request, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = 'https://upload.wikimedia.org/wikipedia/zh/e/ed/Chattime_logo.svg'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
data = urllib.request.urlopen(req, timeout=10).read()
content = data.decode('utf-8')
content = content.replace('.st0{fill:#FFFFFF;}', '.st0{fill:#5B2C87;}')

html = '<html><body style="margin:0;padding:10px;background:white;"><div>' + content + '</div></body></html>'
with open('_chatime_logo.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('OK - HTML created')
