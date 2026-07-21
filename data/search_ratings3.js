const https = require('https');
const fs = require('fs');

const spots = [
  {name: '三仙台', area: '台東', city: 'taitung'},
  {name: '石梯坪', area: '花蓮', city: 'hualien'},
  {name: '羅東夜市', area: '宜蘭', city: 'yilan'},
  {name: '橋頭糖廠', area: '高雄', city: 'kaohsiung'},
  {name: '八卦山天空步道', area: '彰化', city: 'changhua'}
];

function searchSpot(spot) {
  return new Promise((resolve) => {
    const query = encodeURIComponent(spot.name + ' ' + spot.area);
    // Use the tbm=map endpoint which returns map search results
    const options = {
      hostname: 'www.google.com',
      path: '/search?tbm=map&hl=zh-TW&gl=tw&q=' + query,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-TW,zh;q=0.9',
        'Accept': 'text/html,application/xhtml+xml'
      }
    };
    https.get(options, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        // The tbm=map response has ratings in a specific format
        // Look for patterns like: "4.3" and nearby review counts
        // In the map results, rating appears as a standalone decimal, and reviews as a number
        
        const idx = d.indexOf(spot.name);
        if (idx < 0) {
          console.log(spot.name + ': name not found, len=' + d.length);
          resolve();
          return;
        }
        
        // Get a large context window after the name
        const chunk = d.substring(idx, idx + 5000);
        
        // In Google Maps tbm=map results, the data is in JSON-like arrays
        // Rating typically appears as a number like 4.3
        // Reviews count appears as a nearby number
        // Pattern: [null,...,"4.3","2,856 reviews"...] or similar
        
        // Find all occurrences of patterns like X.X (potential ratings)
        const ratingPattern = /([3-5]\.\d)(?:",|",|"\]|[\],])/g;
        let match;
        let results = [];
        while ((match = ratingPattern.exec(chunk)) !== null) {
          // Get context around the match
          const ctx = chunk.substring(Math.max(0, match.index - 30), match.index + 50);
          results.push({rating: match[1], ctx: ctx.replace(/<[^>]+>/g, '').trim()});
        }
        
        // Also look for review count patterns
        const reviewPattern = /(\d[\d,]*)\s*(?:則評|評論|reviews|review)/g;
        let revMatches = [];
        while ((match = reviewPattern.exec(chunk)) !== null) {
          revMatches.push(match[1]);
        }
        
        // Look for the specific Google Maps format: ["4.3","(2,856)"]
        const combined = chunk.match(/([3-5]\.\d)[^\d]{1,10}(\d[\d,]*)\s*(?:則評|評論|reviews|review)/);
        
        if (results.length > 0) {
          console.log(spot.name + ':');
          results.slice(0, 3).forEach(r => console.log('  rating=' + r.rating + ' ctx: ' + r.ctx));
          if (revMatches.length > 0) console.log('  reviews: ' + revMatches.slice(0, 3).join(', '));
          if (combined) console.log('  combined: ' + combined[1] + ', ' + combined[2]);
        } else {
          console.log(spot.name + ': no rating found in context');
          // Save first 1000 chars of context for debugging
          fs.writeFileSync('debug_' + spot.name + '.txt', chunk.substring(0, 2000));
        }
        resolve();
      });
    }).on('error', e => { console.log(spot.name + ': err ' + e); resolve(); });
  });
}

(async () => {
  for (const s of spots) {
    await searchSpot(s);
  }
})();