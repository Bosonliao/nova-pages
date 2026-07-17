#!/usr/bin/env python3
"""
台灣旅遊網站 - 縣市分類錯誤自動檢查
用法: python check_city_classification.py
輸出: 所有可疑的分類錯誤，依嚴重程度排序
"""
import json, sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# 城市中心座標和合理 lat/lng 範圍
# 範圍設得寬鬆，避免邊界城鎮誤判
CITY_BOUNDS = {
    'taipei.json':     {'lat_min': 24.95, 'lat_max': 25.20, 'lng_min': 121.35, 'lng_max': 121.70},
    'newtaipei.json':  {'lat_min': 24.70, 'lat_max': 25.30, 'lng_min': 121.20, 'lng_max': 122.10},
    'taoyuan.json':    {'lat_min': 24.75, 'lat_max': 25.15, 'lng_min': 121.05, 'lng_max': 121.50},
    'hsinchu.json':    {'lat_min': 24.55, 'lat_max': 24.95, 'lng_min': 120.75, 'lng_max': 121.20},
    'taichung.json':   {'lat_min': 23.90, 'lat_max': 24.40, 'lng_min': 120.40, 'lng_max': 120.90},
    'chiayi.json':     {'lat_min': 23.25, 'lat_max': 23.70, 'lng_min': 120.15, 'lng_max': 120.85},
    'tainan.json':     {'lat_min': 22.80, 'lat_max': 23.40, 'lng_min': 119.90, 'lng_max': 120.70},
    'kaohsiung.json':  {'lat_min': 22.40, 'lat_max': 23.40, 'lng_min': 120.10, 'lng_max': 121.10},
    'keelung.json':    {'lat_min': 25.05, 'lat_max': 25.20, 'lng_min': 121.60, 'lng_max': 121.85},
    'yilan.json':      {'lat_min': 24.40, 'lat_max': 25.05, 'lng_min': 121.40, 'lng_max': 122.20},
    'hualien.json':    {'lat_min': 23.40, 'lat_max': 24.40, 'lng_min': 121.20, 'lng_max': 121.90},
    'taitung.json':    {'lat_min': 22.20, 'lat_max': 23.60, 'lng_min': 120.80, 'lng_max': 121.60},
    'pingtung.json':   {'lat_min': 21.80, 'lat_max': 22.80, 'lng_min': 120.10, 'lng_max': 120.95},
    'changhua.json':   {'lat_min': 23.70, 'lat_max': 24.20, 'lng_min': 120.20, 'lng_max': 120.70},
    'nantou.json':     {'lat_min': 23.40, 'lat_max': 24.30, 'lng_min': 120.50, 'lng_max': 121.40},
    'yunlin.json':     {'lat_min': 23.50, 'lat_max': 24.00, 'lng_min': 120.10, 'lng_max': 120.70},
    'miaoli.json':     {'lat_min': 24.30, 'lat_max': 24.70, 'lng_min': 120.60, 'lng_max': 121.20},
    'penghu.json':     {'lat_min': 23.40, 'lat_max': 23.75, 'lng_min': 119.30, 'lng_max': 119.80},
}

# 行政區跨縣市同名提醒（這些 area 名稱在多個縣市都有，需要用座標判斷）
AMBIGUOUS_AREAS = ['中山', '西區', '東區', '北區', '南區', '中區', '中西區', '大安', '信義', '仁愛', '和平', '公館']

def find_closest_city(lat, lng):
    """找出座標最接近哪個城市"""
    best_city = None
    best_dist = 999
    for cf, bounds in CITY_BOUNDS.items():
        clat = (bounds['lat_min'] + bounds['lat_max']) / 2
        clng = (bounds['lng_min'] + bounds['lng_max']) / 2
        dist = ((lat - clat)**2 + (lng - clng)**2) ** 0.5
        if dist < best_dist:
            best_dist = dist
            best_city = cf
    return best_city, best_dist

def check():
    errors = []
    warnings = []
    
    for fname in sorted(os.listdir(DATA)):
        if not fname.endswith('.json') or fname in ['meta.json', 'cities.json', 'search_results_temp.json']:
            continue
        if fname not in CITY_BOUNDS:
            continue
        
        bounds = CITY_BOUNDS[fname]
        fp = os.path.join(DATA, fname)
        with open(fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for cat in ['food', 'spots', 'souvenirs']:
            if cat not in data or not isinstance(data[cat], list):
                continue
            for i, item in enumerate(data[cat]):
                if not isinstance(item, dict):
                    continue
                lat = item.get('lat')
                lng = item.get('lng')
                if lat is None or lng is None:
                    continue
                
                nm = item.get('name', '')[:35]
                area = item.get('area', '')
                
                # 檢查座標是否在該城市範圍內
                out_of_lat = lat < bounds['lat_min'] or lat > bounds['lat_max']
                out_of_lng = lng < bounds['lng_min'] or lng > bounds['lng_max']
                
                if out_of_lat or out_of_lng:
                    # 找出最接近的城市
                    closest, dist = find_closest_city(lat, lng)
                    if closest != fname:
                        # 判斷嚴重程度
                        lat_diff = abs(lat - (bounds['lat_min'] + bounds['lat_max']) / 2)
                        severity = 'HIGH' if lat_diff > 0.5 else 'MED' if lat_diff > 0.2 else 'LOW'
                        
                        # 同名行政區降級為 warning
                        if area in AMBIGUOUS_AREAS and severity == 'LOW':
                            warnings.append((severity, fname, cat, i, nm, area, lat, lng, closest))
                        else:
                            errors.append((severity, fname, cat, i, nm, area, lat, lng, closest))
    
    # 報告
    if errors:
        print(f'\n=== {len(errors)} ERRORS (需要修正) ===')
        # 按嚴重程度和目標城市排序
        errors.sort(key=lambda x: (x[0] == 'HIGH', x[8], x[0]))
        for e in errors:
            print(f'  [{e[0]}] {e[1]} {e[2]}#{e[3]}: {e[4]} | area={e[5]} lat={e[6]} lng={e[7]} -> {e[8]}')
    
    if warnings:
        print(f'\n=== {len(warnings)} WARNINGS (可能是邊界城鎮) ===')
        for w in warnings[:20]:
            print(f'  [{w[0]}] {w[1]} {w[2]}#{w[3]}: {w[4]} | area={w[5]} lat={w[6]} -> {w[8]}')
        if len(warnings) > 20:
            print(f'  ... and {len(warnings)-20} more warnings')
    
    if not errors and not warnings:
        print('\n✅ All items are within their city bounds!')
    
    return len(errors)

if __name__ == '__main__':
    print('台灣旅遊網站 - 縣市分類錯誤檢查')
    print('=' * 60)
    err_count = check()
    print(f'\n總結: {err_count} 個需要修正的錯誤')