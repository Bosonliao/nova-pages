const https = require('https');

function searchBing(query) {
  return new Promise((resolve, reject) => {
    const url = 'https://www.bing.com/search?q=' + encodeURIComponent(query);
    https.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
      }
    }, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        // Save first 5000 chars for inspection
        require('fs').writeFileSync('bing_debug.txt', data.slice(0, 10000));
        
        // Look for any decimal numbers that could be ratings
        const allDecimals = data.match(/\d\.\d/g);
        console.log('All decimals found:', allDecimals ? allDecimals.slice(0, 20) : 'none');
        
        // Look for review-related text
        const reviewTexts = data.match(/[\d,]+\s*(?:則評論|reviews|review|評論數)/gi);
        console.log('Review text matches:', reviewTexts ? reviewTexts.slice(0, 10) : 'none');
        
        // Look for star ratings
        const stars = data.match(/★\s*\d\.\d|\d\.\d\s*★/g);
        console.log('Star matches:', stars ? stars.slice(0, 10) : 'none');
        
        // Look for rating attribute
        const ratings = data.match(/rating["':\s]+[\d.]+/gi);
        console.log('Rating attr:', ratings ? ratings.slice(0, 10) : 'none');
        
        resolve();
      });
    }).on('error', reject);
  });
}

(async () => {
  await searchBing('鮮茶道 關山鎮 台東 Google 評分');
})();