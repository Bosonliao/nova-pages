#!/usr/bin/env python3
"""
頛???Geocoding ?????亥岷??撖怠嚗??甈∟??券 JSON??"""
import json, os, sys, time, urllib.request, urllib.parse

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
API_KEY = 'REDACTED'
RATE = 0.15

def geocode(name, area, city_file):
    city = city_file.replace('.json', '')
    addr = ' '.join(p for p in [name, area, city, '?啁'] if p)
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s&language=zh-TW' % (
        urllib.parse.quote(addr), API_KEY)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'NovaLite/1.0'})
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read())
        if data['status'] == 'OK' and data['results']:
            loc = data['results'][0]['geometry']['location']
            return loc['lat'], loc['lng'], None
        return None, None, data['status']
    except Exception as e:
        return None, None, str(e)

def process_file(fname):
    fp = os.path.join(DATA_DIR, fname)
    with open(fp, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    fail = 0
    modified = False
    
    for cat in ['routes', 'spots', 'food', 'souvenirs']:
        if cat not in data or not isinstance(data[cat], list):
            continue
        for i, item in enumerate(data[cat]):
            if not isinstance(item, dict):
                continue
            if item.get('lat') is not None:
                continue
            
            name = item.get('name', '')
            area = item.get('area', '')
            
            lat, lng, err = geocode(name, area, fname)
            
            if lat is not None:
                data[cat][i]['lat'] = lat
                data[cat][i]['lng'] = lng
                modified = True
                count += 1
                if count % 20 == 0:
                    print(f'  [{fname}] {count} done - {name[:30]} -> {lat:.4f}, {lng:.4f}')
            else:
                fail += 1
                if err == 'OVER_QUERY_LIMIT':
                    print(f'  OVER_QUERY_LIMIT! Sleep 60s...')
                    time.sleep(60)
                    lat, lng, err2 = geocode(name, area, fname)
                    if lat is not None:
                        data[cat][i]['lat'] = lat
                        data[cat][i]['lng'] = lng
                        modified = True
                        count += 1
                        print(f'  retry OK: {name[:30]}')
                    else:
                        print(f'  retry FAIL: {name[:30]} -> {err2}')
            
            time.sleep(RATE)
    
    if modified:
        tmp = fp + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, fp)
        print(f'  -> {fname} saved ({count} geocoded, {fail} failed)')
    else:
        print(f'  -> {fname} no changes needed')
    
    return count, fail

def main():
    files = sorted([f for f in os.listdir(DATA_DIR) 
                    if f.endswith('.json') 
                    and f not in ['meta.json', 'cities.json', 'search_results_temp.json']])
    
    total_done = 0
    total_fail = 0
    
    for fname in files:
        print(f'Processing {fname}...')
        try:
            c, f = process_file(fname)
            total_done += c
            total_fail += f
            print(f'  Cumulative: {total_done} done, {total_fail} failed')
        except Exception as e:
            print(f'  ERROR: {e}')
    
    print(f'\n=== Done ===')
    print(f'Total geocoded: {total_done}')
    print(f'Total failed: {total_fail}')

if __name__ == '__main__':
    main()
