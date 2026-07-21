const https = require('https');

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
        // Try to find rating patterns
        const ratingMatch = d.match(/(\d\.\d)\s*\(?(\d[\d,]*)\s*(?:評論|reviews)/);
        if (ratingMatch) {
          console.log(spot.name + ': rating=' + ratingMatch[1] + ', reviews=' + ratingMatch[2]);
        } else {
          const m2 = d.match(/"rating"[:\s]+"?(\d\.\d)/);
          const m3 = d.match(/"user_ratings_total"[:\s]+(\d+)/);
          if (m2 || m3) {
            console.log(spot.name + ': rating=' + (m2 ? m2[1] : '?') + ', reviews=' + (m3 ? m3[1] : '?'));
          } else {
            // Save a snippet for debugging
            const idx = d.indexOf(spot.name);
            if (idx > 0) {
              const snippet = d.substring(idx - 50, idx + 300).replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ');
              console.log(spot.name + ': snippet=' + snippet.substring(0, 200));
            } else {
              console.log(spot.name + ': no mention, pageLen=' + d.length);
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