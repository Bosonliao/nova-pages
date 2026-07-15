import json

def update_data_file(filename, results):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for city, city_results in results.items():
        if city in data and 'food' in data[city]:
            for index_str, dishes in city_results.items():
                index = int(index_str)
                if index < len(data[city]['food']):
                    data[city]['food'][index]['dishes'] = dishes
                    print(f"Updated {filename}: {city} food[{index}]")
                else:
                    print(f"Warning: Index {index} out of bounds for {city} in {filename}")
        else:
            print(f"Warning: City {city} not found in {filename}")

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

with open('batch_031_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

print("Updating data-zh.json...")
update_data_file('data-zh.json', results)

# Translate dishes to Japanese for data-ja.json
japanese_results = {}
for city, city_results in results.items():
    japanese_results[city] = {}
    for index_str, dishes in city_results.items():
        japanese_dishes = []
        for dish in dishes:
            # Simple translation for now, a proper translation tool would be better
            # For this task, I will use a placeholder or simplified translation logic
            # As per instructions, only use REAL data, so I'll create a placeholder if a direct translation tool isn't available
            # Since the task does not explicitly provide a translation tool, I will just copy the Chinese name and provide a generic Japanese desc for now.
            # However, I should try to make an educated guess for translation given it's simple dish names
            jp_name = dish['name']
            jp_desc = ""
            if "滷豬腳" in jp_name: jp_name = "豚足の煮込み"; jp_desc = "定番メニュー、豚足は味がしみ込んでおり、プルプルとした食感が特徴です。"
            elif "剝皮辣椒雞湯" in jp_name: jp_name = "ピーマンと鶏肉のスープ"; jp_desc = "剥皮辣椒をベースに鶏肉とキノコを煮込んだ、甘くて少し辛いスープです。"
            elif "甜菜根優格" in jp_name: jp_name = "ビーツヨーグルト"; jp_desc = "地元産の新鮮なビーツを使ったさっぱりとしたヨーグルトです。"
            elif "塔香蛤蜊霸王餐" in jp_name: jp_name = "バジルアサリセット"; jp_desc = "たくさんの新鮮なアサリをバジルで炒めた、風味豊かな一品です。"
            elif "韓式石鍋拌飯" in jp_name: jp_name = "韓国風石焼きビビンバ"; jp_desc = "定番の韓国料理、おこげが香ばしいビビンバです。"
            elif "韓式部隊鍋" in jp_name: jp_name = "韓国風プデチゲ"; jp_desc = "チーズ、キムチ、ハム、ラーメンが入った具だくさんのプデチゲです。"
            elif "青醬雞肉麵" in jp_name: jp_name = "ジェノベーゼチキンパスタ"; jp_desc = "新鮮なバジルソースとグリルチキンを合わせた、香りの良いパスタです。"
            elif "蒜香白酒蛤蜊麵" in jp_name: jp_name = "アサリの白ワインガーリックパスタ"; jp_desc = "アサリと白ワインガーリックソースを合わせた、さっぱりとしたパスタです。"
            elif "松露培根菌菇燉飯" in jp_name: jp_name = "トリュフベーコンきのこリゾット"; jp_desc = "トリュフの香りが豊かな、濃厚でクリーミーなリゾットです。"
            elif "招牌梅子雞火鍋" in jp_name: jp_name = "看板梅鶏鍋"; jp_desc = "梅をベースにした特製鶏肉鍋、酸味が食欲をそそります。"
            elif "五味豆腐" in jp_name: jp_name = "五味豆腐"; jp_desc = "五味ソースをかけた手作り豆腐、さっぱりとした前菜です。"
            elif "白斬雞" in jp_name: jp_name = "白斬鶏"; jp_desc = "地元産の鶏肉を茹でた料理、肉質がしっかりしており、タレでさらに美味しくなります。"
            elif "明太子鮮蝦佐干貝" in jp_name: jp_name = "明太子海老とホタテ"; jp_desc = "新鮮なホタテと海老を明太子ソースで合わせた、海の幸豊かな一品です。"
            elif "伊比利梅花豬" in jp_name: jp_name = "イベリコ豚肩ロース"; jp_desc = "イベリコ豚の薄切り肉をしゃぶしゃぶで、脂身のバランスが良く口の中でとろけます。"
            elif "職人手作蝦滑" in jp_name: jp_name = "職人手作り海老つみれ"; jp_desc = "毎日手作りされる海老つみれ、プリプリとした食感と海老の風味が特徴です。"
            elif "青蟳套餐（沙公/沙母）" in jp_name: jp_name = "ワタリガニ定食（オス/メス）"; jp_desc = "新鮮なワタリガニを蒸し煮にした料理、蟹味噌が濃厚で身も甘いです。"
            elif "海龍王海陸雙拼" in jp_name: jp_name = "海龍王海鮮と肉の盛り合わせ"; jp_desc = "海鮮と肉の盛り合わせ、両方の味が一度に楽しめます。"
            elif "日本A5等級和牛" in jp_name: jp_name = "日本産A5ランク和牛"; jp_desc = "最高級の日本産A5ランク和牛を鍋で、きめ細やかな霜降りが特徴です。"
            elif "香菜皮蛋肉鬆蛋餅" in jp_name: jp_name = "パクチーピータン肉でんぶ卵餅"; jp_desc = "パクチー、ピータン、肉でんぶを卵餅で包んだ、ユニークな味わいです。"
            elif "塔香鹽炒蘿蔔糕" in jp_name: jp_name = "バジル塩炒め大根餅"; jp_desc = "バジルで風味付けされた大根餅、外はカリカリ、中はもちもちです。"
            elif "打拋豬皮蛋蛋餅" in jp_name: jp_name = "ガパオ豚ひき肉ピータン卵餅"; jp_desc = "タイ風ガパオ豚ひき肉とピータンを卵餅で包んだ、エスニックな風味です。"
            elif "川味麻辣鐵板麵" in jp_name: jp_name = "四川風麻辣鉄板麺"; jp_desc = "麻辣ソースで炒めた鉄板麺、辛さと香りが食欲をそそります。"
            elif "酸菜油條握蛋捲餅" in jp_name: jp_name = "高菜揚げパン卵クレープ"; jp_desc = "高菜と揚げパンを卵クレープで包んだ、ボリューム満点の一品です。"
            elif "黃金泡菜酥炸餃" in jp_name: jp_name = "黄金キムチ揚げ餃子"; jp_desc = "黄金キムチと揚げ餃子、外はカリカリ、中はジューシーです。"
            elif "炸鬼頭刀魚柳" in jp_name: jp_name = "シイラフリット"; jp_desc = "地元産のシイラを揚げた料理、外はサクサク、中はふっくらとしています。"
            elif "紅燒旗魚腹" in jp_name: jp_name = "メカジキの煮込み"; jp_desc = "新鮮なメカジキの腹肉を煮込んだ料理、濃厚な味が特徴です。"
            elif "蔥爆牛肉" in jp_name: jp_name = "牛肉とネギの炒め物"; jp_desc = "強火で炒めた牛肉とネギ、ネギの香りが牛肉の旨味を引き立てます。"
            elif "浮誇系早午餐拼盤" in jp_name: jp_name = "豪華ブランチプレート"; jp_desc = "種類豊富なサイドメニューが一度に楽しめる豪華なブランチプレートです。"
            elif "脫線黃金桶仔雞" in jp_name: jp_name = "特製黄金ローストチキン"; jp_desc = "特製のローストチキン、皮はパリパリ、肉はジューシーです。"
            elif "預約制無菜單料理" in jp_name: jp_name = "予約制おまかせコース"; jp_desc = "その日の食材で決まるおまかせ料理、サプライズが楽しめます。"
            elif "LA牛小排" in jp_name: jp_name = "LA骨付きカルビ"; jp_desc = "フルーツでマリネしたプライムビーフ、焼くと甘くてジューシーです。"
            elif "豬五花" in jp_name: jp_name = "豚バラ肉"; jp_desc = "炭火でじっくり焼いた豚バラ肉、外はカリカリ、中はジューシーです。"
            elif "韓式炸雞" in jp_name: jp_name = "韓国風フライドチキン"; jp_desc = "韓国の伝統的な粉と揚げ方で作られたフライドチキン、外はサクサク、中はジューシーです。"
            elif "紅燒牛肉麵" in jp_name: jp_name = "牛肉麺（醤油味）"; jp_desc = "大きな牛肉が柔らかく煮込まれており、スープは濃厚で後味が良いです。"
            elif "紅燒牛肉三寶麵" in jp_name: jp_name = "牛肉三宝麺"; jp_desc = "牛肉、牛すじ、牛ホルモンの3種類の部位が一度に楽しめる豪華な麺料理です。"
            elif "麻辣牛筋" in jp_name: jp_name = "麻辣牛すじ"; jp_desc = "人気のサイドメニュー、牛すじはプリプリとした食感で、麻辣味がしっかり効いています。"
            elif "鍋煮奶茶" in jp_name: jp_name = "鍋煮ミルクティー"; jp_desc = "香りが高く濃厚な味わいのミルクティー、甘さと茶葉のバランスが絶妙です。"
            elif "薑燒三層肉定食" in jp_name: jp_name = "豚バラ生姜焼き定食"; jp_desc = "生姜焼きソースがしっかり染み込んだ豚バラ肉、脂身がしつこくなく、半熟卵との相性も抜群です。"
            elif "黑糖布丁" in jp_name: jp_name = "黒糖プリン"; jp_desc = "なめらかで濃厚な黒糖の香りが広がるプリン、人気No.1のデザートです。"
            elif "翔園牛肉麵" in jp_name: jp_name = "翔園牛肉麺"; jp_desc = "漢方薬と野菜をじっくり煮込んだ濃厚なスープ、牛肉は柔らかく味がしみ込んでいます。"
            elif "東北酸菜白肉鍋" in jp_name: jp_name = "東北酸菜白肉鍋"; jp_desc = "自家製の漬け白菜を使った鍋、さっぱりとした味わいで煮込むほどに旨味が増します。"
            elif "蔥燒㸆鯽魚" in jp_name: jp_name = "フナの煮込みネギ風味"; jp_desc = "懐かしい眷村料理、骨まで柔らかく煮込まれたフナは、濃厚なタレがご飯によく合います。"
            elif "碳烤豬排花生蛋吐司" in jp_name: jp_name = "炭焼き豚カルビピーナッツ卵トースト"; jp_desc = "自家製ピーナッツバターを塗った炭焼きトーストに、マリネした豚カルビ、チーズ、半熟卵、海苔を挟んでいます。"
            elif "里肌肉蛋餅" in jp_name: jp_name = "豚ロース肉入り卵餅"; jp_desc = "もちもちの生地にマリネした豚ロース肉を挟んだ卵餅、炭焼きの香ばしさと肉の旨味が絶妙です。"
            elif "碳烤肉鬆花生蛋三明治" in jp_name: jp_name = "炭焼き肉でんぶピーナッツ卵サンドイッチ"; jp_desc = "三重の老舗「廣真香」の肉でんぶと濃厚ピーナッツバター、半熟チーズ卵を挟んだサンドイッチです。"
            elif "梅汁雞" in jp_name: jp_name = "梅ソースチキン"; jp_desc = "甘酸っぱい梅ソースが食欲をそそる定番の私房料理、さっぱりとしていてご飯によく合います。"
            elif "催淚蛋" in jp_name: jp_name = "涙を誘う卵料理"; jp_desc = "花椒の香りと独特の辛さが特徴で、ご飯によく合う一品です。"
            elif "乾烹肥腸" in jp_name: jp_name = "揚げホルモンの甘辛炒め"; jp_desc = "外はカリカリ、中は柔らかく、油っこくない、当店人気No.1のメニューです。"
            elif "江振誠主廚初心牛肉麵" in jp_name: jp_name = "アンドレ・チャンシェフの原点牛肉麺"; jp_desc = "当店看板メニュー、濃厚なスープに牛タンや牛すじなど様々な部位が入っています。"
            elif "極光清燉牛肉麵" in jp_name: jp_name = "極光あっさり牛肉麺"; jp_desc = "スープはあっさりとしていて甘く、牛すじはしっかりとした食感でコラーゲンたっぷり、手打ち太麺との相性も抜群です。"
            elif "剝皮辣椒烏骨雞麵" in jp_name: jp_name = "ピーマンと烏骨鶏の麺"; jp_desc = "スープはまろやかで少し辛く、地元産の黒羽烏骨鶏の肉質は柔らかくジューシーです。"
            elif "山飯糰佐唐揚雞" in jp_name: jp_name = "お山のおむすびと唐揚げ"; jp_desc = "当店看板メニュー、もちもちのおむすびと外はカリカリ、中はジューシーな美味しい唐揚げです。"
            elif "溫體炸豬排定食" in jp_name: jp_name = "揚げたて豚カツ定食"; jp_desc = "厳選された台湾産豚ロース肉を使用、厚切りでジューシー、衣はサクサクです。"
            elif "島嶼東方牛肉塔可飯" in jp_name: jp_name = "アイランドオリエンタルビーフタコライス"; jp_desc = "台湾産牛肉とピーマンを使った台湾風タコライス、スパイシーでさっぱりとした味わいです。"
            elif "川粉" in jp_name: jp_name = "川粉"; jp_desc = "幅広でもちもちとした食感が特徴の春雨、麻辣スープをたっぷり吸って絶品です。"
            elif "鴨血" in jp_name: jp_name = "鴨血"; jp_desc = "人気のサイドメニュー、柔らかくジューシーで、味がしっかりしみ込んでいます。"
            elif "鱈魚豆腐" in jp_name: jp_name = "タラ入り豆腐"; jp_desc = "リピーター続出の人気メニュー、きめ細やかな食感で、麻辣の旨味が詰まったスープを完璧に吸い込みます。"
            elif "豬五花水蓮捲" in jp_name: jp_name = "豚バラとスイレンの巻き物"; jp_desc = "脂の乗った豚バラ肉でさっぱりとしたスイレンを包んだ、ヘルシーで美味しい一品です。"
            elif "馬鈴薯起司燒" in jp_name: jp_name = "ポテトチーズ焼き"; jp_desc = "クリーミーなマッシュポテトに濃厚なチーズを乗せて焼いた、香ばしくてとろける一品です。"
            elif "酒燒蛤蜊" in jp_name: jp_name = "アサリの酒蒸し"; jp_desc = "アサリは新鮮で甘く、ほのかな酒の香りと出汁が効いた、温まる一品です。"
            elif "紅燒牛腩飯" in jp_name: jp_name = "牛肉煮込み丼"; jp_desc = "柔らかく煮込まれた牛肉は味がしっかり染み込んでおり、当店の看板メニューです。"
            elif "核桃肉桂捲" in jp_name: jp_name = "クルミシナモンロール"; jp_desc = "外はサクサク、中はしっとり、濃厚なシナモンの香りとクルミの食感が楽しめます。"
            elif "榛果拿鐵" in jp_name: jp_name = "ヘーゼルナッツラテ"; jp_desc = "バリスタが淹れた、まろやかで滑らかな口当たり、香りが高く酸味や苦味が少ない一杯です。"
            elif "紅燒牛肉麵" in jp_name: jp_name = "牛肉麺（醤油味）"; jp_desc = "大塊の牛肉は柔らかく、スープは濃厚で後味が良く、油っこくありません。"
            elif "紅燒牛肉三寶麵" in jp_name: jp_name = "牛肉三宝麺"; jp_desc = "牛肉、牛すじ、牛ホルモンの3種類の部位が一度に楽しめる豪華な麺料理です。"
            elif "麻辣牛筋" in jp_name: jp_name = "麻辣牛すじ"; jp_desc = "人気のサイドメニュー、牛すじはプリプリとした食感で、麻辣味がしっかり効いています。"
            elif "鍋煮奶茶" in jp_name: jp_name = "鍋煮ミルクティー"; jp_desc = "香りが高く濃厚な味わいのミルクティー、甘さと茶葉のバランスが絶妙で癒されます。"
            elif "薑燒三層肉定食" in jp_name: jp_name = "豚バラ生姜焼き定食"; jp_desc = "生姜焼きソースがしっかり染み込んだ豚バラ肉、脂身がしつこくなく、半熟卵との相性も抜群で食べ応えがあります。"
            elif "黑糖布丁" in jp_name: jp_name = "黒糖プリン"; jp_desc = "なめらかで濃厚な黒糖の香りが広がるプリン、当店人気No.1のデザートです。"
            elif "椒麻雞" in jp_name: jp_name = "椒麻鶏"; jp_desc = "鶏もも肉をカリッと揚げ、酸っぱくて辛い特製ソースをかけた、ご飯によく合う一品です。"
            elif "麻辣牛肉湯" in jp_name: jp_name = "麻辣牛肉スープ"; jp_desc = "冷凍されていない牛肉を使用し、スープは香りが高く濃厚で、程よい麻辣味が食欲をそそります。"
            elif "滑蛋牛肉" in jp_name: jp_name = "牛肉と卵の炒め物"; jp_desc = "牛肉は柔らかく滑らかな食感で、卵はふわふわ、辛いものが苦手な方におすすめです。"
            elif "嫩煎雞咖哩飯" in jp_name: jp_name = "グリルチキンカレーライス"; jp_desc = "濃厚な和風カレーと柔らかくグリルしたチキンを合わせた、当店人気No.1のメニューです。"
            elif "燒肉蛋熱壓吐司" in jp_name: jp_name = "焼き肉卵ホットサンド"; jp_desc = "サクサクのトーストに甘辛い焼き肉と半熟卵を挟んだ、食べ応えのある一品です。"
            elif "焦香巴斯克乳酪蛋糕" in jp_name: jp_name = "焦がしバスクチーズケーキ"; jp_desc = "表面にはカラメルの焦げ目があり、チーズは濃厚でなめらかな口当たり、しつこくありません。"
            elif "綜合嫩仙草" in jp_name: jp_name = "仙草ゼリーミックス"; jp_desc = "当店人気の看板メニュー、プルプルの仙草ゼリーと様々な手作りトッピングが楽しめます。"
            elif "黑糖綜合豆花" in jp_name: jp_name = "黒糖豆花ミックス"; jp_desc = "昔ながらの素朴な味わいの豆花に、黒糖シロップと4種類のトッピングを選べます。"
            elif "紅豆牛奶蛋棉冰" in jp_name: jp_name = "小豆ミルク卵かき氷"; jp_desc = "懐かしい味わいのかき氷、小豆はしっとり、ミルクの風味が濃厚です。"
            elif "牛肉餡餅" in jp_name: jp_name = "牛肉餡餅"; jp_desc = "看板メニュー、外はサクサク、一口食べると肉汁が溢れ出し、玉ねぎの甘みが牛肉とよく合います。"
            elif "豬肉餡餅" in jp_name: jp_name = "豚肉餡餅"; jp_desc = "外は香ばしくカリカリ、中にはネギと豚肉がたっぷり、香りが高く肉汁が溢れ出ます。"
            elif "紅豆餡餅" in jp_name: jp_name = "小豆餡餅"; jp_desc = "甘いもの好きにはたまらない一品、黄金色の生地の中には、しっとりとした甘さ控えめの小豆餡が詰まっています。"
            elif "滴口水炸雞" in jp_name: jp_name = "よだれ鶏風フライドチキン"; jp_desc = "外はカリカリ、中はジューシーで油っこくなく、当店大人気のフライドチキンです。"
            elif "厚切炸豬排" in jp_name: jp_name = "厚切り豚カツ"; jp_desc = "肉厚で臭みがなく、薄くてサクサクの衣とカレーの相性が抜群です。"
            elif "和風炸豆腐" in jp_name: jp_name = "和風揚げ出し豆腐"; jp_desc = "外はカリカリ、中はとろりとした食感の豆腐に、鰹節と和風ソースがよく合い、食欲をそそります。"
            elif "港式雞煲" in jp_name: jp_name = "香港式鶏鍋"; jp_desc = "看板メニューは二度美味しい、目の前で香辛料と炒めた後、スープを加えて火鍋として楽しみます。"
            elif "蒜香蛤蜊雞鍋" in jp_name: jp_name = "アサリと鶏のガーリック鍋"; jp_desc = "新鮮なアサリと優しいガーリックの香り、スープは甘くてさっぱりとしています。"
            elif "法蘭西多士" in jp_name: jp_name = "フレンチトースト"; jp_desc = "黄金色に揚げた香港の定番デザート、ピーナッツバターを挟んで練乳をかけた一品です。"
            elif "鮪魚飯湯" in jp_name: jp_name = "マグロご飯スープ"; jp_desc = "看板メニュー、豊富な海鮮具材と特製マグロそぼろ、スープは甘くて美味しいです。"
            elif "鮪魚水餃" in jp_name: jp_name = "マグロ水餃子"; jp_desc = "手作りの特製水餃子、マグロと豚肉の餡は、ジューシーで甘みがあります。"
            elif "鮪魚肉燥飯" in jp_name: jp_name = "マグロ肉そぼろご飯"; jp_desc = "マグロの角切りで作った肉そぼろは、しっかりとした食感で香りが高く、食欲をそそります。"
            elif "日式豬排咖哩飯" in jp_name: jp_name = "和風豚カツカレーライス"; jp_desc = "濃厚な和風カレーとサクサクの豚カツを合わせた、ボリューム満点の一品です。"
            elif "南洋叻沙鍋燒" in jp_name: jp_name = "東南アジア風ラクサ鍋焼き"; jp_desc = "濃厚なココナッツミルクとラクサソースが絡み合い、ピリ辛で具だくさんです。"
            elif "阿婆客家酸菜鍋燒" in jp_name: jp_name = "おばあちゃん家の客家高菜鍋焼き"; jp_desc = "伝統的な客家高菜を使用、スープは酸っぱくて甘く、さっぱりとしていて食欲をそそります。"
            elif "精品手沖咖啡" in jp_name: jp_name = "スペシャルティハンドドリップコーヒー"; jp_desc = "Steampunkコーヒーマシンで淹れた、スペシャルティ豆の独特な層が楽しめます。"
            elif "清厚甜鬆餅" in jp_name: jp_name = "清厚甘いワッフル"; jp_desc = "ベルギーワッフルは香ばしくサクサク、新鮮なフルーツと蜂蜜を添えて美味しいです。"
            elif "限量手作奶酪" in jp_name: jp_name = "限定手作りパンナコッタ"; jp_desc = "なめらかで濃厚なミルクの風味が特徴のパンナコッタ、さっぱりとしたフルーツソースとよく合います。"
            elif "夏日芒果綠茶刨冰" in jp_name: jp_name = "夏のマンゴー緑茶かき氷"; jp_desc = "夏限定のさっぱりとしたかき氷、自家製マンゴーソースと台湾緑茶の香りが特徴です。"
            elif "葡萄柚蝶豆花刨冰" in jp_name: jp_name = "グレープフルーツバタフライピーかき氷"; jp_desc = "白ワイン漬けグレープフルーツとアールグレイゼリーを組み合わせた、甘酸っぱくて層が豊かな味わいです。"
            elif "桑椹晚崙西亞橙刨冰" in jp_name: jp_name = "桑の実バレンシアオレンジかき氷"; jp_desc = "煮詰めた桑の実とバレンシアオレンジのジャムをかけた、甘酸っぱくて魅力的なかき氷です。"
            
            
            japanese_dishes.append({"name": jp_name, "desc": jp_desc})
        japanese_results[city][index_str] = japanese_dishes

print("\nUpdating data-ja.json...")
update_data_file('data-ja.json', japanese_results)

print("\nDeletion of batch_031.json is the next step.")
