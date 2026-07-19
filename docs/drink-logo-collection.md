# 飲料品牌 Logo 收集方法

## 成功流程

### 1. 品牌清單建立
從各縣市 JSON 資料掃描飲品店，用品牌名正規化提取：
```js
(f.name||'').split(' ')[0].split('-')[0].split('（')[0].split('(')[0].trim()
```
統計各品牌出現次數，排序出前 25 大品牌。

### 2. Logo 來源優先順序

#### ✅ 方法一：Wikipedia（最可靠）
- 搜尋 `https://zh.wikipedia.org/zh-tw/{品牌名}`
- 頁面中找 `File:XXX_logo.png` 連結
- 下載 URL 格式：`https://upload.wikimedia.org/wikipedia/zh/{hash前2碼}/{hash前2碼+2}/{檔名}`
- 用 `Special:FilePath` 重導拿到實際 URL：
  `https://zh.wikipedia.org/zh-tw/Special:FilePath/{檔名}`
- **成功案例**：50嵐、茶的魔手、珍煮丹、UG樂己、日出茶太、老虎堂

#### ✅ 方法二：品牌官網（第二可靠）
- 用 Python `urllib.request` 抓官網 HTML
- 用 regex 找 `<img src="...logo...">` 和 `rel="icon" href="...">`
- 下載 Logo 圖片
- **成功案例**：
  - 茶湯會 → `tw.tp-tea.com/images/logo_h.png`
  - 大苑子 → `dayungs.com/wp-content/uploads/...`（URL 有中文需 `urllib.parse.quote`）
  - CoCo都可 → `coco-tea.com.cn/static/portal/images/logo.png`
  - 可不可熟成紅茶 → `kebuke.com/.../android-icon-192x192.png`
  - 鮮茶道 → `presotea.com/_next/static/media/logo.svg`
  - 麻古茶坊 → `macutea.com.tw/images/fav.png`
  - 八曜和茶 → `8yotea.com/wp-content/uploads/2023/05/logo2023.png`
  - 龜記茗品 → `guiji-group.com/images/fav.png`
  - 茶聚 → `chage.com.tw/archive/image/weblogo/...`
  - 季緣 → `chiyuantea.com/images/loadingLogo.png`
  - 一芳 → `yifangteaglobal.com/tw/images/logo.png`
  - 五桐號 → `wootea.com/images/logo.png`（白字需加深色背景）

#### ✅ 方法三：AGY Agent 輔助搜尋
- 自己找不到的品牌，派 AGY agent 用 Google 搜尋官網
- AGY 回報 URL 後再手動下載驗證
- **成功案例**：五桐號、八曜和茶、龜記茗品、茶聚、日出茶太、老虎堂、季緣

### 3. SVG 處理
- Wikipedia 的 SVG Logo 可能是白色填色（`fill:#FFFFFF`）
- 用文字取代改成品牌色（如 Chatime 紫色 `#5B2C87`）
- 用 Playwright（Python `sync_playwright`）渲染 SVG 成 PNG：
  ```python
  from playwright.sync_api import sync_playwright
  with sync_playwright() as p:
      browser = p.chromium.launch()
      page = browser.new_page()
      page.set_viewport_size({"width": 250, "height": 60})
      page.set_content('<html><body style="margin:0;padding:5px;background:white;">' + svg + '</body></html>')
      page.screenshot(path='output.png')
      browser.close()
  ```

### 4. 驗證流程（重要！）
- **每次下載後用 `image` 工具 AI 辨識驗證**
- 確認圖片內容與品牌名稱相符
- 第一輪 9 個 Logo 有 6 個是錯的（AI 宣稱正確但實際不然）
- **不能信任 AI 的「正確」判斷，要具體描述圖片內容再人工確認**

### 5. 整合到頁面
- Logo 存放：`assets/drink-logos/{品牌名}.{ext}`
- DRINK_LOGOS mapping 定義在 `food-radar.html`
- 有 Logo → 顯示 `<img class="drink-logo">` + 品牌名
- 無 Logo → 只顯示品牌名（值為空字串 `''`）
- drink-logo CSS: `width:32px; height:32px; object-fit:contain`

## 常見問題

| 問題 | 解法 |
|------|------|
| 官網域名過期/DNS 失敗 | 改用 Wikipedia 或 AGY 搜尋 |
| SSL 憑證錯誤 | Python `ssl.create_default_context()` 關閉驗證 |
| URL 含中文 | `urllib.parse.quote()` 編碼 |
| SVG 白色填色 | 文字取代 `fill:#FFFFFF` → 品牌色 |
| SVG 轉 PNG | Playwright 渲染（Windows 無 cairosvg） |
| 透明背景白字看不見 | PIL 合成深色背景 |
| GitHub Pages 快取 | 網址加 `?v=XX` 參數 |
| push 忘記改版本號 | **每次 push 前確認版本號已更新** |

## 找不到 Logo 的品牌
一沐日、茶魔、九茶 — 沒有獨立官網，主要靠 FB/IG 經營，需手動從社群平台抓取。
