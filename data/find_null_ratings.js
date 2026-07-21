const fs = require('fs');
const path = require('path');

const cities = ['taipei','newtaipei','taichung','tainan','kaohsiung','hsinchu','taoyuan','changhua','chiayi','miaoli','nantou','yunlin','pingtung','yilan','hualien','taitung','penghu','keelung','kinmen'];

const results = {};
let totalNull = 0;

for (const city of cities) {
  const file = path.join(__dirname, `${city}.json`);
  if (!fs.existsSync(file)) continue;
  
  const data = JSON.parse(fs.readFileSync(file, 'utf-8'));
  
  // Check structure - could be array or object with spots
  let spots = [];
  if (Array.isArray(data)) {
    spots = data;
  } else if (data.spots) {
    spots = data.spots;
  } else if (data.places) {
    spots = data.places;
  } else {
    // It might be an object with named keys
    spots = Object.values(data);
  }
  
  const nullShops = [];
  for (const spot of spots) {
    if (spot.rating === null || spot.rating === undefined || spot.rating === '') {
      nullShops.push({
        name: spot.name || spot.title || 'unknown',
        district: spot.district || spot.area || '',
        id: spot.id || spot.place_id || ''
      });
    }
  }
  
  if (nullShops.length > 0) {
    results[city] = nullShops;
    totalNull += nullShops.length;
  }
}

console.log(`Total null rating shops: ${totalNull}`);
for (const [city, shops] of Object.entries(results)) {
  console.log(`\n${city}: ${shops.length} null shops`);
  // Show first 5
  shops.slice(0, 5).forEach(s => console.log(`  - ${s.name} (${s.district})`));
}