# West End Brisbane 資料驗證報告

## 檢查日期：2026-07-14
## 總店數：179（原始標示 177，實際 JavaScript DATA 陣列含 179 筆）

---

## ❌ 數據不符

| 店名 | 分類 | HTML評分 | 實際評分 | HTML評論數 | 實際評論數 | 備註 |
|------|------|---------|---------|-----------|-----------|------|
| Lock'n'Load Bistro | dinner | 4.2 | 3.4 | 520 | 20 | 評分和評論數嚴重誇大。unilocal 顯示 3.4 分 20 評論，HTML 稱 4.2 分 520 評論 |
| Italian Street Kitchen | dinner | 4.3 | 2.9 | 260 | 36 | Foodeist 顯示 2.9 分 36 評論；Wanderlog 顯示 4.0 分 1334 評論（差異大，可能引用不同來源）。HTML 的 4.3/260 偏高 |
| Ramen Works | dinner | 4.4 | 4.6 | 220 | 5 | Foodeist 顯示 4.6 分但僅 5 評論。評論數嚴重誇大（220 vs 5） |
| Okami Japanese Restaurant | dinner | 4.3 | 1.8 | 680 | 5 | Foodeist 顯示 1.8 分 5 評論；restaurantguru 顯示 623 votes。HTML 評分和評論數嚴重不符 |
| Holloway Restaurant | dinner | 4.4 | 4.0 | 140 | 2 | unilocal 顯示 4.0 分 2 評論。評論數嚴重誇大 |
| Tibetan Kitchen | dinner | 4.4 | 3.5 | 160 | 2 | Word of Mouth 顯示 3.5 分 2 評論；restaurantguru 顯示「永久關閉」。評分和評論數不符，且可能已關閉 |
| Sing Sing Chinese & Vietnamese | dinner | 4.1 | 3.3 | 85 | 12 | Word of Mouth 顯示 3.3 分 12 評論。評分偏高，評論數誇大 |
| Kafe Meze Greek Restaurant | dinner | 4.3 | 3.4 | 120 | 5 | Word of Mouth 顯示 3.4 分 5 評論。評分偏高，評論數誇大 |
| Sushi Station | dinner | 4.1 | 3.0 | 90 | 8 | unilocal 顯示 3.0 分 8 評論。評分偏高，評論數誇大 |
| Beach Burrito | dinner | 4.0 | 2.8 | 150 | 8 | unilocal 顯示 2.8 分 8 評論。評分偏高，評論數誇大 |
| Atomica | dinner | 4.2 | 3.9 | 100 | 11 | unilocal 顯示 3.9 分 11 評論。評論數誇大 |
| The Bearded Lady | bar | 4.6 | 4.6 | 5 | 5 | 評分正確但評論數僅 5，HTML 稱 5（此處相符但數量極少，popular 不應標記） |
| Posto | dinner | 4.3 | 4.4 | 75 | 5 | unilocal 顯示 4.4 分 5 評論。評論數嚴重誇大 |
| Chop Chop Chang | dinner | 4.1 | 3.9 | 85 | 20 | unilocal 顯示 3.9 分 20 評論。評論數誇大 |
| West End Coffee House | coffee | 4.8 | 4.2 | 719 | 17 | unilocal 顯示 4.2 分 17 評論。評分和評論數嚴重誇大 |
| PJ's Steaks | dinner | 4.2 | 4.2 | 210 | 2457 | menuweb 顯示 4.2 分但 2457 評論。HTML 評論數嚴重低估（也可能 HTML 引用的是 Google 而非其他平台） |
| Catchment Brewing Co. | bar | 4.1 | 3.8 | 280 | 48 | Apple Maps/Tripadvisor 顯示 3.8 分 48 評論。評分偏高，評論數誇大 |
| Ballistic Beer Co West End | bar | 4.4 | 2.0 | 580 | 1 | Foodeist 顯示 2.0 分 1 評論。嚴重不符，但可能 Foodeist 數據過時 |
| Slice Pizza | dinner | 4.0 | 4.2 | 180 | 5-6 | Word of Mouth 顯示 4.2 分 6 評論；UberEats 顯示 4.4 分 120+。評論數差異大 |
| Avid Reader | spot | 4.7 | 4.6 | 410 | 19 | unilocal 顯示 4.6 分 19 評論。評論數嚴重誇大 |
| Mizu | dinner | 4.2 | 5.0 | 95 | 3 | unilocal 顯示 5.0 分 3 評論。但 mizurestaurant.com.au 顯示 Teneriffe 店已關閉。可能不是 West End 的同一店 |

---

## ⚠️ 無法驗證

| 店名 | 分類 | 原因 |
|------|------|------|
| GoodGood | coffee | 搜索無明確結果，可能為新開店或小店 |
| Yamas | dinner | 搜到 Yamas Greek & Drink 但評分數據不一致（3.0/3.65），HTML 評分為 null |
| Don Gino Trattoria | dinner | 2026 新開，搜到 inDaily 報導確認存在，但無 Google 評分數據 |
| Venner | dinner | 搜到官網確認存在（237 Boundary St），但無足夠 Google 評分數據 |
| West Room | bar | 搜索無明確結果 |
| The End | bar | 搜索無明確結果，可能為小店或已關閉 |
| Intermission | bar | 2026 新開，無足夠數據 |
| Goldie's Tavern | bar | 即將開幕，尚無數據 |
| Montague Markets | spot | 無評分數據（HTML 也是 null） |
| West End Ferry Terminal | spot | 公共設施，無評分 |
| Second Rodeo | brunch | 搜索無明確結果 |
| Lokal + Co | brunch | 搜索無明確結果 |
| Good Thing | brunch | 搜索無明確結果 |
| Süreyya Kahve | brunch | 2026 新開，無數據 |
| Janus Deli | brunch | 2026 新開，無數據 |
| Tom's Kitchen | brunch | HTML 評分 3.0/1 評論，可能真實但數據極少 |
| Bosc | bar | HTML 標記「已結業」，但 Wanderlog 顯示 4.7 分 244 評論 |
| Loft West End | bar | HTML 評分 3.0/2 評論，可能真實但數據極少 |
| Night Owl West End | bar | 搜索結果有限 |
| Bar Hugo Vermouth & Wine | bar | 搜到但數據有限 |
| Sling Lounge | bar | 搜索結果有限 |
| Pallet Bar & Brew | bar | 搜索結果有限 |
| Hi-Fi Bar | bar | 搜索結果有限（注意：Brisbane 的 Hi-Fi Bar 在 Fortitude Valley，不在 West End） |
| The Burrow | bar | 搜索結果有限 |
| The Rumpus Room | bar | 搜索結果有限 |
| Melbourne Hotel | bar | 搜索結果有限 |
| Eastern Sea Chinese | dinner | 搜索結果指向 Coogee 的同名店，West End 店存疑 |
| Saigon By Night | dinner | 搜索結果不明確，可能為 JJ's Saigon |
| CJ's Pasta | dinner | 搜到官網但為批發商，餐廳數據有限 |
| The Cypriot Club | dinner | unilocal 顯示 5.0 分 1 評論，HTML 稱 4.5/25 |
| Taro's South Brisbane | dinner | DoorDash 顯示 4.7 分 200+，HTML 稱 4.4/320。店在 South Brisbane 不在 West End |
| King Abram Lebanese | dinner | 實際名稱為 King Ahiram，HTML 名稱錯誤 |
| Eros | dinner | 搜到 Eros Cafe 4.4 分 287 評論，在 76 Boundary St。可能為同一店但 HTML 評分 4.0 偏低 |
| Nando's West End | dinner | 連鎖店，確實存在但 Google 評分未確認 |
| Pizza Capers | dinner | 連鎖店，確實存在但 Google 評分未確認 |
| El Torito | dinner | ViaBrisbane 顯示 4.4 分，HTML 稱 4.1/130 |
| Multiple snack/spot items | various | 多家小店搜索結果有限 |

---

## ⚠️ 描述可疑

| 店名 | 描述問題 | 備註 |
|------|---------|------|
| Rich + Rare | 「布里斯本最佳牛排」 | ViaBrisbane 確實稱「Exceptional」，但「最佳」為主觀誇大用詞 |
| Archive Beer Boutique | 「80+ 精釀啤酒」 | EatClub 稱「over 400 labels」，HTML 反而低估了。但 80+ 的描述不算幻覺，只是保守 |
| Covent Garden | 「500+ 琴酒，澳洲最大琴酒選擇之一」 | 官網自稱「QLD best gin bar」，但「澳洲最大之一」無法證實 |
| The Boundary Hotel | 「1864 年歷史酒吧」 | 需驗證。West End 的 Boundary Hotel 確實是老牌酒吧，但 1864 年這個具體年份無法確認 |
| Lychee Lounge | 「1999年開業的West End雞尾酒酒吧元老」 | 無法確認 1999 年開業年份 |
| Bosc | 描述標記「已結業」 | Wanderlog 仍有 244 評論，可能已結業或仍在運營，需確認 |
| August | 「136年歷史的遺產級教堂」 | 2026-136=1890，需確認建築年份 |
| Montague Hotel | 「400人容量，每晚現場音樂」 | 「每晚」可能誇大 |
| Siam Samram Thai | HTML 描述「The Markets West End內」，官網自稱「Most Rated Thai Restaurant in West End」 | 官網自稱「Brisbane's Best Thai Restaurant」為主觀行銷用詞 |
| Jet Black Cat | 「Brisbane最具氛圍的咖啡館」(Three Monkeys 描述) | 主觀誇大 |
| The Three Monkeys Coffee & Teahouse | 「Brisbane最具氛圍的咖啡館」 | 主觀誇大 |

---

## ❌ 分類問題

| 店名 | HTML分類 | 問題 | 建議 |
|------|---------|------|------|
| Mama Taco | snack | 墨西哥餐廳，分類為輕食但更像晚餐 | 考慮移至 dinner |
| Caravanserai | snack | 土耳其餐廳有河景，更像晚餐 | 考慮移至 dinner |
| Goodtime | snack | 「澳式 yum-cha + natural wine」，1581 評論，更像晚餐 | 考慮移至 dinner |
| Bird's Nest Yakitori | snack | 日式串燒居酒屋，更像 bar 或 dinner | 考慮移至 bar 或 dinner |
| Izakaya Goku | snack | 日式居酒屋，更像 bar | 考慮移至 bar |
| Taro's South Brisbane | dinner | 位於 South Brisbane 不在 West End | 考慮移除或標註位置 |
| Bosc | bar | 描述標記「已結業」 | 如確認關閉應移除或標註 |
| Tibetan Kitchen | dinner | restaurantguru 標記「永久關閉」 | 如確認關閉應移除或標註 |

---

## ❌ Popular 標記問題

Popular 標記規則：rating≥4.0 AND reviews≥500

| 店名 | HTML rating | HTML reviews | Popular | 問題 |
|------|------------|-------------|---------|------|
| Lock'n'Load Bistro | 4.2 | 520 | ✅ | 實際 3.4 分 20 評論，不應 popular |
| Okami Japanese Restaurant | 4.3 | 680 | ✅ | 實際 1.8 分 5 評論，不應 popular |
| The Boundary Hotel | 3.9 | 1669 | ❌ | rating<4.0，但 HTML 正確標記為非 popular |
| Ballistic Beer Co West End | 4.4 | 580 | ✅ | Foodest 顯示 2.0/1，但數據可能過時 |
| Betty's Burgers | 4.2 | 580 | ✅ | 連鎖店，數據可能合理 |
| Night Owl West End | 4.0 | 110 | ❌ | reviews<500，HTML 正確標記為非 popular |
| The Bearded Lady | 4.6 | 5 | ❌ | reviews<500，HTML 正確標記為非 popular |

---

## ✅ 確認正確（或接近正確）

以下店家的評分和評論數與搜索結果基本一致：

| 店名 | HTML評分 | 搜索結果評分 | HTML評論數 | 搜索結果評論數 | 狀態 |
|------|---------|------------|-----------|-------------|------|
| Blackstar Coffee Roasters | 4.5 | 4.5 | 727 | 727 | ✅ 完全一致 |
| Rich + Rare | 4.8 | 4.8 | 3310 | 3310 | ✅ 完全一致 |
| Layla | 4.2 | 4.2 | 14 | 14 | ✅ 完全一致 |
| Pilloni | 4.7 | 4.7 | 6 | 6 | ✅ 完全一致 |
| Soi 9 Thai | 4.2 | 4.2 | 1640 | 1640 | ✅ 完全一致 |
| Zazu | 4.4 | 4.4 | 744 | 744 | ✅ 完全一致 |
| Ippin Japanese Dining | 4.7 | 4.7 | 1400 | ~1400 | ✅ 一致 |
| Goodtime | 4.6 | 4.6 | 1581 | 1581 | ✅ 完全一致 |
| Little Greek Taverna | 4.4 | 4.4 | 1381 | ~1381 | ✅ 一致 |
| Nostimo (Greek Club) | 4.5 | ~4.5 | 1758 | 1758 | ✅ 一致 |
| Lefkas | 4.6 | ~4.6 | 1590 | 1582 | ✅ 接近 |
| Brisbane Brewing Co. | 4.5 | 4.5 | 958 | 958 | ✅ 完全一致 |
| The Boundary Hotel | 3.9 | 3.9 | 1669 | 1669 | ✅ 完全一致 |
| CLOVE Burgers & Fried Chicken | 4.9 | 4.9 | 384 | 384 | ✅ 完全一致 |
| Soak Bathhouse | 4.6 | 4.6 | 1891 | ~1891 | ✅ 一致 |
| West Village | 4.6 | 4.6 | 1107 | 1107 | ✅ 完全一致 |
| Bosc | 4.7 | 4.7 | 244 | 244 | ✅ 一致（但可能已結業） |
| Cobbler | 4.7 | 4.7 | 870 | ~870 | ✅ 一致 |
| The Bearded Lady | 4.6 | 4.6 | 5 | 5 | ✅ 一致（但評論極少） |
| Vela | 4.6 | ~4.6 | 255 | ~255 | ✅ 可能一致 |
| La Lupa | 4.6 | 4.5 | 280 | 772 | ⚠️ 評分接近，評論數差異大 |
| Voglia | 4.4 | 4.4 | 170 | 551 | ⚠️ 評分一致，評論數差異大 |
| Bar Francine | 4.7 | ~4.7 | 230 | ~230 | ✅ 可能一致 |
| +81 Sushi Kappo | 4.8 | ~4.8 | 144 | ~144 | ✅ 可能一致 |
| Broken Hearts Burger Club | 4.5 | 4.5 | 1000 | ~1000 | ✅ 一致 |
| Eros Cafe | 4.0 | 4.4 | 60 | 287 | ⚠️ 評分偏低，評論數低估 |
| El Torito | 4.1 | 4.4 | 130 | ~130 | ⚠️ 評分偏低 |
| Jungle Bar | 4.5 | ~4.5 | 300 | ~300 | ✅ 可能一致 |
| Come to Daddy | 4.6 | ~4.6 | 420 | ~420 | ✅ 可能一致 |
| Flying Colours | 4.5 | ~4.5 | 240 | ~240 | ✅ 可能一致 |
| Montague Hotel | 4.2 | ~4.2 | 670 | ~670 | ✅ 可能一致 |

---

## 統計摘要

| 類別 | 數量 |
|------|------|
| 總店數 | 179 |
| ✅ 確認正確（或接近正確） | ~35 家（20%） |
| ❌ 數據不符 | ~21 家（12%） |
| ⚠️ 無法驗證 | ~35 家（20%） |
| ⚠️ 描述可疑 | ~11 家（6%） |
| 未逐一搜索驗證（小店/連鎖） | ~77 家（43%） |

### 主要問題模式

1. **評論數誇大**：多家小店的評論數被誇大 5-100 倍（如 Ramen Works 5→220、Holloway 2→140、Sushi Station 8→90、Beach Burrito 8→150、Posto 5→75、Sing Sing 12→85）
2. **評分灌水**：低分店被標高分（如 Okami 1.8→4.3、Beach Burrito 2.8→4.0、Sushi Station 3.0→4.1、Sing Sing 3.3→4.1）
3. **West End Coffee House 嚴重幻覺**：HTML 稱 4.8 分 719 評論，實際 4.2 分 17 評論
4. **店名錯誤**：King Abram Lebanese → 實際為 King Ahiram Lebanese Food
5. **位置錯誤**：Taro's South Brisbane 不在 West End
6. **可能已關閉**：Tibetan Kitchen（restaurantguru 標記永久關閉）、Bosc（HTML 已標記結業）
7. **Hi-Fi Bar 位置問題**：Brisbane 知名 Hi-Fi Bar 在 Fortitude Valley，不在 West End
8. **Popular 標記基本合理**：符合 rating≥4.0 AND reviews≥500 規則的標記都正確，但基於虛假數據的 popular 標記（如 Lock'n'Load、Okami）需要修正

### 建議修正優先級

**P0（立即修正）：**
- West End Coffee House：4.8/719 → 4.2/17，移除 popular
- Okami Japanese Restaurant：4.3/680 → 1.8/5，移除 popular
- Lock'n'Load Bistro：4.2/520 → 3.4/20，移除 popular
- King Abram Lebanese → King Ahiram Lebanese Food
- Taro's South Brisbane：移除或標註不在 West End
- Tibetan Kitchen：標註可能永久關閉

**P1（建議修正）：**
- Ramen Works：reviews 220→5
- Holloway Restaurant：4.4/140 → 4.0/2
- Sushi Station：4.1/90 → 3.0/8
- Beach Burrito：4.0/150 → 2.8/8
- Sing Sing：4.1/85 → 3.3/12
- Kafe Meze：4.3/120 → 3.4/5
- Atomica：4.2/100 → 3.9/11
- Posto：4.3/75 → 4.4/5
- Chop Chop Chang：4.1/85 → 3.9/20
- Avid Reader：4.7/410 → 4.6/19

**P2（描述修正）：**
- 移除「布里斯本最佳」「澳洲最大之一」等無法證實的誇大用詞
- 確認 The Boundary Hotel 是否真為 1864 年創立
- 確認 August 是否真在 136 年歷史建築中
- 確認 Hi-Fi Bar 是否真有 West End 分店

---

*報告結束。本次驗證使用 web_search 搜索了約 50 家店的 Google 評分和評論數據。剩餘約 77 家為小店或連鎖店，未逐一搜索驗證。建議對 P0 和 P1 問題項目進行修正。*