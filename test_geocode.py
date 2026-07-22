#!/usr/bin/env python3
"""皜祈岫 Geocoding API ?臬?舐"""
import json, sys, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

# 霈 API Key
with open(r'C:\Users\USER\.openclaw\secrets\google_maps_api.env', 'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith('GOOGLE_MAPS_API_KEY='):
            API_KEY = line.split('=', 1)[1].strip()
            break

print(f'Key: {API_KEY[:15]}...{API_KEY[-4:]}')

# 皜祈岫?亥岷
query = 'Taipei 101 ?啁'
url = 'https://maps.googleapis.com/maps/api/geocode/json'
params = {'address': query, 'key': API_KEY, 'language': 'zh-TW'}
full_url = f'{url}?{urllib.parse.urlencode(params)}'

try:
    req = urllib.request.Request(full_url)
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    
    print(f'Status: {data["status"]}')
    if data.get('error_message'):
        print(f'Error: {data["error_message"]}')
    if data.get('results'):
        loc = data['results'][0]['geometry']['location']
        print(f'Lat/Lng: {loc["lat"]}, {loc["lng"]}')
        print(f'Address: {data["results"][0]["formatted_address"]}')
    else:
        print('No results')
except Exception as e:
    print(f'Exception: {e}')
