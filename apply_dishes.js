// apply_dishes.js - Apply dishes to data-zh.json
// Usage: node apply_dishes.js <json_file_with_dishes>
// The json file should be an array of {name, dishes: [{name, desc}]}

const fs = require('fs');
const path = require('path');

const dataPath = path.join(__dirname, 'data-zh.json');
const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
const food = data['台北'].food;

const dishesData = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));

let applied = 0;
let skipped = 0;

for (const item of dishesData) {
  const restaurant = food.find(p => p.name === item.name);
  if (!restaurant) {
    console.log(`NOT FOUND: ${item.name}`);
    skipped++;
    continue;
  }
  if (restaurant.dishes && restaurant.dishes.length > 0) {
    console.log(`ALREADY HAS DISHES: ${item.name}`);
    skipped++;
    continue;
  }
  restaurant.dishes = item.dishes;
  applied++;
  console.log(`APPLIED: ${item.name} (${item.dishes.length} dishes)`);
}

// Save
fs.writeFileSync(dataPath, JSON.stringify(data, null, 2), 'utf8');
console.log(`\nDone: ${applied} applied, ${skipped} skipped, saved to ${dataPath}`);