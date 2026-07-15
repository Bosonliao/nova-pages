// Helper script to extract the list of restaurants needing dishes
const data = require('./data-zh.json');
const taipei = data['台北'];
const food = taipei.food;
const needDishes = [];
for (let i = 0; i < food.length; i++) {
  const r = food[i];
  const hasMichelin = r.tags && r.tags.includes('michelin');
  const isPopular = r.rating >= 4.0 && r.reviews >= 1000;
  const hasDishes = r.dishes && r.dishes.length > 0;
  if ((hasMichelin || isPopular) && !hasDishes) {
    needDishes.push({index: i, name: r.name});
  }
}
console.log(JSON.stringify(needDishes));
