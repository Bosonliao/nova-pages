import json, time, urllib.request, urllib.parse

data = json.load(open('nightmarkets.json','r',encoding='utf-8'))
print(f"總共 {len(data)} 家夜市")

done = 0
for d in data:
    if d.get('lat') is not None:
        done += 1
        continue
    name = d.get('name','')
    city = d.get('city','')
    district = d.get('district','')
    
    # 嘗試用夜市名+城市查
    queries = [
        f"{name} {city}",
        f"{name} {district}",
        f"{name}",
    ]
    
    found = False
    for q in queries:
        encoded = urllib.parse.quote(q)
        url = f"https://nominatim.openstreetmap.org/search?q={encoded}&format=json&limit=1&countrycodes=tw"
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"nova-pages/1.0"})
            resp = urllib.request.urlopen(req, timeout=10)
            results = json.loads(resp.read())
            if results:
                lat = float(results[0]['lat'])
                lng = float(results[0]['lon'])
                # 確認在台灣範圍內
                if 21.5 <= lat <= 26.5 and 118 <= lng <= 123:
                    d['lat'] = lat
                    d['lng'] = lng
                    found = True
                    break
        except:
            pass
        time.sleep(1.5)
    
    if not found:
        d['lat'] = None
        d['lng'] = None
    
    done += 1
    if done % 10 == 0:
        print(f"進度: {done}/{len(data)}", flush=True)
        json.dump(data, open('nightmarkets.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

json.dump(data, open('nightmarkets.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
has = sum(1 for d in data if d.get('lat') is not None)
print(f"完成！有座標: {has}/{len(data)}")