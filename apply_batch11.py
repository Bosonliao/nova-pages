# -*- coding: utf-8 -*-
import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Batch 11 - more updates for all 5 cities
updates = [
    # 台東
    {"city":"台東","index":454,"dishes":[
        {"name":"炸香豆腐","desc":"池上排隊銅板美食，外酥內嫩只有40~50元","price":"40"},
        {"name":"豆花","desc":"手工豆花搭配豆漿，池上必吃甜點"},
        {"name":"豆漿","desc":"濃郁純手工豆漿，配炸豆腐超對味"}
    ]},
    {"city":"台東","index":476,"dishes":[
        {"name":"西班牙料理","desc":"道地西班牙料理，無敵蔚藍海景配美食"},
        {"name":"海景咖啡","desc":"180度環海美景，露天游泳池美拍"}
    ]},
    {"city":"台東","index":0,"dishes":[
        {"name":"剉冰","desc":"古早味阿桑剉冰，台東消暑聖品"}
    ]},
    {"city":"台東","index":27,"dishes":[
        {"name":"地瓜酥","desc":"台東連城記地瓜酥，正氣門市必買伴手禮"}
    ]},
    {"city":"台東","index":79,"dishes":[
        {"name":"麻糬","desc":"陳家麻糬商行，台東伴手禮必買"}
    ]},
    {"city":"台東","index":187,"dishes":[
        {"name":"海鮮料理","desc":"葉氏海鮮Yeh's Fish，成功漁港新鮮海鮮"}
    ]},
    {"city":"台東","index":222,"dishes":[
        {"name":"玩冰箱","desc":"我在玩玩冰箱，台東特色冰箱博物館美食"
        }
    ]},
    {"city":"台東","index":308,"dishes":[
        {"name":"米苔目","desc":"阿咪米苔目，台東人氣米苔目小吃"}
    ]},
    {"city":"台東","index":410,"dishes":[
        {"name":"池上便當","desc":"池上大坡池周邊小吃，池上米食必吃"}
    ]},
    {"city":"台東","index":443,"dishes":[
        {"name":"豆皮","desc":"大池豆皮店，池上手工豆皮必吃"}
    ]},
    {"city":"台東","index":484,"dishes":[
        {"name":"客家菜","desc":"老地方客家菜大溪超人氣美食，道地老店"}
    ]},
    {"city":"台東","index":516,"dishes":[
        {"name":"脫線雞","desc":"台東脫線牧場，台東知本放山雞必吃"}
    ]},
    # 雲林
    {"city":"雲林","index":390,"dishes":[
        {"name":"豬腳飯","desc":"阿賜豬腳飯，梅干豬腳飯幾乎每桌必點，食尚玩家推薦"}
    ]},
    {"city":"雲林","index":416,"dishes":[
        {"name":"豬腳飯","desc":"阿賜豬腳，斗六老店梅干豬腳飯必吃"}
    ]},
    {"city":"雲林","index":543,"dishes":[
        {"name":"油飯麵線糊","desc":"老等油飯麵線糊，北港傳統油飯必吃"}
    ]},
    {"city":"雲林","index":488,"dishes":[
        {"name":"魷魚嘴羹","desc":"魷魚興魷魚嘴羮，雲林特色小吃必吃"}
    ]},
    {"city":"雲林","index":490,"dishes":[
        {"name":"圓仔冰","desc":"長興圓仔冰，雲林北港必吃古早味冰品"}
    ]},
    {"city":"雲林","index":731,"dishes":[
        {"name":"炊仔飯","desc":"正斗六炊仔飯，雲林斗六必吃特色米食"}
    ]},
    {"city":"雲林","index":732,"dishes":[
        {"name":"肉圓","desc":"鄧肉圓斗六總店，雲林斗六人氣肉圓"}
    ]},
    {"city":"雲林","index":639,"dishes":[
        {"name":"土魠魚羹","desc":"一郎土魠魚羹，招牌青蛙湯豬腳飯必點"}
    ]},
    {"city":"雲林","index":79,"dishes":[
        {"name":"婆婆麵","desc":"虎科婆婆麵店，虎尾科大人氣麵店"}
    ]},
    {"city":"雲林","index":113,"dishes":[
        {"name":"婆婆的店","desc":"虎尾婆婆的店，虎尾人氣家常麵食"}
    ]},
    {"city":"雲林","index":143,"dishes":[
        {"name":"肉圓","desc":"斗南徐記肉圓，雲林斗南必吃肉圓"}
    ]},
    {"city":"雲林","index":222,"dishes":[
        {"name":"牛肉麵","desc":"張家牛肉麵，雲林斗六人氣牛肉麵"}
    ]},
    {"city":"雲林","index":301,"dishes":[
        {"name":"肉圓","desc":"吳記肉圓，雲林北港必吃肉圓"}
    ]},
    {"city":"雲林","index":398,"dishes":[
        {"name":"米糕","desc":"斗南米糕甲，雲林斗南必吃米糕"}
    ]},
    {"city":"雲林","index":478,"dishes":[
        {"name":"當歸鴨","desc":"土庫老店當歸鴨肉麵線，雲林土庫必吃"}
    ]},
    {"city":"雲林","index":587,"dishes":[
        {"name":"羊肉爐","desc":"東市羊肉，雲林人氣羊肉料理"}
    ]},
    # 澎湖
    {"city":"澎湖","index":245,"dishes":[
        {"name":"花菜干","desc":"炒花菜干招牌菜，澎湖傳統特色料理必點"},
        {"name":"鮖鮔滷肉","desc":"鮖鮔滷肉無敵下飯，食尚玩家推薦"},
        {"name":"酸瓜炒肉","desc":"酸瓜炒肉經典澎湖特色菜，古早味"}
    ]},
    {"city":"澎湖","index":0,"dishes":[
        {"name":"仙人掌冰","desc":"江巷仔內仙人掌冰，澎湖必吃仙人掌冰"}
    ]},
    {"city":"澎湖","index":96,"dishes":[
        {"name":"鮮魚粥","desc":"海城上湯鮮魚粥，澎湖馬公必吃鮮魚粥"}
    ]},
    {"city":"澎湖","index":155,"dishes":[
        {"name":"小管麵線","desc":"吹蚵仔海鮮小管麵線，澎湖必吃海鮮麵線"}
    ]},
    {"city":"澎湖","index":160,"dishes":[
        {"name":"海鮮合菜","desc":"臨海樓海鮮料理，澎湖馬公海鮮餐廳必吃"}
    ]},
    {"city":"澎湖","index":191,"dishes":[
        {"name":"牛肉麵","desc":"美東芳牛肉麵，澎湖馬公必吃牛肉麵"}
    ]},
    {"city":"澎湖","index":248,"dishes":[
        {"name":"海鮮料理","desc":"來福海鮮餐廳，澎湖馬公活海鮮必吃"}
    ]},
    {"city":"澎湖","index":189,"dishes":[
        {"name":"牛肉麵","desc":"老蔡牛肉麵，澎湖馬公老牌牛肉麵"}
    ]},
    {"city":"澎湖","index":112,"dishes":[
        {"name":"杏仁茶","desc":"二崁杏仁茶，澎湖西嶼二崁村必喝古早味"}
    ]},
    # 金馬
    {"city":"金馬","index":44,"dishes":[
        {"name":"老酒豬肉披薩","desc":"招牌老酒豬肉蛋口味披薩，芹壁海景第一排必吃"},
        {"name":"歐式麵包","desc":"手工歐式麵包，馬祖北竿芹壁必買"},
        {"name":"海景咖啡","desc":"180度環海美景，一邊喝咖啡一邊聽海聲"}
    ]},
    {"city":"金馬","index":47,"dishes":[
        {"name":"閩式燒餅","desc":"閩式燒餅專賣店，金門必吃特色燒餅"}
    ]},
    {"city":"金馬","index":49,"dishes":[
        {"name":"廣東粥","desc":"米香屋廣東粥，金門人氣廣東粥"}
    ]},
    {"city":"金馬","index":57,"dishes":[
        {"name":"閩式料理","desc":"依嬤的店，金門閩式料理必吃"}
    ]},
    {"city":"金馬","index":60,"dishes":[
        {"name":"海鮮料理","desc":"記德海鮮餐廳，金門海鮮餐廳必吃"}
    ]},
    {"city":"金馬","index":32,"dishes":[
        {"name":"牛肉麵","desc":"良金牧場工廠總店，金門酒糟牛肉麵必吃"}
    ]},
    {"city":"金馬","index":22,"dishes":[
        {"name":"牛肉麵","desc":"良金牧場貞節牌坊店，金門酒糟牛肉麵"}
    ]},
    {"city":"金馬","index":62,"dishes":[
        {"name":"牛肉料理","desc":"喬安牧場伯玉旗艦店，金門牛肉料理必吃"}
    ]},
    {"city":"金馬","index":11,"dishes":[
        {"name":"牛排","desc":"19house炙燒牛排金門店，金門人氣牛排館"}
    ]},
    {"city":"金馬","index":50,"dishes":[
        {"name":"伴手禮","desc":"合泉購物中心，金門伴手禮必買"}
    ]},
    {"city":"金馬","index":70,"dishes":[
        {"name":"海鮮","desc":"信源海產店湖下店，金門海產餐廳必吃"}
    ]},
    {"city":"金馬","index":71,"dishes":[
        {"name":"小吃","desc":"標記小吃店，金門在地人氣小吃"}
    ]}
]

count = 0
for u in updates:
    city = u['city']
    idx = u['index']
    dishes = u['dishes']
    if city in data and idx < len(data[city]['food']):
        data[city]['food'][idx]['dishes'] = dishes
        count += 1
        print(f"Updated {city}[{idx}]")

with open('data-zh.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nTotal updated: {count}")
print("Saved data-zh.json")