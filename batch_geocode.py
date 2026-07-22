#!/usr/bin/env python3
"""
?寞活??Google Geocoding API ?亥岷???撱??舫???蝺臬漲摨扳???v2: 摰撖怠 ?????????瘥?撣?獢摰?撖思?甈～??舀?琿?蝥??"""
import json, os, sys, time, urllib.request, urllib.parse

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
API_KEY = 'REDACTED'
PROGRESS_FILE = os.path.join(os.path.dirname(__file__), 'geocode_progress.json')
RATE_LIMIT = 0.15  # 150ms between calls (~6.6 QPS, safe under 10 QPS)
SAVE_EVERY_CITY = True

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        prog = json.load(open(PROGRESS_FILE, 'r', encoding='utf-8'))
        return prog
    return {'done_files': [], 'total_done': 0, 'failed': [], 'errors': 0}

def save_progress(prog):
    tmp = PROGRESS_FILE + '.tmp'
    json.dump(prog, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    os.replace(tmp, PROGRESS_FILE)

def geocode(name, area, city_file):
    city_name = city_file.replace('.json', '')
    parts = [name, area, city_name, '?啁']
    addr = ' '.join(p for p in parts if p)
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={urllib.parse.quote(addr)}&key={API_KEY}&language=zh-TW'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Nova-BatchGeocoder/2.0'})
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read())
        if data['status'] == 'OK' and data['results']:
            loc = data['results'][0]['geometry']['location']
            return loc['lat'], loc['lng'], None
        else:
            return None, None, data['status']
    except Exception as e:
        return None, None, str(e)

def process_city(fname, prog):
    fp = os.path.join(DATA_DIR, fname)
    data = json.load(open(fp, 'r', encoding='utf-8'))
    if not isinstance(data, dict):
        return 0
    
    city_count = 0
    city_failed = []
    file_modified = False
    
    for cat in data:
        if not isinstance(data[cat], list):
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
                file_modified = True
                city_count += 1
                prog['total_done'] += 1
                
                if city_count % 20 == 0:
                    print(f'  [{fname}] {city_count} done - {name[:20]} -> {lat:.4f}, {lng:.4f}')
            else:
                city_failed.append({'cat': cat, 'idx': i, 'name': name, 'error': err})
                prog['errors'] += 1
                if err == 'OVER_QUERY_LIMIT':
                    print(f'  OVER_QUERY_LIMIT! Sleeping 60s...')
                    time.sleep(60)
                    # retry
                    lat, lng, err2 = geocode(name, area, fname)
                    if lat is not None:
                        data[cat][i]['lat'] = lat
                        data[cat][i]['lng'] = lng
                        file_modified = True
                        city_count += 1
                        prog['total_done'] += 1
                        prog['errors'] -= 1
                        print(f'  retry OK: {name} -> {lat}, {lng}')
                    else:
                        print(f'  retry FAIL: {name} -> {err2}')
            
            time.sleep(RATE_LIMIT)
    
    # Write file once after processing entire city
    if file_modified:
        tmp = fp + '.tmp'
        json.dump(data, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        os.replace(tmp, fp)
        print(f'  -> {fname} saved ({city_count} geocoded)')
    
    prog['failed'].extend(city_failed)
    prog['done_files'].append(fname)
    save_progress(prog)
    return city_count

def main():
    prog = load_progress()
    done_files = set(prog['done_files'])
    
    # List all city files
    city_files = sorted([f for f in os.listdir(DATA_DIR) 
                         if f.endswith('.json') 
                         and f not in ['meta.json', 'cities.json', 'search_results_temp.json']])
    
    pending = [f for f in city_files if f not in done_files]
    print(f'??瑼?: {len(city_files)} ??)
    print(f'撌脣??? {len(done_files)} ??)
    print(f'敺??? {len(pending)} ??)
    print(f'撌脫摨扳?: {prog["total_done"]} 蝑?)
    print(f'憭望?: {prog["errors"]} 蝑?)
    print()
    
    if not pending:
        print('?券摰?嚗?)
        return
    
    grand_total = 0
    for idx, fname in enumerate(pending):
        print(f'[{idx+1}/{len(pending)}] ?? {fname}...')
        count = process_city(fname, prog)
        grand_total += count
        print(f'  蝝航?: {grand_total} 蝑?(蝮賡脣漲: {prog["total_done"]})')
        print()
    
    print(f'\n=== ?券摰? ===')
    print(f'?祆活?亙?: {grand_total}')
    print(f'蝮質??亙?: {prog["total_done"]}')
    print(f'憭望?: {prog["errors"]}')

if __name__ == '__main__':
    main()
