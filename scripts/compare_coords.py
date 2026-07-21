import json, sys, io, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Johnny's precise coords
johnny = {
    "花火禾茶": (24.91032, 121.15786),
    "金茶伍": (24.91316, 121.17387),
    "茗茗究市": (24.91386, 121.14583),
    "吾奶王": (24.91892, 121.18231),
    "功夫茶": (24.91523, 121.18042),
    "自然湉": (24.91187, 121.14385),
    "50嵐 楊梅大成店": (24.91225, 121.14418),
}

# Playwright coords (from the gmaps_coords.py run)
playwright = {
    "花火禾茶": (24.91170, 121.15661),
    "金茶伍": (24.91004, 121.18243),
    "茗茗究市": (24.90847, 121.14541),
    "吾奶王": (24.90886, 121.17570),
    "功夫茶": (24.91347, 121.18076),
    "自然湉": (24.91307, 121.14576),
    "50嵐 楊梅大成店": (24.91734, 121.18503),  # original data
}

def haversine(lat1,lng1,lat2,lng2):
    R=6371
    dLat=math.radians(lat2-lat1)
    dLng=math.radians(lng2-lng1)
    a=math.sin(dLat/2)**2+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dLng/2)**2
    return R*2*math.asin(math.sqrt(a))

print('=== Playwright vs Johnny 精確座標比較 ===')
print(f'{"店名":20s} | {"Playwright":20s} | {"Johnny":20s} | {"誤差":>8s}')
print('-' * 80)
for name in johnny:
    p_lat, p_lng = playwright[name]
    j_lat, j_lng = johnny[name]
    d = haversine(p_lat, p_lng, j_lat, j_lng)
    print(f'{name:20s} | ({p_lat:.5f}, {p_lng:.5f}) | ({j_lat:.5f}, {j_lng:.5f}) | {d:.0f}m')
