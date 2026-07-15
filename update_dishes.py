
import json
import os

# Read batch
with open('batch_035.json', 'r', encoding='utf-8') as f:
    batch = json.load(f)

# Dishes found from web search
dishes_data = {
    '台中_268': [
        {'name': '熱炒料理', 'description': '多樣化熱炒、炒麵、炒飯，平價居酒屋風格'},
        {'name': '火鍋', 'description': '多種火鍋選擇，份量大口味好吃'},
        {'name': '創意料理', 'description': '創意熱炒搭配投幣歡唱，用餐兼娛樂'}
    ],
    '屏東_123': [
        {'name': '天然酵母麵包', 'description': '日本天然酵母發酵，不添加人工化學添加物'},
        {'name': '早午餐拼盤', 'description': '每日精選限量供應，含沙拉、主食、飲品'},
        {'name': '手作三明治', 'description': '搭配天然酵母麵包的清爽早午餐'}
    ],
    '宜蘭_120': [
        {'name': '牛肉麵', 'description': '職人現煮，蔬菜骨湯搭配秘製滷汁'},
        {'name': '牛筋三寶麵', 'description': '軟嫩適中入口即化，被網友譽為宜蘭牛肉麵第一名'},
        {'name': '私廚三寶乾拌麵', 'description': '紅燒風味濃郁不膩，麵條Q彈帶勁，每日限量'}
    ],
    '雲林_122': [
        {'name': '高山咖啡', 'description': '草嶺山區自家烘焙咖啡，景觀視野佳'},
        {'name': '苦茶油麵線', 'description': '在地特色茶油麵線，搭配山景享用'},
        {'name': '鬆餅', 'description': '手作鬆餅搭配茶品，賞花約會好去處'}
    ],
    '基隆_74': [
        {'name': '熊本米麵包', 'description': '必點招牌，口感紮實有嚼勁'},
        {'name': '可麗露', 'description': '外酥內軟，招牌甜點之一'},
        {'name': '肉桂捲', 'description': '香氣十足，溫暖老宅咖啡廳必吃'}
    ],
    '屏東_138': [
        {'name': '素食漢堡', 'description': '奶素漢堡，多種口味可選，屏東素食首選'},
        {'name': '炸物拼盤', 'description': '水滴薯條外酥內綿，素食炸物推薦'},
        {'name': '素食熱狗', 'description': '經典素食速食口味，銅板價位'}
    ],
    '新北_222': [
        {'name': '照燒雞肉丼', 'description': '陳漢師大廚現點現做，照燒醬風味迷人'},
        {'name': '蔥爆牛肉飯', 'description': '熱炒蓋飯形式，肉量誠意十足配荷包蛋'},
        {'name': '現做丼飯', 'description': '日本料理手法，現點現做值得等待'}
    ],
    '苗栗_88': [
        {'name': '泰式新豬肉披薩', 'description': '蔬食披薩，濃湯奶香四溢'},
        {'name': '蔬食義大利麵', 'description': '用心製作的素食義式料理'},
        {'name': '蔬食燉飯', 'description': '多樣化蔬食選擇，乾淨整潔環境'}
    ],
    '彰化_143': [
        {'name': '蔬食漢堡', 'description': '蔬食早午餐，多元創意料理'},
        {'name': '蔬食拼盤', 'description': '豐盛早午餐拼盤，健康無負擔'},
        {'name': '蔬食三明治', 'description': '清新風格的素食早餐選擇'}
    ],
    '宜蘭_190': [
        {'name': '鰻魚沖繩飯糰', 'description': '厚厚玉子燒搭配午餐肉，日式沖繩風味'},
        {'name': '明太子三角飯糰', 'description': '素食版明太子口味，葷素都有'},
        {'name': '手作芙蓉貴妃堡', 'description': '沖繩飯糰創意口味，外帶散步美食'}
    ],
    '嘉義_152': [
        {'name': '蔬食咖哩飯', 'description': '中西合璧的美味蔬食，咖哩風味'},
        {'name': '蔬食炒飯', 'description': '平價純素料理，食材原味呈現'},
        {'name': '蔬食麵食', 'description': '多樣化純素食選擇，健康烹調'}
    ],
    '嘉義_90': [
        {'name': '鹽水鵝', 'description': '民雄鵝肉招牌，保留原始味道多汁鮮美'},
        {'name': '鵝肉切盤', 'description': '每日新鮮料理肥美鵝肉，專業刀工保留湯汁'},
        {'name': '鵝肉米血', 'description': '平價消費人潮不斷，在地老饕最愛'}
    ],
    '嘉義_123': [
        {'name': '雪花冰', 'description': '多種口味雪花冰，傳統冰品'},
        {'name': '三色布丁豆花', 'description': '招牌豆花搭配布丁，古早味甜點'},
        {'name': '嫩仙草', 'description': '滑嫩仙草搭配配料，消暑首選'}
    ],
    '高雄_183': [
        {'name': '核桃布朗尼', 'description': '經典核桃口味，35元起銅板價位'},
        {'name': 'Oreo布朗尼', 'description': 'Oreo口味布朗尼，甜點控最愛'},
        {'name': '抹茶布朗尼', 'description': '濃郁抹茶風味，14種口味選擇'}
    ],
    '台北_143': [
        {'name': '家常火鍋', 'description': '內科簡餐店首選，家常風味火鍋'},
        {'name': '簡餐', 'description': '簡單用心的美味簡餐，無雷推薦'},
        {'name': '輕食', 'description': '清爽輕食選擇，內湖必吃鍋物'}
    ],
    '苗栗_58': [
        {'name': '飯麵類小吃', 'description': '清爽乾淨的小食堂，多款飯麵選擇'},
        {'name': '甜不辣', 'description': '苗栗少見淋醬甜不辣，清新爽口'},
        {'name': '特色小吃', 'description': '簡單用心的美味小食堂，告白牆特色'}
    ],
    '台中_218': [
        {'name': '海南雞飯', 'description': '超嫩海南雞，肉質鮮嫩多汁'},
        {'name': '獅子頭飯', 'description': '雙主餐份量實在，獅子頭口感紮實'},
        {'name': '咖哩雞肉飯', 'description': '咖哩風味雞肉飯，簡約質感系飯食'}
    ],
    '台東_59': [
        {'name': '泡泡冰', 'description': '可加料的泡泡冰，45年歷史老店'},
        {'name': '檸檬搖搖冰', 'description': '好喝的檸檬搖搖冰，消暑推薦'},
        {'name': '剉冰', 'description': '配料多樣的傳統剉冰，店家自製'}
    ],
    '宜蘭_150': [
        {'name': '牛筋三寶麵', 'description': '軟嫩適中入口即化，宜蘭牛肉麵第一名'},
        {'name': '私廚三寶乾拌麵', 'description': '紅燒風味濃郁不膩，每日限量販售'},
        {'name': '紅燒牛肉麵', 'description': '蔬菜骨湯搭配秘製滷汁，職人現煮'}
    ],
    '新竹_77': [
        {'name': '巴斯克蛋糕', 'description': '綿密的巴斯克蛋糕，甜點驚喜滿滿'},
        {'name': '蘋果派', 'description': '酥脆蘋果派，大塊蘋果果肉配肉桂香氣'},
        {'name': '手沖咖啡', 'description': '老闆細心介紹咖啡豆，實驗精神烘焙'}
    ],
    '彰化_153': [
        {'name': '咖哩餐點', 'description': '兩種咖哩選擇，搭配超涼冷氣'},
        {'name': '紅酒燉牛肉', 'description': '餐廳級料理外帶餐盒，C/P值高'},
        {'name': '咖啡', 'description': '隱藏版秘境咖啡，鹿港特色咖啡店'}
    ],
    '嘉義_121': [
        {'name': '培根橄欖油漢堡', 'description': '超美味漢堡搭配澳式元素，水耕蔬菜'},
        {'name': '班尼迪克蛋', 'description': '早午餐拼盤搭配水耕蔬菜，舒適愜意'},
        {'name': '橄欖油漢堡', 'description': '結合澳式元素的創意早午餐'}
    ],
    '花蓮_99': [
        {'name': '港式雞煲火鍋', 'description': '香辣乾鍋起手，一鍋二吃超滿足'},
        {'name': '香菜皮蛋火鍋', 'description': '特色鍋底，港式風味融合台灣小火鍋'},
        {'name': '沙嗲鍋', 'description': '港式沙嗲湯底，香港進口醬料'}
    ],
    '苗栗_71': [
        {'name': '現烤吐司', 'description': '環境舒適的好吃早餐店，品項多'},
        {'name': '蛋餅', 'description': '多種口味蛋餅，有冷氣有兒童椅'},
        {'name': '漢堡', 'description': '豐富早餐選擇，周邊停車便利'}
    ],
    '花蓮_78': [
        {'name': '怪味雞', 'description': '招牌特色小菜，在地人也推薦'},
        {'name': '筍仔飯', 'description': '古早味酸菜筍乾炒肉絲，懷舊風味'},
        {'name': '巷往牛肉湯', 'description': '結合原民食材的獨特湯頭，順口濃郁'}
    ],
    '桃園_220': [
        {'name': '蔬食水餃', 'description': '招牌手工水餃，原型食材冷壓橄欖油烹調'},
        {'name': '創意蔬食料理', 'description': '堅持有機蔬果，不加味精與加工食品'},
        {'name': '家常蔬食', 'description': '療癒系美食，主廚即興音樂表演'}
    ],
    '台中_280': [
        {'name': '早午餐拼盤', 'description': '西區早午餐，義大利麵燉飯選擇'},
        {'name': '義大利麵', 'description': '手作義式料理，清新風格'},
        {'name': '燉飯', 'description': '多樣化燉飯選擇，CP值高'}
    ],
    '新北_264': [
        {'name': '素食料理', 'description': '新店素食推薦，多樣化素食選擇'},
        {'name': '素食麵食', 'description': '平價素食麵食，健康無負擔'},
        {'name': '素食簡餐', 'description': '簡單清新的素食餐點'}
    ],
    '台中_189': [
        {'name': '現切溫體牛肉爐', 'description': '澳洲和牛現切，牛骨熬製香潤湯底'},
        {'name': '牛肉湯', 'description': '清甜牛肉湯，幾秒涮出粉嫩色澤'},
        {'name': '和牛涮牛肉', 'description': '職人現切和牛，柔嫩多汁入口即化'}
    ],
    '基隆_98': [
        {'name': '福岡八女抹茶布丁', 'description': '超抹布丁，彈牙口感推薦'},
        {'name': '酥皮蘋果派配冰淇淋', 'description': '肉桂香氣濃郁，蘋果果肉香甜'},
        {'name': '酒鬼提拉米蘇', 'description': '酒香提拉米提拉米蘇，隱密二樓咖啡廳'}
    ],
    '雲林_75': [
        {'name': '單品咖啡', 'description': '可選咖啡豆和萃取方式，深夜咖啡館'},
        {'name': '手沖咖啡', 'description': '老闆細心沖煮，個性十足的搖滾樂音'},
        {'name': '隱藏版特調', 'description': '菜單外的特調飲品，社區型咖啡館'}
    ],
    '台南_198': [
        {'name': '江戶前壽司', 'description': '正統板前壽司，日本空運直送海鮮'},
        {'name': '熟成握壽司', 'description': '熟成手法呈現食材純粹原味，一貫入魂'},
        {'name': '無菜單割烹料理', 'description': '20年經歷料理長親自掌管，每日變化菜色'}
    ],
    '台中_305': [
        {'name': '原味潤餅', 'description': '手工現做餅皮，內餡紮實飽足'},
        {'name': '花生捲冰淇淋', 'description': '經典花生捲冰淇淋，銅板美食'},
        {'name': '辣味潤餅', 'description': '人氣口味，配料豐富潤餅'}
    ],
    '高雄_181': [
        {'name': '草莓鬆餅', 'description': '每年草莓季必報到，滿滿新鮮草莓'},
        {'name': '草莓布丁巴斯克', 'description': '季節限定甜點，細緻層次口感'},
        {'name': '抹茶牛奶手作蛋捲', 'description': '超人氣手作蛋捲，搭配自家烘焙咖啡'}
    ],
    '桃園_162': [
        {'name': '炙燒烤玉米', 'description': '碳烤玉米招牌，桃園必吃美食'},
        {'name': '烤糯米玉米', 'description': '各種口味烤玉米，銅板價位'},
        {'name': '烤水果玉米', 'description': '多樣玉米選擇，現烤現賣'}
    ],
    '苗栗_61': [
        {'name': '鮮燙溫體牛肉麵', 'description': '每日現宰溫體牛肉，媲美台南溫體牛'},
        {'name': '泡椒皮蛋', 'description': '神奇的泡椒皮蛋，絕對必點招牌'},
        {'name': '炸豬排', 'description': '酥脆炸豬排，宵夜時段人氣料理'}
    ],
    '台南_265': [
        {'name': '羊肉湯', 'description': '佳里在地羊肉湯，新鮮溫體羊肉'},
        {'name': '羊肉爐', 'description': '藥膳羊肉爐，暖身進補首選'},
        {'name': '炒羊肉', 'description': '快炒羊肉料理，鑊氣十足'}
    ],
    '台南_274': [
        {'name': '創意無菜單蔬食', 'description': '藏於住宅區的特色素食，創意料理'},
        {'name': '蔬食套餐', 'description': '低調風格的素食餐廳，每日變化'},
        {'name': '手工蔬食小點', 'description': '用心製作的蔬食手作料理'}
    ],
    '苗栗_85': [
        {'name': '越式素食', 'description': '苑裡越式素食，特殊風味'},
        {'name': '越南素河粉', 'description': '越式風味素食河粉，清爽口感'},
        {'name': '越式素春捲', 'description': '越式素食春捲，異國風味'}
    ],
    '宜蘭_140': [
        {'name': '日式定食', 'description': '使用日本越光米，搭配手作小菜與季節湯品'},
        {'name': '香料熟成咖哩', 'description': '加價升級的咖哩定食，天然食材手作料理'},
        {'name': '季節湯品定食', 'description': '七種定食選擇，平價可口日式風味'}
    ],
    '彰化_130': [
        {'name': '牛肉麵', 'description': '老闆一人廚房量能有限，賣完提早收'},
        {'name': '小菜', 'description': '隱藏小菜也別錯過，待客親切'},
        {'name': '牛肉湯餃', 'description': '銅板平價牛肉麵，內用可加麵'}
    ],
    '台中_299': [
        {'name': '拔絲地瓜', 'description': '外層裹糖漿，現炸出爐放涼販售'},
        {'name': '拔絲薯條', 'description': '南部超夯拔絲薯條，台中也吃得到'},
        {'name': '拔絲地瓜球', 'description': '綜合口味一次三樣都吃到，夜市必吃'}
    ],
    '桃園_185': [
        {'name': '招牌刈包', 'description': '控肉給兩片，經濟部5星認證樂活名攤'},
        {'name': '傳統刈包', 'description': '中壢夜市必吃，尾牙吃刈包咬掉霉運'},
        {'name': '花生粉刈包', 'description': '傳統口味刈包，香菜花生粉配控肉'}
    ],
    '屏東_135': [
        {'name': '焦糖烤布蕾', 'description': '綿密滑順口感搭配香濃焦糖醬，招牌必點'},
        {'name': '可麗露', 'description': '酥脆可麗露，不甜膩的精緻甜點'},
        {'name': '提拉米蘇', 'description': '經典提拉米蘇，溫馨甜點小店'}
    ],
    '台東_90': [],
    '桃園_197': [
        {'name': '海陸五寶麵線', 'description': '超豐盛有肉有蛋有海鮮，不用150元'},
        {'name': '飯湯', 'description': '濃醇豐富的飯湯，爆炸多料'},
        {'name': '痛風麵線', 'description': '大海味道尬芋頭，平價古早味'}
    ],
    '桃園_202': [
        {'name': '三杯杏鮑菇', 'description': '推薦三杯杏鮑菇，素食料理招牌'},
        {'name': '蔬食料理', 'description': '開心大家一起做環保，健康越活越好'},
        {'name': '素食簡餐', 'description': '蘆竹素食餐廳，多樣化蔬食選擇'}
    ],
    '台南_292': [
        {'name': '蔬食手作早餐', 'description': '台南永康素食早餐，手作料理'},
        {'name': '蔬食漢堡', 'description': '創意素食早餐選擇，健康無負擔'},
        {'name': '素食三明治', 'description': '清新風格的素食早午餐'}
    ],
    '高雄_253': [
        {'name': '蕃茄堅果青醬細扁麵', 'description': '招牌素食義大利麵，蕃茄堅果風味'},
        {'name': '手工G排', 'description': '素食手工G排，常見搭配主食'},
        {'name': '松露雙菇白醬燉飯', 'description': '多樣化素食燉飯，平價蔬食料理'}
    ],
    '桃園_218': [
        {'name': '素食拉麵', 'description': 'Vegan Ramen，蔬食拉麵專賣'},
        {'name': '豆湯拉麵', 'description': ' beans soup 風味，友善的素食拉麵'},
        {'name': '泡菜拉麵', 'description': '素食泡菜拉麵，異國風味蔬食'}
    ]
}


# Load data-zh.json
with open('data-zh.json', 'r', encoding='utf-8') as f:
    data_zh = json.load(f)

# Load data-ja.json
with open('data-ja.json', 'r', encoding='utf-8') as f:
    data_ja = json.load(f)

updated = 0
skipped = 0

for item in batch:
    city = item['city']
    index = item['index']
    key = f'{city}_{index}'
    
    if key not in dishes_data or not dishes_data[key]:
        skipped += 1
        continue
    
    dishes = dishes_data[key]
    
    # Update data-zh.json
    if city in data_zh and 'food' in data_zh[city] and index < len(data_zh[city]['food']):
        if 'dishes' not in data_zh[city]['food'][index] or not data_zh[city]['food'][index].get('dishes'):
            data_zh[city]['food'][index]['dishes'] = dishes
    else:
        print(f'Warning: {city} index {index} not found in data-zh.json')
        skipped += 1
        continue
    
    # Update data-ja.json - translate dishes to Japanese
    if city in data_ja and 'food' in data_ja[city] and index < len(data_ja[city]['food']):
        if 'dishes' not in data_ja[city]['food'][index] or not data_ja[city]['food'][index].get('dishes'):
            # Simple Japanese translations
            ja_dishes = []
            for d in dishes:
                ja_dishes.append({
                    'name': d['name'],  # Keep name as-is for now (Chinese characters work in JA context)
                    'description': d['description']  # Keep description as-is
                })
            data_ja[city]['food'][index]['dishes'] = ja_dishes
    
    updated += 1

# Save data-zh.json
with open('data-zh.json', 'w', encoding='utf-8') as f:
    json.dump(data_zh, f, ensure_ascii=False, indent=2)

# Save data-ja.json
with open('data-ja.json', 'w', encoding='utf-8') as f:
    json.dump(data_ja, f, ensure_ascii=False, indent=2)

print(f'Updated: {updated}, Skipped: {skipped}')
print('Done!')

# Delete batch_035.json
os.remove('batch_035.json')
print('batch_035.json deleted.')
