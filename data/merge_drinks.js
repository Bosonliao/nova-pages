// Merge geocoded drink shops into each county's food array
const fs = require('fs');
const path = require('path');

const dataDir = path.join(__dirname);

const countyFiles = {
  '彰化': 'changhua',
  '嘉義': 'chiayi',
  '新竹': 'hsinchu',
  '花蓮': 'hualien',
  '高雄': 'kaohsiung',
  '基隆': 'keelung',
  '金馬': 'kinmen',
  '苗栗': 'miaoli',
  '南投': 'nantou',
  '新北': 'newtaipei',
  '澎湖': 'penghu',
  '屏東': 'pingtung',
  '台中': 'taichung',
  '台南': 'tainan',
  '台北': 'taipei',
  '台東': 'taitung',
  '桃園': 'taoyuan',
  '宜蘭': 'yilan',
  '雲林': 'yunlin'
};

let totalAdded = 0;

for (const [countyCn, countyEn] of Object.entries(countyFiles)) {
  const drinkFile = path.join(dataDir, countyCn + '-drinks-final.json');
  const foodFile = path.join(dataDir, countyEn + '.json');
  
  // Read drink data
  const drinks = JSON.parse(fs.readFileSync(drinkFile, 'utf8'));
  if (drinks.length === 0) {
    console.log(`${countyCn} (${countyEn}): 0 drinks, skipped`);
    continue;
  }

  // Read food data
  const foodData = JSON.parse(fs.readFileSync(foodFile, 'utf8'));
  const food = foodData.food || [];
  const beforeCount = food.length;

  // Check for duplicates (same name + same coords)
  const existingKeys = new Set();
  food.forEach(r => {
    const key = `${r.name}_${r.lat}_${r.lng}`;
    existingKeys.add(key);
  });

  // Also check if there are already drink entries with same name within 50m
  const existingDrinkNames = new Set();
  food.forEach(r => {
    if ((r.categories || []).includes('飲品') || (r.categories || []).includes('饮品')) {
      existingDrinkNames.add(r.name);
    }
  });

  let added = 0;
  for (const drink of drinks) {
    // Skip if already has same brand name in drinks (avoid too many duplicates)
    const key = `${drink.name}_${drink.lat.toFixed(4)}_${drink.lng.toFixed(4)}`;
    if (existingKeys.has(key)) continue;
    
    // For Taipei: already has 20 drink shops, add the new ones
    // Just add all unique coordinate entries
    food.push(drink);
    existingKeys.add(key);
    added++;
  }

  foodData.food = food;
  fs.writeFileSync(foodFile, JSON.stringify(foodData, null, 2), 'utf8');
  
  console.log(`${countyCn} (${countyEn}): ${beforeCount} → ${food.length} food items (+${added} drinks)`);
  totalAdded += added;
}

console.log(`\n=== DONE ===`);
console.log(`Total drinks added: ${totalAdded}`);