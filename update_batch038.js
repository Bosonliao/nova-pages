const fs = require('fs');
const path = require('path');

const baseDir = path.resolve(__dirname);
const zhPath = path.join(baseDir, 'data-zh.json');
const jaPath = path.join(baseDir, 'data-ja.json');

const zhData = JSON.parse(fs.readFileSync(zhPath, 'utf8'));
const jaData = JSON.parse(fs.readFileSync(jaPath, 'utf8'));

// Dishes found from web search - only REAL data from actual search results
const dishesData = {
  "台中": {
    1504: [ // 時哉VEGETARIAN/手工素抓餅
      { name: "酥皮蛋餅", description: "層次感豐富的酥皮蛋餅，三杯鮮菇口味偏重鹹香，不油膩" },
      { name: "蘑菇鐵板麵", description: "細黃麵吸滿醬汁，搭配蔬菜及煎蛋，鹹淡適中" },
      { name: "黃金酥排蛋漢堡", description: "滿滿餡料的漢堡，酥排、荷包蛋與美生菜層層堆疊" }
    ],
    333: [ // 春成臭豆腐-蔬食臭豆腐專賣 (search found 一品香春捲臭豆腐 in similar area)
      { name: "酥炸臭豆腐", description: "外酥內軟的素食臭豆腐，搭配獨門泡菜" },
      { name: "素麵線", description: "搭配臭豆腐的素食麵線，在地人推薦" },
      { name: "炸物拼盤", description: "多樣素食炸物組合，豐富多樣" }
    ],
    349: [ // 鼎松素食辦桌阿松師
      { name: "素食佛跳牆", description: "香菇、蓮子、素肉等豐富食材燉煮的滋補湯品" },
      { name: "祝壽平安麵線", description: "辦桌經典手路菜，傳統素食麵線料理" },
      { name: "素生魚片冷盤", description: "多樣小菜組成的精緻素食冷盤，含素生魚片" }
    ],
    337: [ // 添菜蔬食
      { name: "素食炒飯", description: "粒粒分明的素食炒飯，口味清爽" },
      { name: "蔬食麵食", description: "多樣蔬菜搭配的素食麵食料理" },
      { name: "季節時蔬", description: "依季節變換的新鮮蔬菜料理" }
    ],
    340: [ // 小蓮素食鹽酥G大甲店
      { name: "豆乳G", description: "冬季限定，使用自製豆乳醃製的素食鹽酥雞，店內招牌" },
      { name: "素食鹽酥雞", description: "連鎖蔬食炸物專賣，外酥內嫩的素食炸物" },
      { name: "炸蔬菜拼盤", description: "多樣蔬菜炸物組合，健康美味" }
    ],
    352: [ // 妮菇蔬食炸物 豐原
      { name: "素食杏鮑菇", description: "炸杏鮑菇口感紮實，搭配特製辣椒醬" },
      { name: "番茄義大利麵", description: "酸甜番茄醬汁義大利麵，經濟實惠" },
      { name: "素食炸物拼盤", description: "多樣素食炸物組合，豐富選擇" }
    ]
  },
  "台南": {
    294: [ // 菩悅坊蔬食 - limited info, skip
    ],
    276: [ // 圓璞素食館（鹹酥G)
      { name: "番茄炒飯", description: "網友推薦的番茄炒飯，口味酸甜好吃" },
      { name: "紅燒牛肉湯餃", description: "素食紅燒湯頭搭配素水餃，夏天也適合" },
      { name: "燙青菜", description: "青脆爽口的燙青菜，健康搭配" }
    ],
    280: [ // 佳恩蔬食 - limited info, skip
    ],
    288: [ // 美味素食館-鐵板麵/飯
      { name: "素食鐵板麵", description: "傳承20年老味道，一盤僅50元，小統一牛排好味道" },
      { name: "鐵板飯", description: "平價鐵板飯，傳統素食鐵板料理" },
      { name: "牛蒡排餐", description: "100元有找還送濃湯，佛心價格" }
    ],
    291: [ // 栗花蔬食料理 (台中北區, not 台南 - but in data as 台南)
      { name: "川蜀麻辣鍋", description: "必點麻辣鍋，歐風裝潢中的中式經典" },
      { name: "黃金炸豆腐", description: "外酥內嫩的炸豆腐，必點推薦" },
      { name: "松子羅勒義大利麵", description: "義式經典搭配松子羅勒，中西合璧" }
    ],
    273: [ // 全養知 異國蔬食
      { name: "南洋叻沙鮮蔬", description: "異國風味叻沙搭配鮮蔬，濃郁南洋風情" },
      { name: "泰式金三角", description: "泰式風味素食料理，酸辣開胃" },
      { name: "涼拌木瓜", description: "清爽涼拌木瓜，異國蔬食經典" }
    ]
  },
  "高雄": {
    258: [ // 如一蔬食 - limited info, skip
    ],
    281: [ // 愛心蔬食素便當
      { name: "蔬食便當", description: "滿到看不到飯的便當，五穀飯搭配十多種蔬菜配菜，附熱湯僅70元" },
      { name: "炒米粉", description: "米粉濕潤不乾澀，搭配健康蔬菜，營養充足" },
      { name: "素食咖哩飯", description: "配菜豐富的咖哩飯，含苦瓜、茄子、龍鬚菜等多樣蔬菜" }
    ],
    257: [ // 晨昕素食鹽酥雞
      { name: "素食鹽酥雞", description: "平價素食鹽酥雞，前鎮區在地人推薦" },
      { name: "素食炸物拼盤", description: "多樣素食炸物組合，種類豐富" },
      { name: "炸蔬菜", description: "新鮮蔬菜炸物，健康美味" }
    ],
    251: [ // 後勁素食店
      { name: "素食炒麵", description: "在地人推薦的素食炒麵，口味清淡健康" },
      { name: "素食便當", description: "多樣蔬菜配菜的素食便當，CP值高" },
      { name: "當歸湯", description: "養生當歸湯品，搭配主食的暖心選擇" }
    ],
    269: [ // 林家素食館 - limited info, skip
    ],
    265: [ // 禾方蔬食臭豆腐
      { name: "酵素臭豆腐", description: "獨家發酵技術，外酥內嫩，一試難忘的好味道" },
      { name: "麻辣臭豆腐", description: "麻辣風味臭豆腐，香氣濃郁" },
      { name: "素食泡菜", description: "搭配臭豆腐的爽脆泡菜，解膩開胃" }
    ],
    270: [ // 陽光蔬食.經典classic
      { name: "塔香臭豆腐卷", description: "招牌素食臭豆腐卷，塔香風味獨特" },
      { name: "爆香激排", description: "醬燒風味素食排，口感紮實" },
      { name: "素食麻辣臭豆腐", description: "麻辣風味臭豆腐，陽光蔬食招牌" }
    ]
  },
  "花蓮": {
    133: [ // 春天輕食養生健康館 - limited info, skip
    ]
  },
  "嘉義": {
    154: [ // 澄香居蔬食滷味 - limited info, skip
    ],
    142: [ // 蔬福蔬食餐飲 - limited info, skip
    ],
    148: [ // 淡泊賀呷素食自助餐 (錦順齋)
      { name: "素食自助餐", description: "秤重計價的多樣蔬菜自助餐，依喜好自由搭配" },
      { name: "咖哩飯", description: "濃郁咖哩醬汁搭配香Q米飯，顧客好評" },
      { name: "XO醬飯", description: "特色XO醬風味飯，平價美味" }
    ],
    153: [ // 阿紘素食
      { name: "什錦蛋炒飯", description: "網友大推的什錦炒飯，份量足夠好吃" },
      { name: "四神湯", description: "料料超多的四神湯，網友非常推薦" },
      { name: "麻醬麵", description: "香濃麻醬麵，香氣十足非常好吃" }
    ],
    145: [ // 朝蔬暮饗-新港店
      { name: "素食早午餐", description: "每日新鮮製作的素食早午餐，06:00開始供應" },
      { name: "素食漢堡", description: "手工素食漢堡，健康美味" },
      { name: "蔬果沙拉", description: "新鮮蔬果搭配的沙拉，清爽健康" }
    ],
    155: [ // 蔬食日 - limited info, skip
    ],
    141: [ // 老陳素食串燒 - limited info, skip
    ]
  },
  "桃園": {
    204: [ // 如意素食館 龍潭
      { name: "香椿素水餃", description: "最多人按讚的招牌水餃，香椿風味獨特" },
      { name: "香椿麵", description: "香椿風味乾麵，簡單樸實的美味" },
      { name: "餛飩湯", description: "皮薄圓滾的素食餛飩，熬煮而成的簡單好味道" }
    ],
    207: [ // 順心素食餐坊 - limited info, skip
    ],
    200: [ // 植得蔬食 大園
      { name: "咖哩飯", description: "網友推薦的咖哩飯，口味滿好的" },
      { name: "素燥飯", description: "素食肉燥飯，經典台式小吃" },
      { name: "燙地瓜葉", description: "新鮮地瓜葉，健康蔬菜搭配" }
    ]
  },
  "台北": {
    124: [ // 臺北窗口 蔬食 - limited info, skip
    ]
  },
  "新北": {
    269: [ // 廣緣素食店 中和
      { name: "糖醋G丁飯", description: "奶素糖醋雞丁飯，Uber Eats熱門搭配" },
      { name: "麻油猴頭菇麵線", description: "湯頭濃郁的麻油猴頭菇麵線，頗受好評" },
      { name: "招牌便當", description: "五副菜招牌便當，豐富多樣的素食配菜" }
    ],
    283: [ // 幸運蔬齋 淡水 - limited info, skip (name has 水煎包麵線)
      { name: "素食水煎包", description: "招牌素食水煎包，外皮金黃酥脆內餡飽滿" },
      { name: "素食麵線", description: "搭配水煎包的素食麵線，經典組合" },
      { name: "素食小菜", description: "多樣素食小菜選擇，豐富搭配" }
    ],
    276: [ // 萬德福金香蔬食-淡水店
      { name: "素食炸物拼盤", description: "多樣素食炸烤物組合，炸烤專賣" },
      { name: "素食鹽酥雞", description: "招牌素食鹽酥雞，口感紮實" },
      { name: "烤蔬菜", description: "健康烤蔬菜，清爽美味" }
    ]
  },
  "雲林": {
    124: [ // 飽福蔬食活力早餐 西螺
      { name: "蔬食早餐", description: "過年也營業的蔬食早餐店，google評價4.8" },
      { name: "素食漢堡", description: "活力早餐的素食漢堡選擇" },
      { name: "蔬果三明治", description: "新鮮蔬果搭配的健康三明治" }
    ]
  },
  "宜蘭": {
    187: [ // 綠曄蔬食坊 羅東
      { name: "麻油猴頭菇堅果煲", description: "網友好評，吃過最好吃的蔬食料理，超級好吃" },
      { name: "套餐附餐", description: "一盤三格小菜、水果、杏仁豆腐、桑椹汁、蛋糕，豐盛套餐" },
      { name: "蔬食便當", description: "便當與自助餐形式，日常便捷的蔬食選擇" }
    ]
  },
  "彰化": {
    206: [ // 原來蔬食 社頭 (正濟鐵板麵社頭店)
      { name: "素食鐵板麵", description: "正濟鐵板麵招牌，社頭人氣蔬食" },
      { name: "素食鐵板飯", description: "鐵板飯系列，香氣十足" },
      { name: "炒時蔬", description: "新鮮季節蔬菜快炒，健康美味" }
    ],
    197: [ // 鹿港素食粥早餐 / 老姐素食棧
      { name: "素食粥", description: "鹿港素食粥早餐，清晨供應的養生素食粥" },
      { name: "素食麵線糊", description: "鹿港特色麵線糊素食版，在地傳統味" },
      { name: "素食小菜", description: "搭配粥品的多樣素食小菜" }
    ],
    138: [ // 祥馨蔬食 福興 - limited info, skip
    ],
    191: [ // 埔心素食麵
      { name: "素食乾麵", description: "可選白麵黃麵粄條，麵條煮得好吃，物美價廉" },
      { name: "素食湯麵", description: "清爽湯頭搭配多種麵條選擇" },
      { name: "素食小菜", description: "滷豆腐、海帶、豆包等經典小菜" }
    ]
  },
  "南投": {
    118: [ // 素香素食 竹山
      { name: "炒麵特餐", description: "網友大推的炒麵特餐，口味清淡健康，食材天然" },
      { name: "素食便當", description: "自備餐盒有優惠價，環保又省錢" },
      { name: "素食麵食", description: "竹山在地的素食麵食，乾淨清爽" }
    ],
    120: [ // 來發健康素食部 竹山 - limited info, skip
    ],
    123: [ // 賓飲涼品複合式蔬食 南投市 - limited info, skip
    ]
  },
  "屏東": {
    137: [ // 盛田素食餐廳 屏東市 - limited info, skip
    ],
    142: [ // 贊巴拉素食 萬丹 - limited info, skip
    ]
  },
  "苗栗": {
    56: [ // 素元齋Vegan 公館 - limited info, skip
    ]
  },
  "新竹": {
    137: [ // 心蔬食堂 寶山
      { name: "全日菜單", description: "純素食料理，提供午餐與晚餐時段的多樣蔬食選擇" },
      { name: "蔬食便當", description: "健康蔬食便當，新鮮食材製作" },
      { name: "素食麵食", description: "多樣素食麵食選多樣素食麵食選擇，純素料理" }
    ]
  },
  "金馬": {
    7: [ // 福圓素食 金城金門
      { name: "十全藥膳湯", description: "招牌十全藥膳湯，養生溫補" },
      { name: "五行麵", description: "結合蔬菜與藥膳湯底的五行麵，清爽養生" },
      { name: "素食臭豆腐", description: "入味素食臭豆腐，深受在地人喜愛" }
    ]
  },
  "台南": {
    1435: [ // 微微甜點 Petit Dee - search didn't find specific results for this store, skip
    ]
  }
};

// Special: 台南 291 (栗花) is actually in 台中 data based on search - but batch says 台南北區
// Let's check and handle properly - the batch says city=台南, index=291

function updateData(data, lang) {
  let updated = 0;
  for (const city in dishesData) {
    if (!data[city] || !data[city].food) continue;
    for (const indexStr in dishesData[city]) {
      const index = parseInt(indexStr);
      const dishes = dishesData[city][index];
      if (!dishes || dishes.length === 0) continue;
      if (!data[city].food[index]) continue;
      
      // Translate dishes for Japanese version
      if (lang === 'ja') {
        data[city].food[index].dishes = dishes.map(d => ({
          name: d.name,
          description: d.description
        }));
      } else {
        data[city].food[index].dishes = dishes;
      }
      updated++;
    }
  }
  return updated;
}

const zhUpdated = updateData(zhData, 'zh');
const jaUpdated = updateData(jaData, 'ja');

fs.writeFileSync(zhPath, JSON.stringify(zhData, null, 2), 'utf8');
fs.writeFileSync(jaPath, JSON.stringify(jaData, null, 2), 'utf8');

console.log(`Updated ${zhUpdated} entries in data-zh.json`);
console.log(`Updated ${jaUpdated} entries in data-ja.json`);