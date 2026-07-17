#!/usr/bin/env python3
"""
台灣旅遊網站 — 縣市分類自動稽核腳本
用座標(lat/lng)判斷每家店是否放在正確的城市 JSON。

邏輯：
1. 定義每個城市的座標邊界框（bounding box）
2. 掃描所有 data/*.json 的 food/spots/souvenirs
3. 如果 item 有 lat/lng，檢查座標是否落在所屬城市的邊界框內
4. 如果不在，找出座標實際落在哪個城市
5. 輸出報告：需要搬移的 item 清單

注意：
- 邊界城鎮（美濃、瑞芳、清境等）可能座標靠近其他城市，但行政區歸屬是正確的
- 所以用 area 行政區名稱做二次確認：如果 area 是該城市的行政區，就算座標偏了也不搬
- 只搬移「座標 + area 都不屬於該城市」的 item

Usage:
  python city_audit.py              # 只報告，不修改
  python city_audit.py --fix        # 報告 + 自動搬移
"""

import json
import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# ============================================================
# 城市邊界框 (lat_min, lat_max, lng_min, lng_max)
# 參考實際行政區範圍，留一些 margin
# ============================================================
CITY_BBOX = {
    'taipei.json':     (24.95, 25.20, 121.43, 121.70),  # 含北投/士林/關渡
    'newtaipei.json':  (24.70, 25.30, 121.28, 122.10),  # 含瑞芳/貢寮/雙溪/三芝
    'taoyuan.json':    (24.75, 25.05, 121.05, 121.35),
    'hsinchu.json':    (24.50, 24.90, 120.85, 121.20),  # 含尖石/關西
    'miaoli.json':     (24.30, 24.70, 120.70, 121.20),
    'taichung.json':   (24.00, 24.30, 120.50, 121.10),
    'changhua.json':   (23.85, 24.15, 120.30, 120.70),
    'nantou.json':     (23.50, 24.20, 120.60, 121.30),  # 含清境/仁愛鄉
    'yunlin.json':     (23.50, 23.80, 120.10, 120.65),
    'chiayi.json':     (23.30, 23.60, 120.20, 120.85),  # 嘉義縣市
    'tainan.json':     (22.85, 23.45, 120.05, 120.60),
    'kaohsiung.json':  (22.55, 23.35, 120.20, 121.15),  # 含美濃/六龜/甲仙/桃源/茂林/那瑪夏
    'pingtung.json':   (21.90, 22.85, 120.25, 120.95),  # 含小琉球
    'keelung.json':    (25.08, 25.20, 121.70, 121.85),
    'yilan.json':      (24.40, 24.95, 121.50, 121.95),
    'hualien.json':    (23.10, 24.50, 121.20, 121.80),
    'taitung.json':    (21.90, 23.50, 120.85, 121.80),  # 含蘭嶼/綠島
    'penghu.json':     (23.40, 23.75, 119.40, 119.70),
}

# 城市行政區關鍵字（用來做 area 二次確認）
# 如果 area 包含這些關鍵字，就算座標偏了也不搬
CITY_AREAS = {
    'taipei.json': ['北投','士林','內湖','松山','信義','大安','中正','大同','萬華','文山','南港','中山','台北'],
    'newtaipei.json': ['板橋','三重','中和','永和','新莊','新店','土城','蘆洲','樹林','汐止','鶯歌','三峽','淡水','金山','萬里','八里','林口','泰山','五股','瑞芳','深坑','石碇','坪林','烏來','雙溪','貢寮','平溪','新北'],
    'taoyuan.json': ['桃園','中壢','平鎮','八德','楊梅','蘆竹','大溪','龜山','龍潭','大園','觀音','新屋','復興'],
    'hsinchu.json': ['新竹','新埔','竹北','竹東','湖口','新豐','峨眉','寶山','北埔','芎林','橫山','關西','尖石','五峰'],
    'miaoli.json': ['苗栗','竹南','頭份','後龍','通霄','苑裡','銅鑼','三義','西湖','公館','獅潭','三灣','南庄','卓蘭','大湖','泰安','造橋','頭屋'],
    'taichung.json': ['台中','豐原','大里','太平','東勢','沙鹿','梧棲','清水','大甲','霧峰','烏日','后里','石岡','外埔','大安','龍井','神岡','潭子','大雅','新社','和平','大肚','烏日'],
    'changhua.json': ['彰化','員林','鹿港','和美','北斗','田中','二林','溪湖','埔心','埔鹽','永靖','社頭','田尾','埤頭','芳苑','大城','竹塘','溪州','芬園','花壇','線西','伸港','二水'],
    'nantou.json': ['南投','埔里','草屯','竹山','集集','名間','鹿谷','水里','魚池','國姓','水里','信義','仁愛','中寮','鹿谷','太魯閣'],
    'yunlin.json': ['斗六','斗南','虎尾','西螺','土庫','北港','古坑','大埤','莿桐','林內','二崙','崙背','麥寮','東勢','褒忠','台西','元長','四湖','口湖','水林'],
    'chiayi.json': ['嘉義','朴子','布袋','大林','民雄','水上','梅山','竹崎','中埔','番路','大埔','新港','六腳','東石','鹿草','太保','溪口','義竹','阿里山'],
    'tainan.json': ['台南','永康','新化','善化','佳里','麻豆','新營','白河','鹽水','柳營','後壁','東山','仁德','歸仁','關廟','安定','安平','安南','北門','將軍','七股','學甲','西港','下營','楠西','南化','左鎮','玉井','山上','大內','六甲','官田','善化','新市','新化','安定'],
    'kaohsiung.json': ['高雄','鳳山','岡山','旗山','美濃','林園','大寮','大樹','大社','仁武','鳥松','橋頭','燕巢','阿蓮','路竹','湖內','茄萣','永安','彌陀','梓官','楠梓','左營','鼓山','三民','鹽埕','前金','新興','苓雅','前鎮','旗津','小港','桃源','那瑪夏','茂林','六龜','甲仙','杉林','內門','田寮','美麗島','草衙道','紅毛港'],
    'pingtung.json': ['屏東','潮州','內埔','萬丹','麟洛','竹田','長治','新園','崁頂','南州','新埤','來義','萬巒','竹田','恆春','車城','滿州','枋山','枋寮','春日','獅子','牡丹','琉球','東港','林邊','佳冬','枋寮','高樹','里港','鹽埔','九如','三地門','霧台','瑪家','泰武','來義'],
    'keelung.json': ['基隆','仁愛','信義','中正','安樂','暖暖','七堵'],
    'yilan.json': ['宜蘭','羅東','蘇澳','頭城','礁溪','壯圍','員山','冬山','五結','三星','大同','南澳'],
    'hualien.json': ['花蓮','吉安','新城','壽豐','鳳林','光復','豐濱','瑞穗','玉里','富里','秀林','萬榮','卓溪'],
    'taitung.json': ['台東','卑南','延平','鹿野','關山','海端','池上','東河','成功','長濱','太麻里','金峰','大武','達仁','綠島','蘭嶼'],
    'penghu.json': ['澎湖','馬公','湖西','白沙','西嶼','望安','七美'],
}


def point_in_bbox(lat, lng, bbox):
    """檢查座標是否在邊界框內"""
    lat_min, lat_max, lng_min, lng_max = bbox
    return lat_min <= lat <= lat_max and lng_min <= lng <= lng_max


def find_city_by_point(lat, lng):
    """根據座標找出最近的城市"""
    for city, bbox in CITY_BBOX.items():
        if point_in_bbox(lat, lng, bbox):
            return city
    # 不在任何邊界框內，找最近的
    best = None
    best_dist = 999
    for city, bbox in CITY_BBOX.items():
        clat = (bbox[0] + bbox[1]) / 2
        clng = (bbox[2] + bbox[3]) / 2
        d = ((lat - clat) ** 2 + (lng - clng) ** 2) ** 0.5
        if d < best_dist:
            best_dist = d
            best = city
    return best


def area_belongs_to_city(area, city_file):
    """檢查 area 行政區名稱是否屬於該城市"""
    if not area:
        return False
    areas = CITY_AREAS.get(city_file, [])
    for a in areas:
        if a in area or area in a:
            return True
    return False


def audit():
    """主稽核函數"""
    misplaced = []

    for fname in sorted(os.listdir(DATA_DIR)):
        if not fname.endswith('.json') or fname in ['meta.json', 'cities.json', 'search_results_temp.json']:
            continue
        if fname not in CITY_BBOX:
            continue

        filepath = os.path.join(DATA_DIR, fname)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for cat in ['food', 'spots', 'souvenirs']:
            if cat not in data or not isinstance(data[cat], list):
                continue
            for idx, item in enumerate(data[cat]):
                if not isinstance(item, dict):
                    continue
                lat = item.get('lat')
                lng = item.get('lng')
                if lat is None or lng is None:
                    continue

                # 檢查座標是否在該城市邊界框內
                bbox = CITY_BBOX[fname]
                if point_in_bbox(lat, lng, bbox):
                    continue  # 座標在正確城市，OK

                # 座標不在該城市，用 area 二次確認
                area = item.get('area', '')
                if area_belongs_to_city(area, fname):
                    continue  # area 確認是該城市的行政區，OK（邊界城鎮）

                # 座標和 area 都不屬於該城市 → 真正的錯誤
                correct_city = find_city_by_point(lat, lng)
                if correct_city and correct_city != fname:
                    misplaced.append({
                        'from_file': fname,
                        'to_file': correct_city,
                        'category': cat,
                        'index': idx,
                        'name': item.get('name', '')[:40],
                        'area': area,
                        'lat': lat,
                        'lng': lng,
                    })

    return misplaced


def fix(misplaced):
    """自動搬移錯誤的 item"""
    # 按 from_file 分組
    moves = {}  # {(from_file, to_file, cat): [indices]}
    for m in misplaced:
        key = (m['from_file'], m['to_file'], m['category'])
        if key not in moves:
            moves[key] = []
        moves[key].append(m)

    # 收集所有要搬的 item
    to_move = {}  # {from_file: {cat: {index: to_file}}}
    for m in misplaced:
        from_f = m['from_file']
        cat = m['category']
        idx = m['index']
        to_f = m['to_file']
        if from_f not in to_move:
            to_move[from_f] = {}
        if cat not in to_move[from_f]:
            to_move[from_f][cat] = {}
        to_move[from_f][cat][idx] = to_f

    # 從 from_file 移除，加到 to_file
    moved = 0
    for from_file, cats in to_move.items():
        from_path = os.path.join(DATA_DIR, from_file)
        with open(from_path, 'r', encoding='utf-8') as f:
            from_data = json.load(f)

        # 要搬出的 items（按 index 降序排，方便 pop）
        items_by_dest = {}  # {to_file: [items]}
        for cat, indices in cats.items():
            for idx in sorted(indices.keys(), reverse=True):
                to_file = indices[idx]
                item = from_data[cat].pop(idx)
                if to_file not in items_by_dest:
                    items_by_dest[to_file] = {}
                if cat not in items_by_dest[to_file]:
                    items_by_dest[to_file][cat] = []
                items_by_dest[to_file][cat].append(item)
                moved += 1

        # 寫回 from_file
        tmp = from_path + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(from_data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, from_path)

        # 加到 to_file
        for to_file, cats_to_add in items_by_dest.items():
            to_path = os.path.join(DATA_DIR, to_file)
            with open(to_path, 'r', encoding='utf-8') as f:
                to_data = json.load(f)
            for cat, items in cats_to_add.items():
                if cat not in to_data:
                    to_data[cat] = []
                to_data[cat].extend(items)
            tmp = to_path + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(to_data, f, ensure_ascii=False, indent=2)
            os.replace(tmp, to_path)

    return moved


def main():
    do_fix = '--fix' in sys.argv

    print("=" * 70)
    print("台灣旅遊網站 — 縣市分類稽核")
    print("=" * 70)

    # 先統計各城市數量
    print("\n📊 各城市 item 數量（稽核前）：")
    total = 0
    for fname in sorted(CITY_BBOX.keys()):
        fp = os.path.join(DATA_DIR, fname)
        if not os.path.exists(fp):
            continue
        with open(fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
        count = 0
        for cat in ['food', 'spots', 'souvenirs']:
            if cat in data and isinstance(data[cat], list):
                count += len(data[cat])
        total += count
        print(f"  {fname:25s} {count:5d}")
    print(f"  {'TOTAL':25s} {total:5d}")

    # 稽核
    print("\n🔍 開始稽核...")
    # 先刪除國外座標的 item（lat 不在 21-26 範圍內）
    foreign_deleted = 0
    for fname in sorted(os.listdir(DATA_DIR)):
        if not fname.endswith('.json') or fname in ['meta.json', 'cities.json', 'search_results_temp.json']:
            continue
        if fname not in CITY_BBOX:
            continue
        fp = os.path.join(DATA_DIR, fname)
        with open(fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
        changed = False
        for cat in ['food', 'spots', 'souvenirs']:
            if cat not in data or not isinstance(data[cat], list):
                continue
            new_list = []
            for item in data[cat]:
                if not isinstance(item, dict):
                    new_list.append(item)
                    continue
                lat = item.get('lat', 0)
                lng = item.get('lng', 0)
                if lat and lng and not (21.0 <= lat <= 26.5 and 119.0 <= lng <= 122.5):
                    nm = item.get('name', '')[:30]
                    print(f'  [FOREIGN] {fname} [{cat}] {nm} lat={lat},lng={lng} -> DELETE')
                    foreign_deleted += 1
                    changed = True
                else:
                    new_list.append(item)
            data[cat] = new_list
        if changed:
            tmp = fp + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(tmp, fp)
    if foreign_deleted:
        print(f'  刪除 {foreign_deleted} 筆國外座標 item')

    misplaced = audit()

    if not misplaced:
        print("\n✅ 沒有發現分類錯誤！所有 item 都在正確的城市。")
        return

    # 報告
    print(f"\n⚠️  發現 {len(misplaced)} 筆分類錯誤：\n")

    # 按 from_file 分組顯示
    by_from = {}
    for m in misplaced:
        key = m['from_file']
        if key not in by_from:
            by_from[key] = []
        by_from[key].append(m)

    for from_file, items in sorted(by_from.items()):
        # 按 to_file 統計
        by_to = {}
        for m in items:
            to = m['to_file']
            if to not in by_to:
                by_to[to] = []
            by_to[to].append(m)

        print(f"  {from_file}:")
        for to_file, sub_items in sorted(by_to.items()):
            print(f"    → {to_file}: {len(sub_items)} 筆")
            for m in sub_items[:5]:  # 每組最多顯示 5 筆
                print(f"       [{m['category']}] {m['name']} | area={m['area']} | lat={m['lat']:.4f},lng={m['lng']:.4f}")
            if len(sub_items) > 5:
                print(f"       ... 還有 {len(sub_items) - 5} 筆")
        print()

    if do_fix:
        print("🔧 開始自動搬移...")
        moved = fix(misplaced)
        print(f"✅ 搬移完成！共搬移 {moved} 筆。")

        # 統計搬移後數量
        print("\n📊 各城市 item 數量（稽核後）：")
        total = 0
        for fname in sorted(CITY_BBOX.keys()):
            fp = os.path.join(DATA_DIR, fname)
            if not os.path.exists(fp):
                continue
            with open(fp, 'r', encoding='utf-8') as f:
                data = json.load(f)
            count = 0
            for cat in ['food', 'spots', 'souvenirs']:
                if cat in data and isinstance(data[cat], list):
                    count += len(data[cat])
            total += count
            print(f"  {fname:25s} {count:5d}")
        print(f"  {'TOTAL':25s} {total:5d}")
    else:
        print(f"\n💡 加 --fix 參數可自動搬移：python city_audit.py --fix")


if __name__ == '__main__':
    main()