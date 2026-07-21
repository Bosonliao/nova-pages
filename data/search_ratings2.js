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
      path: '/maps/search/' + query,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'zh-TW,zh;q=0.9'
      }
    };
    https.get(options, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        // Save full response for first spot for debugging
        if (spot.name === '三仙台') {
          fs.writeFileSync('debug_sansiantai.txt', d);
        }
        
        // Look for patterns like 4.3, 2,856 or 4.5(1,234 reviews)
        // Google Maps embeds ratings in the protobuf arrays
        // Common patterns: [4.3,2856] or "4.3" or rating:4.3
        
        // Find all decimal numbers that look like ratings (3.0-5.0 range)
        const allDecimals = d.match(/\b([3-5]\.\d)\b/g);
        // Find all numbers that could be review counts (3-6 digit numbers)
        const allNums = d.match(/\b([\d,]{3,7})\b/g);
        
        // Also try to find patterns near the spot name
        const idx = d.indexOf(spot.name);
        let nearRating = null;
        if (idx > 0) {
          const chunk = d.substring(idx, idx + 2000);
          // Look for rating pattern: number between 1-5 with decimal, followed by review count
          const m = chunk.match(/([3-5]\.\d)[,\s\]]+(\d[\d,]*)/);
          if (m) {
            nearRating = m[1] + ', ' + m[2];
          }
        }
        
        console.log(spot.name + ': nearRating=' + (nearRating || 'none') + 
          ', decimals=' + (allDecimals ? allDecimals.slice(0,5).join(',') : 'none') +
          ', bigNums=' + (allNums ? allNums.slice(0,5).join(',') : 'none'));
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