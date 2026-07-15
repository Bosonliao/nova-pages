# -*- coding: utf-8 -*-
import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Batch 10 - 台東 + 雲林 + 澎湖 + 金馬
updates = [
    # 台東
    {"city":"台東","index":18,"dishes":[
        {"name":"鹽味拉麵","desc":"每日熬煮8小時湯頭，濃郁鮮美的招牌鹽味拉麵"},
        {"name":"醬油拉麵","desc":"經典醬油拉麵，開放式廚房可看廚師料理"},
        {"name":"辣味肉醬拉麵","desc":"辣味肉醬拉麵，風味獨特"},
        {"name":"厚切豬排飯","desc":"厚切豬排飯，日式定食人氣選擇"}
    ]},
    {"city":"台東","index":25,"dishes":[
        {"name":"小太陽雞油飯","desc":"超人氣必點，花東晶瑩白米搭配生蛋黃油蔥酥海苔"},
        {"name":"和牛燒肉","desc":"冷藏肉現點現切，和牛選擇多樣"},
        {"name":"霜降牛丼飯","desc":"熱門菜色霜降牛丼飯，晚間最熱門時段"}
    ]},
    {"city":"台東","index":92,"dishes":[
        {"name":"日式定食","desc":"精緻日式定食，開放式廚房新鲜看得見"}
    ]},
    {"city":"台東","index":404,"dishes":[
        {"name":"牛肉麵","desc":"金崙車站旁排隊牛肉麵，超人氣台9線美食"},
        {"name":"酸辣麵","desc":"知本金聯世紀酒店推薦酸辣麵，比牛肉麵還好吃"},
        {"name":"雙醬麵","desc":"雙醬麵好吃，價格實惠份量大"}
    ]},
    {"city":"台東","index":446,"dishes":[
        {"name":"臭豆腐","desc":"酥香卡滋臭豆腐搭香菜蘿蔔絲，美味飄香40多年"}
    ]},
    {"city":"台東","index":454,"dishes":[
        {"name":"福原豆腐","desc":"池上福原豆腐店，台東池上必吃"
        }
    ]},
    {"city":"台東","index":455,"dishes":[
        {"name":"東河包子","desc":"纏記舊街東河包子，台東必吃排隊小吃"}
    ]},
    {"city":"台東","index":337,"dishes":[
        {"name":"牛肉麵","desc":"東鼎牛肉麵館，台東人氣牛肉麵"}
    ]},
    {"city":"台東","index":289,"dishes":[
        {"name":"牛肉麵","desc":"阿牛冠軍牛肉麵，台東冠軍級牛肉麵"}
    ]},
    {"city":"台東","index":173,"dishes":[
        {"name":"鬼頭刀魚乾","desc":"王記鬼頭刀專賣店，成功旗魚料理必吃"}
    ]},
    {"city":"台東","index":221,"dishes":[
        {"name":"鬼頭刀料理","desc":"好漁日鬼頭刀魚主題餐廳，成功漁港新鮮魚料理"}
    ]},
    {"city":"台東","index":500,"dishes":[
        {"name":"黑松羊肉爐","desc":"知本黑松羊肉爐，台東知本必吃暖身美食"}
    ]},
    {"city":"台東","index":504,"dishes":[
        {"name":"黑松羊肉爐","desc":"台東知本老牌羊肉爐，天冷必吃"}
    ]},
    # 雲林
    {"city":"雲林","index":1,"dishes":[
        {"name":"碗粿","desc":"老街碗粿，雲林北港老街必吃碗粿"}
    ]},
    {"city":"雲林","index":28,"dishes":[
        {"name":"石頭火鍋","desc":"金誠石火鍋石頭火鍋韓式燒肉，雲林人氣火鍋"}
    ]},
    {"city":"雲林","index":54,"dishes":[
        {"name":"花枝羹麵","desc":"高稼庄花枝羹麵，雲林北港必吃花枝羹"}
    ]},
    {"city":"雲林","index":37,"dishes":[
        {"name":"嗑肉石鍋","desc":"嗑肉石鍋斗六上海店二代店，人氣石頭火鍋"}
    ]},
    {"city":"雲林","index":52,"dishes":[
        {"name":"牛排套餐","desc":"西堤牛排斗六萬家福店，王品集團平價牛排"}
    ]},
    {"city":"雲林","index":592,"dishes":[
        {"name":"火雞肉飯","desc":"民主火雞肉飯，雲林嘉義-style火雞肉飯必吃"}
    ]},
    {"city":"雲林","index":662,"dishes":[
        {"name":"魷魚羹","desc":"阿國獅魷魚羹，雲林虎尾人氣魷魚羹"}
    ]},
    {"city":"雲林","index":669,"dishes":[
        {"name":"鴨肉飯","desc":"北港福安鴨肉飯，雲林北港必吃鴨肉飯"}
    ]},
    {"city":"雲林","index":675,"dishes":[
        {"name":"鴨肉飯","desc":"福安鴨肉飯，北港老牌鴨肉飯必吃"}
    ]},
    {"city":"雲林","index":712,"dishes":[
        {"name":"紅燒青蛙湯","desc":"北港圓環紅燒青蛙湯，雲林北港特色美食"}
    ]},
    # 澎湖
    {"city":"澎湖","index":5,"dishes":[
        {"name":"冰品","desc":"禾風冰品，澎湖必吃冰品推薦"}
    ]},
    {"city":"澎湖","index":11,"dishes":[
        {"name":"小卷麵線","desc":"吉貝小三的店小卷麵線，澎湖吉貝必吃海鮮麵線"}
    ]},
    {"city":"澎湖","index":29,"dishes":[
        {"name":"仙人掌冰","desc":"自由伯仙人掌冰創始人，澎湖必吃仙人掌冰"}
    ]},
    {"city":"澎湖","index":169,"dishes":[
        {"name":"嫩仙草","desc":"玉冠嫩仙草澎湖總店，澎湖消暑聖品"}
    ]},
    {"city":"澎湖","index":192,"dishes":[
        {"name":"牛雜湯","desc":"北新橋牛雜湯，澎湖馬公必喝暖胃牛雜湯"}
    ]},
    {"city":"澎湖","index":217,"dishes":[
        {"name":"小管麵線","desc":"小萍的店小管麵線，澎湖必吃小管麵線"}
    ]},
    {"city":"澎湖","index":243,"dishes":[
        {"name":"牡蠣料理","desc":"福牡蠣屋，澎湖鮮蚵料理必吃"}
    ]},
    {"city":"澎湖","index":262,"dishes":[
        {"name":"蔥油餅","desc":"郵局口蔥油餅，澎湖馬公排隊蔥油餅"}
    ]},
    # 金馬
    {"city":"金馬","index":3,"dishes":[
        {"name":"拉麵","desc":"初原麵場金門金寧店，金門人氣日式拉麵"}
    ]},
    {"city":"金馬","index":14,"dishes":[
        {"name":"牛肉麵","desc":"圓頭肉乾金城榮泰店，金門牛肉麵牛肉乾必買"}
    ]},
    {"city":"金馬","index":15,"dishes":[
        {"name":"牛肉料理","desc":"高坑牛肉食樂苑餐廳，金門高坑牛肉必吃預約制"}
    ]},
    {"city":"金馬","index":17,"dishes":[
        {"name":"牛肉麵","desc":"良金牧場牛肉麵，金門酒糟牛肉麵必吃"}
    ]},
    {"city":"金馬","index":20,"dishes":[
        {"name":"牛肉麵","desc":"圓頭肉乾金門農牧概念館，金門牛肉麵牛肉乾"}
    ]},
    {"city":"金馬","index":21,"dishes":[
        {"name":"麵線","desc":"馬家麵線，金馬馬祖手工麵線必吃"}
    ]},
    {"city":"金馬","index":28,"dishes":[
        {"name":"廣東粥","desc":"永春廣東粥，金門必吃廣東粥"}
    ]},
    {"city":"金馬","index":45,"dishes":[
        {"name":"魚麵","desc":"阿婆魚麵店，金馬馬祖特色魚麵必吃"}
    ]},
    {"city":"金馬","index":61,"dishes":[
        {"name":"牛肉料理","desc":"金門牛家莊酒糟牛肉料理，金門牛肉專賣"}
    ]},
    {"city":"金馬","index":80,"dishes":[
        {"name":"芋頭冰","desc":"三層樓芋頭餐館芋頭冰，金馬馬祖必吃芋頭冰"}
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