// Script to process a batch of restaurants and add dishes
// Usage: node add_dishes_batch.js <startIndex> <count>
// Outputs JSON results for the batch to stdout

const fs = require('fs');
const path = require('path');

const dataPath = path.join(__dirname, 'data-zh.json');
const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
const food = data['台北'].food;

// Find all restaurants needing dishes
const needDishes = food.filter(p => {
  const hasMichelin = p.tags && p.tags.includes('michelin');
  const isPopular = p.rating >= 4.0 && p.reviews >= 1000;
  const noDishes = !p.dishes || p.dishes.length === 0;
  return (hasMichelin || isPopular) && noDishes;
});

const startIdx = parseInt(process.argv[2] || '0');
const count = parseInt(process.argv[3] || '5');
const batch = needDishes.slice(startIdx, startIdx + count);

// Output the names and indices for this batch
console.log(JSON.stringify({
  totalNeed: needDishes.length,
  startIndex: startIdx,
  batchSize: batch.length,
  restaurants: batch.map((p, i) => ({
    index: startIdx + i,
    name: p.name,
    tags: p.tags,
    rating: p.rating,
    reviews: p.reviews
  }))
}));