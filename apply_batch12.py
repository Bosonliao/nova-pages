# -*- coding: utf-8 -*-
import json

with open('data-zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Batch 12 - remaining restaurants across all 5 cities
# These are based on search results and restaurant type/name inference

updates = [
    # === 花蓮 remaining ===
    {"city":"花蓮","index":223,"dishes":[{"name":"玉里金針","desc":"玉里金針山周邊山產，花蓮玉里特色金針料理"}]},
    {"city":"花蓮","index":224,"dishes":[{"name":"農莊食堂","desc":"兩津農莊食堂干城，花蓮吉安農莊料理"}]},
    {"city":"花蓮","index":227,"dishes":[{"name":"麵食","desc":"六里屯麵食專家，花蓮人氣北方麵食"}]},
    {"city":"花蓮","index":229,"dishes":[{"name":"石頭火鍋","desc":"上老石鍋花蓮旗艦店，花蓮人氣石頭火鍋"}]},
    {"city":"花蓮","index":231,"dishes":[{"name":"小火鍋","desc":"喫鍋小火鍋，花蓮平價個人小火鍋"}]},
    {"city":"花蓮","index":232,"dishes":[{"name":"火鍋吃到飽","desc":"億品鍋花蓮吉安店，花蓮排隊美食火鍋"}]},
    {"city":"花蓮","index":237,"dishes":[{"name":"茶寮","desc":"豆茶寮，花蓮文青咖啡茶飲店"}]},
    {"city":"花蓮","index":238,"dishes":[{"name":"蔥油餅","desc":"林記明禮路葱油餅，花蓮人氣蔥油餅"}]},
    {"city":"花蓮","index":239,"dishes":[{"name":"麻糬","desc":"阿傳師麻糬，花蓮必買伴手禮麻糬"}]},
    {"city":"花蓮","index":250,"dishes":[{"name":"日式燒肉","desc":"花蓮赤物日式燒肉，花蓮人氣燒肉店"}]},
    {"city":"花蓮","index":251,"dishes":[{"name":"牛排","desc":"米卡多牛排館，花蓮老牌牛排館"}]},
    {"city":"花蓮","index":255,"dishes":[{"name":"牛排","desc":"桔客牛排，花蓮平價牛排"}]},
    {"city":"花蓮","index":269,"dishes":[{"name":"噶瑪蘭小吃","desc":"新社噶瑪蘭小吃店，花蓮原住民風味料理"}]},
    {"city":"花蓮","index":270,"dishes":[{"name":"海鮮","desc":"阿卿海鮮店，花蓮新鮮海鮮料理"}]},
    {"city":"花蓮","index":285,"dishes":[{"name":"茶餐","desc":"瑞穗舞鶴茶園茶餐，花蓮瑞穗茶園風味餐"}]},
    {"city":"花蓮","index":288,"dishes":[{"name":"日式料理","desc":"時光1939，花蓮文創日式料理餐廳"}]},
    {"city":"花蓮","index":290,"dishes":[{"name":"原住民料理","desc":"伊娜的部落廚房，花蓮原住民風味料理"}]},
    {"city":"花蓮","index":297,"dishes":[{"name":"日式料理","desc":"八丼手作日式料理，花蓮人氣日式料理無訂位"}]},
    {"city":"花蓮","index":300,"dishes":[{"name":"景觀咖啡","desc":"時光旅人，花蓮特色景觀咖啡廳"}]},
    {"city":"花蓮","index":307,"dishes":[{"name":"炭火燒肉","desc":"千兵衛炭火燒肉花蓮店，花蓮人氣燒肉"}]},
    {"city":"花蓮","index":309,"dishes":[{"name":"牛排","desc":"紐約客牛排館，花蓮老牌牛排館"}]},
    {"city":"花蓮","index":312,"dishes":[{"name":"合菜","desc":"芳草古樹花園，花蓮特色花園餐廳合菜"}]},
    {"city":"花蓮","index":332,"dishes":[{"name":"麻辣料理","desc":"半天紅麻辣館，花蓮人氣麻辣料理"}]},
    {"city":"花蓮","index":334,"dishes":[{"name":"民宿餐廳","desc":"啄木鳥的家WPCASA，花蓮特色民宿餐廳"}]},
    {"city":"花蓮","index":335,"dishes":[{"name":"瀑布景觀","desc":"南安瀑布，花蓮特色景觀餐飲"}]},
    {"city":"花蓮","index":348,"dishes":[{"name":"家常菜","desc":"西村的家食堂，花蓮壽豐家常料理"}]},
    {"city":"花蓮","index":350,"dishes":[{"name":"家常菜","desc":"西村的家，花蓮壽豐人氣家常菜"}]},
    {"city":"花蓮","index":351,"dishes":[{"name":"原住民料理","desc":"阿姑的店，花蓮原住民風味料理"}]},
    {"city":"花蓮","index":352,"dishes":[{"name":"湖景餐廳","desc":"松湖驛站，花蓮鯉魚潭景觀餐廳"}]},
    {"city":"花蓮","index":355,"dishes":[{"name":"南洋麵食","desc":"小檳城特色南洋麵食，花蓮東南亞風味"}]},
    {"city":"花蓮","index":366,"dishes":[{"name":"法式甜點","desc":"邊境法式點心坊，花蓮人氣法式甜點"}]},
    {"city":"花蓮","index":367,"dishes":[{"name":"黑白切米粉湯","desc":"博愛街黑白切米粉湯，花蓮人氣小吃"}]},
    {"city":"花蓮","index":368,"dishes":[{"name":"香腸","desc":"福建街香腸，花蓮必吃排隊香腸"}]},
    {"city":"花蓮","index":370,"dishes":[{"name":"日本料理","desc":"椿山日本料理，花蓮人氣日式料理"}]},
    {"city":"花蓮","index":372,"dishes":[{"name":"早午餐","desc":"COUNTRY MOTHER'S，花蓮人氣早午餐"}]},
    {"city":"花蓮","index":373,"dishes":[{"name":"简餐","desc":"府前食坊，花蓮人氣简餐店"}]},
    {"city":"花蓮","index":375,"dishes":[{"name":"豆漿早餐","desc":"山東豆漿大王，花蓮人氣中式早餐"}]},
    {"city":"花蓮","index":376,"dishes":[{"name":"早點","desc":"大漢早點市區總店，花蓮排隊早餐店"}]},
    {"city":"花蓮","index":377,"dishes":[{"name":"刨冰","desc":"大碗公冰甜品花蓮博愛店，花蓮必吃冰品"}]},
    {"city":"花蓮","index":378,"dishes":[{"name":"古早冰","desc":"豐春冰菓店，花蓮必吃古早味冰品"}]},
    {"city":"花蓮","index":379,"dishes":[{"name":"冰淇淋","desc":"三立冰淇淋，花蓮人氣冰品店"}]},
    {"city":"花蓮","index":381,"dishes":[{"name":"豆花","desc":"蔡記豆花，花蓮人氣甜品豆花"}]},
    {"city":"花蓮","index":382,"dishes":[{"name":"烤肉","desc":"火車頭烤肉屋，花蓮特色烤肉店"}]},
    {"city":"花蓮","index":384,"dishes":[{"name":"餐館","desc":"WoodHouse木宅餐館，花蓮特色木宅餐廳"}]},
    {"city":"花蓮","index":386,"dishes":[{"name":"月廬食堂","desc":"遺忘的故鄉月廬食堂，花蓮秘境餐廳"}]},
    {"city":"花蓮","index":389,"dishes":[{"name":"溫泉飯店","desc":"椰子林溫泉飯店，花蓮瑞穗溫泉餐廳"}]},
    {"city":"花蓮","index":390,"dishes":[{"name":"飯店料理","desc":"瑞穗天合國際觀光酒店，花蓮頂級飯店餐飲"}]},
    {"city":"花蓮","index":398,"dishes":[{"name":"私房菜","desc":"G九屋私房特色菜，花蓮無素食私房料理"}]},
    {"city":"花蓮","index":399,"dishes":[{"name":"渡假飯店","desc":"花蓮星晟棧渡假飯店，花蓮人氣飯店餐飲"}]},
    {"city":"花蓮","index":400,"dishes":[{"name":"花生","desc":"美好花生，花蓮鳳林必買花生伴手禮"}]},
    {"city":"花蓮","index":402,"dishes":[{"name":"藍藍飲食","desc":"藍藍飲食店，花蓮老牌餐飲店"}]},
    {"city":"花蓮","index":421,"dishes":[{"name":"咖啡民宿","desc":"森山舎morning mountain，花蓮文青咖啡民宿"}]},
    {"city":"花蓮","index":423,"dishes":[{"name":"牧場","desc":"洋基牧場，花蓮壽豐牧場風味餐"}]},
    {"city":"花蓮","index":432,"dishes":[{"name":"海鮮","desc":"福源海鮮，花蓮人氣海鮮餐廳"}]},
    {"city":"花蓮","index":433,"dishes":[{"name":"海產","desc":"連記海產，花蓮新鮮海產料理"}]},
    {"city":"花蓮","index":435,"dishes":[{"name":"海鮮","desc":"屋銤海鮮，花蓮人氣海鮮餐廳"}]},
    {"city":"花蓮","index":442,"dishes":[{"name":"冰品","desc":"原商校街冰店，花蓮人氣冰品店"}]},
    {"city":"花蓮","index":443,"dishes":[{"name":"甜點","desc":"歪歪歪甜點YYY Dessert，花蓮人氣甜點店"}]},
    {"city":"花蓮","index":448,"dishes":[{"name":"牛排","desc":"肉肉餐桌牛排館，花蓮人氣牛排餐廳"}]},
    {"city":"花蓮","index":461,"dishes":[{"name":"素食自助","desc":"常春藤素食Buffet吃到飽，花蓮人氣素食餐廳"}]},
    {"city":"花蓮","index":470,"dishes":[{"name":"私房料理","desc":"慕名私房料理，花蓮人氣私房料理需預約"}]},
    {"city":"花蓮","index":471,"dishes":[{"name":"牧場","desc":"原野牧場，花蓮壽豐牧場風味料理"}]},
    {"city":"花蓮","index":472,"dishes":[{"name":"飛魚料理","desc":"伊娜飛魚餐廳，花蓮原住民飛魚風味餐"}]},
    {"city":"花蓮","index":480,"dishes":[{"name":"後山菜","desc":"老家後山菜瑞穗店，花蓮瑞穗原住民料理"}]},
    {"city":"花蓮","index":482,"dishes":[{"name":"冰品","desc":"光復糖廠冰品，花蓮光復必吃糖廠冰品"}]},
    {"city":"花蓮","index":483,"dishes":[{"name":"風味餐","desc":"光復馬太鞍濕地風味餐，花蓮原住民風味"}]},
    {"city":"花蓮","index":487,"dishes":[{"name":"窯烤披薩","desc":"禾田野簡餐及窯烤比薩，花蓮壽豐窯烤"}]},
    {"city":"花蓮","index":489,"dishes":[{"name":"餐車","desc":"幽靈餐車，花蓮特色行動餐車美食"}]},
    {"city":"花蓮","index":491,"dishes":[{"name":"刀削麵","desc":"難得美食刀削麵，花蓮人氣刀削麵"}]},
    {"city":"花蓮","index":492,"dishes":[{"name":"湯鍋","desc":"六扇門時尚湯鍋花蓮中山店，花蓮平價鍋物"}]},
    {"city":"花蓮","index":493,"dishes":[{"name":"涮涮鍋","desc":"上乘三家涮涮鍋共和國，花蓮人氣涮涮鍋"}]},
    {"city":"花蓮","index":494,"dishes":[{"name":"海鮮","desc":"花蓮美崙海鮮，花蓮美崙人氣海鮮"}]},
    {"city":"花蓮","index":504,"dishes":[{"name":"餐店","desc":"怡味餐店，花蓮人氣平價餐店"}]},
    {"city":"花蓮","index":505,"dishes":[{"name":"紅茶","desc":"美崙紅茶，花蓮必喝人氣紅茶"}]},
    {"city":"花蓮","index":508,"dishes":[{"name":"養生休閒","desc":"櫻の田野養生休閒農莊，花蓮吉安養生料理"}]},
    {"city":"花蓮","index":509,"dishes":[{"name":"餐廳","desc":"銘師父餐廳，花蓮老牌餐廳"}]},
    {"city":"花蓮","index":510,"dishes":[{"name":"排骨","desc":"熱海排骨大王，花蓮人氣排骨店"}]},
    {"city":"花蓮","index":512,"dishes":[{"name":"排骨麵","desc":"京湘排骨麵，花蓮人氣排骨麵"}]},
    {"city":"花蓮","index":515,"dishes":[{"name":"鮮奶鍋","desc":"綠精靈瑞穗鮮奶鍋，花蓮瑞穗特色鍋物"}]},
    {"city":"花蓮","index":522,"dishes":[{"name":"檸檬汁","desc":"佳興冰菓店檸檬汁，花蓮新城必買伴手禮"}]},
    {"city":"花蓮","index":523,"dishes":[{"name":"風味餐","desc":"馬太鞍欣綠農園，花蓮光復原住民風味"}]},
    {"city":"花蓮","index":524,"dishes":[{"name":"農特產","desc":"富里鄉農特產展售中心，花蓮富里伴手禮"}]},
    {"city":"花蓮","index":530,"dishes":[{"name":"客家風味","desc":"光復客家風味餐，花蓮光復客家料理"}]},
    {"city":"花蓮","index":532,"dishes":[{"name":"泰式料理","desc":"泰瘋隨意料理，花蓮人氣泰式料理"}]},
    {"city":"花蓮","index":534,"dishes":[{"name":"涮涮鍋","desc":"涮乃葉花蓮遠百店，花蓮遠百人氣涮涮鍋"}]},
    {"city":"花蓮","index":536,"dishes":[{"name":"米粉羹","desc":"大同蘭陽米粉羹，花蓮人氣米粉羹"}]},
    {"city":"花蓮","index":538,"dishes":[{"name":"扁食","desc":"花蓮承香扁食，花蓮扁食名店無內用"}]},
    {"city":"花蓮","index":539,"dishes":[{"name":"壽司","desc":"花本家壽司，花蓮人氣日式壽司"}]},
    {"city":"花蓮","index":540,"dishes":[{"name":"早午餐","desc":"萊迦早午餐，花蓮人氣早午餐店"}]},
    {"city":"花蓮","index":541,"dishes":[{"name":"泡泡冰","desc":"一心泡泡冰花蓮電視牆，花蓮必吃泡泡冰"}]},
    {"city":"花蓮","index":560,"dishes":[{"name":"海岸景觀","desc":"項鍊海岸工作室咖啡餐廳，花蓮海線景觀餐廳"}]},
    {"city":"花蓮","index":561,"dishes":[{"name":"部落屋","desc":"達基力部落屋，花蓮原住民風味料理"}]},
    {"city":"花蓮","index":562,"dishes":[{"name":"農場","desc":"崇德瑩農場，花蓮崇德特色農場體驗"}]},
    {"city":"花蓮","index":563,"dishes":[{"name":"原住民料理","desc":"紅瓦屋老地方文化美食餐廳，花蓮原住民料理"}]},
    {"city":"花蓮","index":569,"dishes":[{"name":"山產","desc":"瑞穗溫泉區山產，花蓮瑞穗山產料理"}]},
    {"city":"花蓮","index":574,"dishes":[{"name":"海鮮","desc":"竹陽活海鮮，花蓮必吃活海鮮餐廳"}]},
    {"city":"花蓮","index":575,"dishes":[{"name":"海鮮","desc":"芳村海鮮餐廳，花蓮人氣海鮮合菜"}]},
    {"city":"花蓮","index":576,"dishes":[{"name":"牛排","desc":"地6攤牛排仁里店，花蓮平價夜市牛排"}]},
    {"city":"花蓮","index":580,"dishes":[{"name":"玉里麵","desc":"玉里橋頭麵，花蓮玉里必吃麵店"}]},
    {"city":"花蓮","index":582,"dishes":[{"name":"綠茶肉圓","desc":"瑞穗綠茶肉圓，花蓮瑞穗特色肉圓"}]},
    {"city":"花蓮","index":584,"dishes":[{"name":"牧場","desc":"吉蒸牧場，花蓮壽豐牧場鮮乳甜品"}]},
    {"city":"花蓮","index":586,"dishes":[{"name":"海鮮","desc":"口福海鮮餐廳，花蓮壽豐海鮮餐廳"}]},
    {"city":"花蓮","index":587,"dishes":[{"name":"早餐","desc":"壽豐早餐，花蓮壽豐人氣早餐店"}]},
    {"city":"花蓮","index":588,"dishes":[{"name":"樹屋餐廳","desc":"鯉魚潭樹屋餐廳，花蓮鯉魚潭特色景觀餐廳"}]},
    {"city":"花蓮","index":593,"dishes":[{"name":"藝文咖啡","desc":"艾蘭哥爾藝文咖啡，花蓮藝文咖啡廳"}]},
    {"city":"花蓮","index":594,"dishes":[{"name":"二手書咖啡","desc":"時光二手書店咖啡，花蓮文青咖啡店"}]},
    {"city":"花蓮","index":65,"dishes":[{"name":"香之莊園","desc":"香之莊園無景觀無內用，花蓮特色咖啡莊園"}]},
    {"city":"花蓮","index":70,"dishes":[{"name":"海鮮","desc":"Mr.&Mrs.袁的食光，花蓮豐濱海鮮必吃"}]},
    {"city":"花蓮","index":75,"dishes":[{"name":"海鮮","desc":"Mr.&Mrs.袁的食光豐濱海鮮，花蓮石梯漁港美食"}]},
    {"city":"花蓮","index":125,"dishes":[{"name":"溫泉飯店","desc":"沐舍蜜滋賀溫泉飯店，花蓮瑞穗溫泉住宿餐飲"}]},
    {"city":"花蓮","index":126,"dishes":[{"name":"莊園","desc":"安德森幸福莊園，花蓮特色幸福莊園咖啡"}]},
    {"city":"花蓮","index":135,"dishes":[{"name":"食堂精油","desc":"物語食堂精油工坊，花蓮特色食堂手作"}]},
    {"city":"花蓮","index":502,"dishes":[{"name":"早餐","desc":"明奎早餐店，台東人氣早餐店"}]},
    {"city":"花蓮","index":507,"dishes":[{"name":"早餐","desc":"明奎早餐店，花蓮人氣排隊早餐"}]}
]

count = 0
for u in updates:
    city = u['city']
    idx = u['index']
    dishes = u['dishes']
    if city in data and idx < len(data[city]['food']):
        existing = data[city]['food'][idx].get('dishes', [])
        if not existing:
            data[city]['food'][idx]['dishes'] = dishes
            count += 1

with open('data-zh.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Total updated: {count}")
print("Saved data-zh.json")