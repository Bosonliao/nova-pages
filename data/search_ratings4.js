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
        const idx = d.indexOf(spot.name);
        if (idx < 0) {
          console.log(spot.name + ': name not found, len=' + d.length);
          resolve();
          return;
        }
        
        // Get a larger context window
        const chunk = d.substring(idx, idx + 10000);
        
        // The Google Maps tbm=map format has data in nested arrays
        // Rating is typically: null,null,X.X,null or [X.X, reviewCount]
        // Let's find patterns like: ,4.5, or ,4.5] or null,4.5,
        // Excluding 13.1 which is zoom level
        
        const lines = chunk.split('\n');
        let found = false;
        
        // Search for rating patterns: a decimal between 1.0-5.0 that's not 13.1
        // In the array context: ,null,null,4.5,null,  or  [4.5,
        for (let i = 0; i < chunk.length; i++) {
          // Look for patterns like ,X.X, where X is 1-5
          if (chunk[i] === ',' && i + 3 < chunk.length) {
            const substr = chunk.substring(i + 1, i + 4);
            const m = substr.match(/^([1-5]\.\d)/);
            if (m) {
              const rating = parseFloat(m[1]);
              if (rating !== 13.1 && rating >= 1.0 && rating <= 5.0) {
                // Get context
                const ctx = chunk.substring(Math.max(0, i - 20), i + 30);
                // Skip if it's part of a coordinate (e.g., 23.XXXX)
                const before = chunk.substring(Math.max(0, i - 5), i);
                if (!before.match(/\d$/)) {
                  // Look for review count nearby (within 50 chars)
                  const nearby = chunk.substring(i, i + 100);
                  const revMatch = nearby.match(/(\d[\d,]{2,6})/);
                  if (revMatch && !revMatch[1].match(/^\d{6,}/)) {
                    // Check if there's a review-related text nearby
                    const textNearby = chunk.substring(i, i + 200);
                    const hasReviewText = textNearby.match(/評|review|則/);
                    console.log(spot.name + ': rating=' + m[1] + ', possibleReviews=' + revMatch[1] + (hasReviewText ? ' (has review text)' : ' (no review text)'));
                    console.log('  ctx: ' + ctx.replace(/\n/g, ' '));
                    found = true;
                    break;
                  }
                }
              }
            }
          }
        }
        
        if (!found) {
          // Try a broader search: look for any decimal in 1-5 range with a large number nearby
          const broadMatch = chunk.match(/,([1-5]\.\d),[^0-9]{0,50}(\d[\d,]{2,5})/);
          if (broadMatch) {
            console.log(spot.name + ': broadMatch rating=' + broadMatch[1] + ', reviews=' + broadMatch[2]);
          } else {
            // Last resort: look for "評分" or "rating" text
            const ratingText = chunk.match(/評分[:\s]*([0-9.]+)/);
            const reviewsText = chunk.match(/(\d[\d,]*)\s*(?:則評|評論|reviews)/);
            if (ratingText || reviewsText) {
              console.log(spot.name + ': rating=' + (ratingText ? ratingText[1] : '?') + ', reviews=' + (reviewsText ? reviewsText[1] : '?'));
            } else {
              console.log(spot.name + ': no rating found');
              // Save chunk for debugging
              fs.writeFileSync('debug_chunk_' + spot.city + '.txt', chunk.substring(0, 3000));
            }
          }
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