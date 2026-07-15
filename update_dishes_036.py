import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load both data files
with open('data-zh.json', 'r', encoding='utf-8') as f:
    data_zh = json.load(f)
with open('data-ja.json', 'r', encoding='utf-8') as f:
    data_ja = json.load(f)

# Define dishes for each restaurant based on search results
# Format: (city, index, [dishes_zh], [dishes_ja])
updates = [
    # 1. Shangrila Buddha - 屏東 96 - Albany CA restaurant, limited Chinese info
    # Skip - this is a California restaurant, no Taiwan-specific dishes found
    
    # 2. 波羅密素食館 - 新北 282
    ("新北", 282, [
        {"name": "素食炒麵", "description": "人氣主食，配料豐富份量足"},
        {"name": "麻婆豆腐", "description": "素食版本，香辣下飯"},
        {"name": "羅漢齋", "description": "多種蔬菜混炒，清爽健康"}
    ], [
        {"name": "野菜焼きそば", "description": "人気の主食、具だくさんでボリューム満点"},
        {"name": "麻婆豆腐（ベジタリアン）", "description": "素食版のピリ辛麻婆豆腐"},
        {"name": "羅漢斎", "description": "多種の野菜を炒めたヘルシーな一皿"}
    ]),
    
    # 3. 晨間廚房早午餐 - 彰化 184
    ("彰化", 184, [
        {"name": "炒泡麵", "description": "招牌必點，麻辣風味炒泡麵"},
        {"name": "奶酥厚片", "description": "人氣早午餐項目，奶香濃郁"},
        {"name": "脆皮蛋餅", "description": "外酥內軟的台式蛋餅"}
    ], [
        {"name": "炒め即席麺", "description": "看板メニュー、ピリ辛風味の炒め麺"},
        {"name": "ミルクトースト", "description": "人気の朝食メニュー、濃厚なミルク風味"},
        {"name": " crispy蛋餅", "description": "外はカリカリ中はフワフワの台湾式卵餅"}
    ]),
    
    # 4. 恩潔素食 - 台南 285 - limited info, skip
    
    # 5. 覺豆咖啡 - 新竹 802
    ("新竹", 802, [
        {"name": "靈感特調咖啡", "description": "店長依客人狀態調配專屬風味咖啡，附籤詩"},
        {"name": "檸檬塔", "description": "招牌甜點，使用整顆檸檬製作，酸甜清爽"},
        {"name": "肉桂捲", "description": "每日現做，可選鬆軟或酥脆口感"}
    ], [
        {"name": "霊感特調コーヒー", "description": "店長が客の状態に合わせて調合する専用コーヒー、おみくじ付き"},
        {"name": "レモンタルト", "description": "看板スイーツ、丸ごとレモン使用、甘酸っぱくさっぱり"},
        {"name": "シナモンロール", "description": "毎日手作り、ふわふわかサクサクか選べる"}
    ]),
    
    # 6. 誠農食堂X翌莎咖啡 - 嘉義 135
    ("嘉義", 135, [
        {"name": "舒肥嫩雞胸日式咖哩飯", "description": "招牌主食，舒肥雞胸搭配自製咖哩"},
        {"name": "自釀高粱梅子醋", "description": "店內自釀，酸甜解膩"},
        {"name": "精品咖啡", "description": "2019世界盃測師台灣區冠軍品質"}
    ], [
        {"name": "舒肥鶏胸肉の日本式カレー", "description": "看板メニュー、低温調理鶏胸肉と自家製カレー"},
        {"name": "自家醸造高粱梅子酢", "description": "店内醸造、甘酸っぱくさっぱり"},
        {"name": "スペシャリティコーヒー", "description": "2019年ワールドカップテイスター台湾チャンピオン品質"}
    ]),
    
    # 7. 茶汕鼎鍋物 - 台中 311 - search returned wrong restaurant (鍋泰暖)
    # Skip - can't confirm specific dishes for this restaurant
    
    # 8. 逸鄉村 YST - 宜蘭 124
    ("宜蘭", 124, [
        {"name": "流淚吐司", "description": "招牌必買，口感柔軟讓人感動流淚"},
        {"name": "爆漿饅頭", "description": "多種口味，粉圓鮮奶、起司鮮奶等人氣選項"},
        {"name": "巴斯克芝士蛋糕", "description": "濃郁芝士風味，每日限量"}
    ], [
        {"name": "涙トースト", "description": "看板商品、柔らかい食感で感動して涙が出る"},
        {"name": "爆饅頭", "description": "多種フレーバー、タピオカミルクやチーズミルクが人気"},
        {"name": "バスクチーズケーキ", "description": "濃厚チーズ風味、数量限定"}
    ]),
    
    # 9. 邱記古早味黑糖剉冰 - 基隆 111 - new shop, no dish info found
    # Skip
    
    # 10. 蕭家古厝 - 苗栗 83 - search returned different restaurants
    # Skip - no specific dish info for this restaurant
    
    # 11. CYL Coffee - 苗栗 665
    ("苗栗", 665, [
        {"name": "手作甜點", "description": "每日現做甜點，種類依當日製作"},
        {"name": "手沖咖啡", "description": "SCA認證咖啡，精品莊園豆"},
        {"name": "特調咖啡", "description": "創意風味特調，口感豐富"}
    ], [
        {"name": "手作スイーツ", "description": "毎日手作り、種類は日によって異なる"},
        {"name": "ハンドドリップコーヒー", "description": "SCA認証コーヒー、スペシャリティ豆"},
        {"name": "特調コーヒー", "description": "クリエイティブな風味特調、豊かな味わい"}
    ]),
    
    # 12. INITA - 台北 982
    ("台北", 982, [
        {"name": "生牛肉韃靼銅鑼燒", "description": "米其林招牌菜，台灣黃牛生牛肉搭配銅鑼燒外型"},
        {"name": "無菜單料理", "description": "日義台融合創意套餐，板前互動歡樂"},
        {"name": "餐酒搭配", "description": "Half/Full Glass 葡萄酒 pairing 套餐"}
    ], [
        {"name": "生牛肉タルタルどら焼き", "description": "ミシュラン看板料理、台湾産牛肉のタルタルをどら焼き型で"},
        {"name": "おまかせコース", "description": "日・伊・台融合のクリエイティブコース"},
        {"name": "ワインペアリング", "description": "ハーフグラス/フルグラスのワインペアリング"}
    ]),
    
    # 13. 天香素食園 - 花蓮 131
    ("花蓮", 131, [
        {"name": "炒河粉", "description": "招牌菜，越式風味炒河粉"},
        {"name": "水餃", "description": "人氣菜品，皮Q餡香"},
        {"name": "咖哩麵", "description": "濃郁咖哩風味，值得一試"}
    ], [
        {"name": "焼きビーフン", "description": "看板料理、ベトナム風味の炒めビーフン"},
        {"name": "水餃子", "description": "人気メニュー、皮はモチモチ餡は香り豊か"},
        {"name": "カレー麺", "description": "濃厚カレー風味、一食の価値あり"}
    ]),
    
    # 14. 山茶話堂 - 南投 110
    ("南投", 110, [
        {"name": "秘製滷味", "description": "獨家秘方滷製，每日限量供應"},
        {"name": "水果千層蛋糕", "description": "每日限量手作千層蛋糕，清爽水果風味"},
        {"name": "高山金萱茶", "description": "自家產茶，現點現沖回甘溫醇"}
    ], [
        {"name": "秘製滷味", "description": "独自の秘方で滷製、数量限定"},
        {"name": "フルーツミルフィーユ", "description": "毎日限定手作りミルフィーユ、さわやかなフルーツ風味"},
        {"name": "高山金萱茶", "description": "自家産茶、注文ごとに淹れる、甘みのある味わい"}
    ]),
    
    # 15. 青珍坊牛舌餅 - 彰化 182
    ("彰化", 182, [
        {"name": "麥芽牛舌餅", "description": "招牌產品，好吃不黏牙的麥芽口味"},
        {"name": "黑糖牛舌餅", "description": "古早味黑糖風味，香酥可口"},
        {"name": "蜂蜜薄脆片", "description": "薄片口感，蜂蜜香氣十足"}
    ], [
        {"name": "麦芽牛舌餅", "description": "看板商品、美味しくて歯にくっつかない麦芽味"},
        {"name": "黒糖牛舌餅", "description": "昔ながらの黒糖風味、香ばしく美味"},
        {"name": "蜂蜜薄脆片", "description": "薄い食感、蜂蜜の香り豊か"}
    ]),
    
    # 16. Soban Vegan Restaurant - 金馬 6 - no specific info found
    # Skip
    
    # 17. 文化鵝肉店 - 嘉義 134
    ("嘉義", 134, [
        {"name": "煙燻鵝肉", "description": "招牌菜，肉質扎實煙燻香氣，不沾醬就夠味"},
        {"name": "鵝肉飯", "description": "鵝油包裹米飯，搭配鵝肉油蔥筍絲"},
        {"name": "鵝肉冬粉", "description": "清甜鵝湯搭配冬粉，清爽順口"}
    ], [
        {"name": "燻製ガチョウ肉", "description": "看板料理、肉質しっかり燻製香り、タレ不要で美味"},
        {"name": "ガチョウ肉ご飯", "description": "ガチョウ油で包んだご飯、ガチョウ肉と玉葱筍添え"},
        {"name": "ガチョウ肉ビーフン", "description": "甘辛いガチョウスープとビーフン、さっぱり美味"}
    ]),
    
    # 18. 瓦咖喱家 - 高雄 284
    ("高雄", 284, [
        {"name": "炸豬排咖哩飯", "description": "富士山造型咖哩飯，厚實豬排搭配蔬菜咖哩"},
        {"name": "日式丼飯", "description": "文青日系風格丼飯，多種口味"},
        {"name": "唐揚雞", "description": "酥脆日式炸雞，內用優惠贈品"}
    ], [
        {"name": "とんかつカレーライス", "description": "富士山型カレーライス、厚切とんかつと野菜カレー"},
        {"name": "日式丼飯", "description": "文青和風丼飯、多种口味"},
        {"name": "唐揚げ", "description": "サクサク日式唐揚げ、内用特典付き"}
    ]),
    
    # 19. 許記麵線羹麵 - 桃園 105
    ("桃園", 105, [
        {"name": "大腸麵線", "description": "招牌麵線，胡椒香氣濃郁"},
        {"name": "肉羹麵", "description": "人氣主食，肉羹有胡椒香"},
        {"name": "魷魚羹", "description": "鮮甜魷魚羹湯頭"}
    ], [
        {"name": "大腸麺線", "description": "看板麺線、胡椒の香り豊か"},
        {"name": "肉羹麺", "description": "人気の主食、肉羹に胡椒の香り"},
        {"name": "いか羹", "description": "甘いいか羹スープ"}
    ]),
    
    # 20. 日日素食 - 台中 331
    ("台中", 331, [
        {"name": "香椿麵", "description": "招牌必吃，香椿風味獨特"},
        {"name": "紅燒湯", "description": "配麵最佳搭檔，玉米甜香"},
        {"name": "筍乾飯", "description": "平價小菜，筍乾入味"}
    ], [
        {"name": "椿麺", "description": "看板メニュー、椿の風味が独特"},
        {"name": "紅焼スープ", "description": "麺のベストパートナー、玉米の甘み"},
        {"name": "筍乾ご飯", "description": "お手頃な副菜、味しみ筍乾"}
    ]),
    
    # 21. 存在咖啡 - 桃園 1004 - no specific dishes found
    # Skip
    
    # 22. 資豐美食 豐原店 - 台中 211
    ("台中", 211, [
        {"name": "麻油飯", "description": "招牌必點，粒粒分明香氣縈繞的麻油飯"},
        {"name": "傳統炒麵", "description": "彈牙滑嫩麵條搭配獨門醬料，鹹香夠味"},
        {"name": "餛飩湯", "description": "鮮美餛飩搭配清甜高湯"}
    ], [
        {"name": "麻油飯", "description": "看板メニュー、一粒一粒がはっきりした麻油飯"},
        {"name": "伝統炒め麺", "description": "コシのある麺と自家製タレ、塩辛い味付け"},
        {"name": "ワンタンスープ", "description": "美味しいワンタンと甘い出汁"}
    ]),
    
    # 23. 品饌蔬食館 - 台中 324 - limited specific dish info
    # Skip
    
    # 24. 蔬植 純素料理 - 新北 266 - no specific dish info found
    # Skip
    
    # 25. 拾山現炒 - 台中 212 - limited specific dish info
    # Skip
    
    # 26. 大大尾義大利家常料理 - 雲林 76
    ("雲林", 76, [
        {"name": "橄欖油義大利麵", "description": "最樸素卻讓人想再來一盤，麵心口感正統"},
        {"name": "番茄肉醬義大利麵", "description": "新鮮食材製成的平價家常味"},
        {"name": "義式湯品", "description": "不假他人之手的自製湯品"}
    ], [
        {"name": "オリーブオイルパスタ", "description": "最もシンプルだがリピートしたくなる、芯のある麺"},
        {"name": "トマトミートソースパスタ", "description": "新鮮食材で作ったお手頃な家庭の味"},
        {"name": "伊式スープ", "description": "手作りのスープ、市販品不使用"}
    ]),
    
    # 27. 古坑古濃精品咖啡 - 雲林 119
    ("雲林", 119, [
        {"name": "台灣高山精品咖啡", "description": "高山經典杏仁奶香微果酸，在地冠軍咖啡"},
        {"name": "艾蒙冠軍咖啡", "description": "堅果香氣檸檬茶焦糖感，2022冠軍豆"},
        {"name": "非洲花王", "description": "柑橘草莓花香熱帶水果風味"}
    ], [
        {"name": "台湾高山精品コーヒー", "description": "高山アーモンドミルク香り微果酸、地元チャンピオン豆"},
        {"name": "エイモンチャンピオンコーヒー", "description": "ナッツ香りレモン茶キャラメル感、2022チャンピオン豆"},
        {"name": "アフリカ花王", "description": "柑橘いちご花香熱帯果実風味"}
    ]),
    
    # 28. 嵐畇小籠湯包 - 台中 195
    ("台中", 195, [
        {"name": "小籠湯包", "description": "現包現蒸皮薄餡多，咬下爆汁"},
        {"name": "虱目魚風味湯包", "description": "特色口味，鮮美虱目魚內餡"},
        {"name": "酸辣湯", "description": "料多豐富，搭配湯包最佳"}
    ], [
        {"name": "小籠湯包", "description": "手作り蒸したて皮薄餡多、噛むと汁が溢れる"},
        {"name": "虱目魚風味湯包", "description": "特色口味、美味しい虱目魚餡"},
        {"name": "酸辣湯", "description": "具だくさん、湯包にベストマッチ"}
    ]),
    
    # 29. 胡同李東北水餃 - 台中 196
    ("台中", 196, [
        {"name": "酸白菜豬肉水餃", "description": "招牌必吃，自然發酵酸白菜搭配豬肉，開胃爽脆"},
        {"name": "招牌香蔥豬肉水餃", "description": "每日溫體豬現調現包，口感筋道"},
        {"name": "高麗菜豬肉水餃", "description": "經典口味，新鮮高麗菜配溫體豬肉"}
    ], [
        {"name": "酸白菜豚肉水餃", "description": "看板メニュー、自然発酵の酸白菜と豚肉、開胃でシャキシャキ"},
        {"name": "看板香葱豚肉水餃", "description": "毎日新鮮豚肉を手作り、コシのある食感"},
        {"name": "キャベツ豚肉水餃", "description": "定番口味、新鮮キャベツと新鮮豚肉"}
    ]),
    
    # 30. 饗二林莊園 - 彰化 189
    ("彰化", 189, [
        {"name": "鮮食葡萄糖醋大黃魚", "description": "無菜單料理招牌菜，使用二林在地葡萄入菜"},
        {"name": "火龍果龍蝦沙拉刈包", "description": "在地火龍果搭配龍蝦沙拉，清爽香甜"},
        {"name": "二林在地香米炒飯", "description": "使用二林冠軍馥米製作"}
    ], [
        {"name": "ブドウ酢豚大魚", "description": "おまかせ料理の看板、二林産ブドウ使用"},
        {"name": "ドラゴンフルーツロブスターサラダー刈包", "description": "地元ドラゴンフルーツとロブスターサラダー、さっぱり甘い"},
        {"name": "二林産香米チャーハン", "description": "二林チャンピオン馥米使用"}
    ]),
    
    # 31. 澤喆稱奇 蔬食餐廳 - 雲林 77
    ("雲林", 77, [
        {"name": "全蔬食料理", "description": "歐式古典風格全蔬食，不含蛋奶"},
        {"name": "植物甜點", "description": "無蛋奶甜點，精緻美味"},
        {"name": "植物飲品", "description": "無蛋奶飲品，咖啡與茶飲"}
    ], [
        {"name": "全蔬食料理", "description": "欧式古典風の全蔬食、卵乳不使用"},
        {"name": "植物スイーツ", "description": "卵乳不使用の精緻なデザート"},
        {"name": "植物ドリンク", "description": "卵乳不使用のドリンク、コーヒーと茶"}
    ]),
    
    # 32. 東港集旺黑鮪魚專賣店 - 屏東 131
    ("屏東", 131, [
        {"name": "黑鮪魚生魚片", "description": "當日現撈黑鮪魚，肉質細緻油脂豐富"},
        {"name": "黑鮪魚握壽司", "description": "現切黑鮪魚搭配醋飯，鮮美無比"},
        {"name": "黑鮪魚燒烤", "description": "從刺身到燒烤樣樣到位，老饕推薦"}
    ], [
        {"name": "黒鮪刺身", "description": "当日の鮮魚、肉質きめ細かく脂豊か"},
        {"name": "黒鮪握り寿司", "description": "切り立て黒鮪と酢飯、極上の美味"},
        {"name": "黒鮪焼き物", "description": "刺身から焼き物まで何でも対応、通好み"}
    ]),
    
    # 33. 泰機車泰客蔬食 - 基隆 75
    ("基隆", 75, [
        {"name": "桔醬青木瓜沙拉", "description": "客家桔醬搭配泰式青木瓜沙拉，爽脆開胃"},
        {"name": "炒河粉", "description": "在地人最愛，五星口味平民價格"},
        {"name": "泰式打拋蔬食", "description": "泰式風味蔬食版打拋豬"}
    ], [
        {"name": "桔醬青木瓜サラダ", "description": "客家桔醬とタイ式青木瓜サラダ、シャキシャキ開胃"},
        {"name": "焼きビーフン", "description": "地元民に愛される、五星の味お手頃価格"},
        {"name": "タイ式打拋蔬食", "description": "タイ風味の野菜版打拝豬"}
    ]),
    
    # 34. Ad Astra - 台北 1014
    ("台北", 1014, [
        {"name": "Tasting Menu", "description": "米其林一星無菜單料理，北歐日式融合料理"},
        {"name": "無酒精調飲配搭", "description": "五杯無酒精調飲搭配套餐，星空之旅"},
        {"name": "吧台席", "description": "面對開放式廚房，看主廚料理過程"}
    ], [
        {"name": "テイスティングメニュー", "description": "ミシュラン一星おまかせ、北欧和風融合料理"},
        {"name": "ノンアルコールペアリング", "description": "5杯のノンアルペアリング、星空の旅"},
        {"name": "カウンター席", "description": "オープンキッチン正面、シェフの料理プロセスを見学"}
    ]),
    
    # 35. 百合素食 - 台中 353 - limited specific dish info
    # Skip
    
    # 36. DO-DO-WU Café 蔬食 - 高雄 283 - no specific dish info found for this restaurant
    # Skip
    
    # 37. 響叮噹素食 - 台中 336
    ("台中", 336, [
        {"name": "鐵板麵", "description": "招牌鐵板麵，店名特色料理"},
        {"name": "猴頭菇料理", "description": "特色猴頭菇料理，口感豐富"},
        {"name": "手工水餃", "description": "多種口味水餃，每日現包"}
    ], [
        {"name": "鉄板麺", "description": "看板鉄板麺、店名の特色料理"},
        {"name": "猴頭菇料理", "description": "特色猴頭菇料理、豊かな食感"},
        {"name": "手作水餃", "description": "多種口味の水餃子、毎日手作り"}
    ]),
    
    # 38. 五福軒純素共饗 - 雲林 78
    ("雲林", 78, [
        {"name": "純素異國料理", "description": "純素異國風味料理，藝術系美食"},
        {"name": "觀天之道套餐", "description": "招牌套餐，以純素食材呈現多國風味"},
        {"name": "純素甜點", "description": "無蛋奶的手作甜點"}
    ], [
        {"name": "純菜異国料理", "description": "純菜の異国風料理、アート系美食"},
        {"name": "観天之道セット", "description": "看板セット、純菜食材で多国風味を表現"},
        {"name": "純菜スイーツ", "description": "卵乳不使用の手作りデザート"}
    ]),
    
    # 39. 李好蛋餅 - 雲林 116 - no specific dish info found
    # Skip
    
    # 40. 熱浪小島 大里店 - 台中 323
    ("台中", 323, [
        {"name": "馬來鹹擂茶飯", "description": "招牌主食，酥脆炸菜圃搭配南洋風味擂茶飯"},
        {"name": "泰泰椰香麵", "description": "濃郁酸辣椰香湯頭的南洋麵食"},
        {"name": "南洋蔬食小菜", "description": "多款南洋風味蔬食小菜"}
    ], [
        {"name": "マレー塩擂茶飯", "description": "看板主食、サクサク揚菜圃と南洋風擂茶飯"},
        {"name": "タイ風ココナッツ麺", "description": "濃厚酸辣ココナッツスープの南洋麺"},
        {"name": "南洋蔬食サイドメニュー", "description": "多彩な南洋風味の野菜サイドメニュー"}
    ]),
    
    # 41. 一本蔬 - 高雄 252 - limited specific dish info
    # Skip
    
    # 42. 灘頭客家常菜 - 屏東 95
    ("屏東", 95, [
        {"name": "滷豬腳", "description": "招牌菜，肥而不膩入口即化"},
        {"name": "薑絲大腸", "description": "大腸處理乾淨，搭配酸辣薑絲醬汁"},
        {"name": "塔香斬雞", "description": "九層塔香氣的斬雞，嫩又甜"}
    ], [
        {"name": "滷豚足", "description": "看板料理、脂身がくどくなく口溶け"},
        {"name": "生姜大腸", "description": "大腸はきれいに処理、酸辣生姜ソース"},
        {"name": "塔香斬鶏", "description": "バジル香りの斬鶏、嫩で甘い"}
    ]),
    
    # 43. 橙義製研所 - 彰化 188
    ("彰化", 188, [
        {"name": "黃金田燒餅", "description": "招牌必買，外皮香酥奶香與微甜奶糖餡"},
        {"name": "鹽之花蛋黃酥", "description": "超強中秋伴手禮，鹹甜交織"},
        {"name": "可麗露", "description": "每日限量，外脆內軟的法式甜點"}
    ], [
        {"name": "黄金田焼餅", "description": "看板必買、外皮香ばしくミルク香と甘いキャラメル餡"},
        {"name": "塩の花蛋黄酥", "description": "極上中秋ギフト、甘塩バランス"},
        {"name": "カヌレ", "description": "毎日数量限定、外カリ中フワのフランス菓子"}
    ]),
    
    # 44. 老担菩提素食 - 南投 119
    ("南投", 119, [
        {"name": "南投意麵", "description": "推薦必吃，非油炸意麵口感獨特"},
        {"name": "水餃", "description": "皮Q內餡香，附配菜份量足"},
        {"name": "香菇芋頭", "description": "人氣菜品，一早就賣完"}
    ], [
        {"name": "南投意麺", "description": "おすすめ必食、油揚げではない独自の食感"},
        {"name": "水餃子", "description": "皮モチモチ餡香り、副菜付きボリューム満点"},
        {"name": "椎茸芋頭", "description": "人気メニュー、朝で売り切れ"}
    ]),
    
    # 45. 春祥茶庄 - 台中 301 - search returned 有春茶館 not 春祥茶庄
    # Skip - wrong restaurant matched
    
    # 46. 溪湖台北魷魚焿羊肉焿 - 彰化 185 - limited specific info
    # Skip
    
    # 47. 順發麵食館 - 台中 300 - limited specific info
    # Skip
    
    # 48. 我行我素 - 新北 275
    ("新北", 275, [
        {"name": "素肉骨茶", "description": "馬來西亞風味素食肉骨茶，香氣濃郁"},
        {"name": "咖哩湯飯", "description": "南洋風味咖哩搭配白飯，香料豐富"},
        {"name": "素沙嗲", "description": "東南亞風味素食沙嗲串烤"}
    ], [
        {"name": "菜肉骨茶", "description": "マレーシア風味の素食肉骨茶、香り豊か"},
        {"name": "カレースープご飯", "description": "南洋風カレーと白飯、スパイス豊か"},
        {"name": "菜サテ", "description": "東南アジア風の素食サテ串焼き"}
    ]),
    
    # 49. 微笑葉子早午餐 - 桃園 198
    ("桃園", 198, [
        {"name": "咖哩飯", "description": "招牌必點，份量不小別輕易挑戰"},
        {"name": "手工漢堡", "description": "每日現做漢堡，社區型早午餐人氣"},
        {"name": "脆皮蛋餅", "description": "外酥內軟的台式蛋餅"}
    ], [
        {"name": "カレーライス", "description": "看板メニュー、ボリューム満点で挑戦注意"},
        {"name": "手作バーガー", "description": "毎日手作りバーガー、社区型ブランチ人気"},
        {"name": "crispy蛋餅", "description": "外カリ中フワの台湾式卵餅"}
    ]),
    
    # 50. 魚弄 - 台南 267
    ("台南", 267, [
        {"name": "蓉城烤魚", "description": "源自四川成都的烤魚，有麻辣、青花椒、蒜香三種口味"},
        {"name": "老罈酸菜魚", "description": "正宗川味酸菜魚，酸辣平衡鮮味十足"},
        {"name": "水煮魚", "description": "川味水煮魚，麻辣鮮香"}
    ], [
        {"name": "蓉城焼き魚", "description": "四川成都発の焼き魚、麻辣・青花椒・蒜香の3種"},
        {"name": "老罈酸菜魚", "description": "本格四川風酸菜魚、酸辣バランス鮮味豊か"},
        {"name": "水煮魚", "description": "四川風水煮魚、麻辣鮮香"}
    ]),
]

# Apply updates
applied = 0
skipped = 0
for city, idx, dishes_zh, dishes_ja in updates:
    if city in data_zh and idx < len(data_zh[city]["food"]):
        data_zh[city]["food"][idx]["dishes"] = dishes_zh
        applied += 1
    else:
        print(f"WARNING: {city} index {idx} not found in data-zh.json")
        skipped += 1
    if city in data_ja and idx < len(data_ja[city]["food"]):
        data_ja[city]["food"][idx]["dishes"] = dishes_ja
    else:
        print(f"WARNING: {city} index {idx} not found in data-ja.json")

# Save both files
with open('data-zh.json', 'w', encoding='utf-8') as f:
    json.dump(data_zh, f, ensure_ascii=False, indent=2)
with open('data-ja.json', 'w', encoding='utf-8') as f:
    json.dump(data_ja, f, ensure_ascii=False, indent=2)

print(f"Done! Applied dishes to {applied} restaurants. Skipped {skipped}.")