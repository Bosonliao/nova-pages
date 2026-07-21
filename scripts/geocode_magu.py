import urllib.request, json, sys, io, urllib.parse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
addr = '桃園市楊梅區文化街167號'
url = 'https://nominatim.openstreetmap.org/search?q=' + urllib.parse.quote(addr) + '&format=json&limit=1'
req = urllib.request.Request(url, headers={'User-Agent': 'nova-bot/1.0'})
try:
    data = json.loads(urllib.request.urlopen(req, timeout=10).read())
    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
        print(f'lat: {lat}, lng: {lon}')
    else:
        print('No result from Nominatim')
except Exception as e:
    print(f'Error: {e}')
