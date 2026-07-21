/**
 * drinks-official-to-json.js
 * 
 * 將 drinks-official.md（AGY 查詢結果）轉換成各縣市 JSON 的飲品資料
 * 
 * 步驟：
 * 1. 解析 drinks-official.md，提取每家店的 品牌、分店名、地址
 * 2. 用 Nominatim 將地址轉成 lat/lng 座標
 * 3. 根據地址中的區/鄉鎮判斷 area 欄位
 * 4. 輸出到 drinks-geocoded.json，供後續合併
 * 
 * 用法：node drinks-official-to-json.js [--geocode] [--county 桃園]
 *   --geocode  完整 geocode（不加則只解析 MD 不查座標）
 *   --county   只處理指定縣市
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const MD_PATH = path.join(__dirname, 'drinks-official.md');
const OUTPUT_PATH = path.join(__dirname, 'drinks-geocoded.json');

// 縣市名稱對照（MD 中的名稱 → JSON 中的英文 key）
const COUNTY_MAP = {
  '基隆市': 'keelung',
  '台北市': 'taipei',
  '新北市': 'newtaipei',
  '宜蘭縣': 'yilan',
  '桃園市': 'taoyuan',
  '新竹縣市': 'hsinchu',
  '苗栗縣': 'miaoli',
  '台中市': 'taichung',
  '南投縣': 'nantou',
  '彰化縣': 'changhua',
  '雲林縣': 'yunlin',
  '嘉義縣市': 'chiayi',
  '台南市': 'tainan',
  '高雄市': 'kaohsiung',
  '屏東縣': 'pingtung',
  '花蓮縣': 'hualien',
  '台東縣': 'taitung',
  '澎湖縣': 'penghu',
  '金馬': 'kinmen',
};

// 品牌名統一化
const BRAND_NORMALIZE = {
  'CoCo都可': 'CoCo都可',
  'CoCo 都可': 'CoCo都可',
  'COMEBUY': 'COMEBUY',
  '可不可熟成紅茶': '可不可熟成紅茶',
};

/**
 * 解析 drinks-official.md，提取所有門市資料
 */
function parseMD() {
  const md = fs.readFileSync(MD_PATH, 'utf8');
  const stores = [];
  let currentCounty = '';
  
  const lines = md.split('\n');
  for (const line of lines) {
    // 縣市標題：## 基隆市
    const countyMatch = line.match(/^## (.+)/);
    if (countyMatch) {
      currentCounty = countyMatch[1].trim();
      continue;
    }
    
    // 表格行：| 50嵐 | 楊梅大成店 | 桃園市楊梅區大成路204號 |
    const tableMatch = line.match(/^\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|/);
    if (tableMatch && currentCounty) {
      const brand = tableMatch[1].replace(/\*\*/g, '').trim();
      const storeName = tableMatch[2].trim();
      const address = tableMatch[3].trim();
      
      // 跳過表頭
      if (brand === '品牌名' || brand.startsWith('---') || brand.startsWith(':---')) continue;
      if (!address || address === '完整地址' || address === '（待查）') continue;
      if (address.includes('待查')) continue;
      
      // 統一品牌名
      const normalBrand = BRAND_NORMALIZE[brand] || brand;
      
      stores.push({
        county: currentCounty,
        brand: normalBrand,
        storeName,
        address,
        lat: 0,
        lng: 0,
      });
    }
  }
  
  return stores;
}

/**
 * 從地址提取區/鄉鎮市
 */
function extractArea(address) {
  // 台北/新北/桃園/台中/台南/高雄：OO區
  // 其他縣市：OO市/鎮/鄉
  const match = address.match(/[市縣]([^市縣鄉鎮區]+?[鄉鎮市區])/);
  if (match) {
    // 去掉「市」結尾的（如宜蘭市 → 宜蘭，但楊梅區保留「區」）
    let area = match[1];
    // 六都的區保留「區」
    if (area.endsWith('區')) return area;
    // 其他縣市的市/鎮/鄉去掉後綴
    if (area.endsWith('市')) return area; // 如宜蘭市、花蓮市
    if (area.endsWith('鎮')) return area; // 如羅東鎮
    if (area.endsWith('鄉')) return area; // 如礁溪鄉
    return area;
  }
  return '';
}

/**
 * Nominatim geocode：地址 → 座標
 * 注意：每秒不超過 1 次請求（Nominatim 使用政策）
 */
function geocodeAddress(address) {
  return new Promise((resolve, reject) => {
    const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(address)}&format=json&limit=1&countrycodes=tw&accept-language=zh-TW`;
    
    const req = https.get(url, { headers: { 'User-Agent': 'NovaPages/1.0' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const results = JSON.parse(data);
          if (results.length > 0) {
            resolve({ lat: parseFloat(results[0].lat), lng: parseFloat(results[0].lon), displayName: results[0].display_name });
          } else {
            resolve({ lat: 0, lng: 0, displayName: '' });
          }
        } catch (e) {
          resolve({ lat: 0, lng: 0, displayName: '' });
        }
      });
    });
    
    req.on('error', (e) => resolve({ lat: 0, lng: 0, displayName: '' }));
    req.setTimeout(15000, () => { req.destroy(); resolve({ lat: 0, lng: 0, displayName: '' }); });
  });
}

/**
 * 延遲函數
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function main() {
  const args = process.argv.slice(2);
  const doGeocode = args.includes('--geocode');
  const countyArg = args.indexOf('--county');
  const filterCounty = countyArg >= 0 ? args[countyArg + 1] : null;
  
  console.log('解析 drinks-official.md...');
  let stores = parseMD();
  console.log(`共解析出 ${stores.length} 家門市`);
  
  if (filterCounty) {
    stores = stores.filter(s => s.county.includes(filterCounty));
    console.log(`篩選 ${filterCounty}：${stores.length} 家`);
  }
  
  // 提取 area
  for (const s of stores) {
    s.area = extractArea(s.address);
  }
  
  // Geocode
  if (doGeocode) {
    console.log(`開始 geocode ${stores.length} 個地址（每秒1個，預計 ${Math.ceil(stores.length / 60)} 分鐘）...`);
    let success = 0, fail = 0;
    for (let i = 0; i < stores.length; i++) {
      const s = stores[i];
      const result = await geocodeAddress(s.address);
      s.lat = result.lat;
      s.lng = result.lng;
      if (result.lat !== 0) success++;
      else fail++;
      
      if ((i + 1) % 10 === 0 || i === stores.length - 1) {
        console.log(`  進度 ${i + 1}/${stores.length}（成功 ${success}，失敗 ${fail}）`);
      }
      
      // Nominatim 政策：每秒最多 1 次
      await sleep(1100);
    }
    console.log(`Geocode 完成：成功 ${success}，失敗 ${fail}`);
  } else {
    console.log('跳過 geocode（加上 --geocode 參數才會查座標）');
  }
  
  // 按縣市分組輸出
  const byCounty = {};
  for (const s of stores) {
    const key = COUNTY_MAP[s.county] || s.county;
    if (!byCounty[key]) byCounty[key] = [];
    byCounty[key].push({
      name: s.brand,
      storeName: s.storeName,
      address: s.address,
      area: s.area,
      lat: s.lat,
      lng: s.lng,
      cat: '飲品',
      categories: ['飲品'],
    });
  }
  
  // 讀取已有結果，合併
  let existing = {};
  if (fs.existsSync(OUTPUT_PATH)) {
    existing = JSON.parse(fs.readFileSync(OUTPUT_PATH, 'utf8'));
  }
  
  for (const [key, shops] of Object.entries(byCounty)) {
    existing[key] = shops;
  }
  
  fs.writeFileSync(OUTPUT_PATH, JSON.stringify(existing, null, 2), 'utf8');
  console.log(`已寫入 ${OUTPUT_PATH}`);
  
  // 統計
  for (const [key, shops] of Object.entries(existing)) {
    const withCoords = shops.filter(s => s.lat !== 0).length;
    console.log(`  ${key}: ${shops.length} 家（有座標 ${withCoords}）`);
  }
}

main().catch(console.error);
