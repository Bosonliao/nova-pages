/**
 * merge-official-drinks.js
 * 
 * 將 drinks-geocoded.json 的飲品資料合併到各縣市 JSON 檔
 * 
 * 步驟：
 * 1. 讀取 drinks-geocoded.json
 * 2. 讀取各縣市 JSON（如 keelung.json）
 * 3. 移除該縣市 JSON 中 cat=飲品 的舊資料（Nominatim 不可靠的資料）
 * 4. 加入 drinks-geocoded.json 中該縣市的新資料（AGY 查詢 + 地址 geocode）
 * 5. 寫回 JSON 檔
 * 
 * 用法：node merge-official-drinks.js [--county keelung] [--all] [--dry-run]
 *   --county   只處理指定縣市
 *   --all      處理所有有資料的縣市
 *   --dry-run  只顯示不寫入
 */

const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname);
const GEOCODED_PATH = path.join(DATA_DIR, 'drinks-geocoded.json');

const COUNTY_FILES = {
  keelung: 'keelung.json',
  taipei: 'taipei.json',
  newtaipei: 'newtaipei.json',
  yilan: 'yilan.json',
  taoyuan: 'taoyuan.json',
  hsinchu: 'hsinchu.json',
  miaoli: 'miaoli.json',
  taichung: 'taichung.json',
  nantou: 'nantou.json',
  changhua: 'changhua.json',
  yunlin: 'yunlin.json',
  chiayi: 'chiayi.json',
  tainan: 'tainan.json',
  kaohsiung: 'kaohsiung.json',
  pingtung: 'pingtung.json',
  hualien: 'hualien.json',
  taitung: 'taitung.json',
  penghu: 'penghu.json',
  kinmen: 'kinmen.json',
};

function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const countyArg = args.indexOf('--county');
  const doAll = args.includes('--all');
  
  if (!fs.existsSync(GEOCODED_PATH)) {
    console.error(`找不到 ${GEOCODED_PATH}，請先跑 drinks-official-to-json.js`);
    process.exit(1);
  }
  
  const geocoded = JSON.parse(fs.readFileSync(GEOCODED_PATH, 'utf8'));
  
  // 決定處理哪些縣市
  let targets = [];
  if (countyArg >= 0) {
    targets = [args[countyArg + 1]];
  } else if (doAll) {
    targets = Object.keys(geocoded);
  } else {
    console.log('請指定 --county <key> 或 --all');
    process.exit(1);
  }
  
  for (const key of targets) {
    if (!geocoded[key] || geocoded[key].length === 0) {
      console.log(`${key}: 無飲品資料，跳過`);
      continue;
    }
    
    const jsonFile = path.join(DATA_DIR, COUNTY_FILES[key]);
    if (!fs.existsSync(jsonFile)) {
      console.log(`${key}: 找不到 ${COUNTY_FILES[key]}，跳過`);
      continue;
    }
    
    const countyData = JSON.parse(fs.readFileSync(jsonFile, 'utf8'));
    const oldFood = countyData.food || [];
    
    // 移除舊的飲品資料
    const oldDrinks = oldFood.filter(f => (f.categories || []).includes('飲品') || f.cat === '飲品');
    const oldNonDrinks = oldFood.filter(f => !(f.categories || []).includes('飲品') && f.cat !== '飲品');
    
    // 新飲品資料
    const newDrinks = geocoded[key].map(d => ({
      name: d.name,
      description: '',
      area: d.area,
      rating: 0,
      reviews: 0,
      categories: ['飲品'],
      category: '飲品',
      tags: [],
      _sort: 5,
      dishes: [],
      lat: d.lat,
      lng: d.lng,
      cat: '飲品',
      storeName: d.storeName,
      address: d.address,
    }));
    
    // 合併
    countyData.food = [...oldNonDrinks, ...newDrinks];
    
    console.log(`${key}: 舊飲品 ${oldDrinks.length} 家 → 新飲品 ${newDrinks.length} 家（有座標 ${newDrinks.filter(d => d.lat !== 0).length}）`);
    console.log(`  總食物：${oldNonDrinks.length}（非飲品）+ ${newDrinks.length}（飲品）= ${countyData.food.length}`);
    
    if (!dryRun) {
      fs.writeFileSync(jsonFile, JSON.stringify(countyData, null, 2), 'utf8');
      console.log(`  已寫入 ${COUNTY_FILES[key]}`);
    } else {
      console.log(`  [dry-run] 不寫入`);
    }
  }
}

main();
