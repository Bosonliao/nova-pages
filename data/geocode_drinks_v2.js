// Geocode drink shops using Nominatim with bounding box filter
const fs = require('fs');
const path = require('path');
const https = require('https');

const dataDir = path.join(__dirname);

// Taiwan county bounding boxes (south,west,north,east) - approximate
const countyBBox = {
  '彰化': [23.80, 120.30, 24.20, 120.70],
  '嘉義': [23.15, 120.10, 23.80, 120.90],
  '新竹': [24.55, 120.75, 24.95, 121.25],
  '花蓮': [23.20, 121.10, 24.50, 121.80],
  '高雄': [22.40, 120.10, 23.20, 121.10],
  '基隆': [25.00, 121.60, 25.30, 121.85],
  '金馬': [24.30, 118.10, 24.60, 118.70],
  '苗栗': [24.25, 120.60, 24.90, 121.30],
  '南投': [23.40, 120.60, 24.30, 121.30],
  '新北': [24.70, 121.20, 25.30, 122.00],
  '澎湖': [23.10, 119.20, 23.80, 119.80],
  '屏東': [21.80, 120.10, 22.90, 121.10],
  '台中': [24.00, 120.40, 24.40, 121.00],
  '台南': [22.80, 120.00, 23.40, 120.70],
  '台北': [24.95, 121.40, 25.20, 121.70],
  '台東': [22.30, 120.90, 23.50, 121.80],
  '桃園': [24.80, 121.00, 25.20, 121.60],
  '宜蘭': [24.40, 121.50, 25.10, 122.20],
  '雲林': [23.40, 120.00, 24.00, 120.70]
};

const brands = [
  '50嵐', '清心福全', 'CoCo都可', '迷客夏', '八曜和茶', '麻古茶坊',
  '龜記茗品', '五桐號', '一沐日', '可不可熟成紅茶', '茶的魔手',
  '茶聚', 'COMEBUY', '茶湯會', '鮮茶道', '珍煮丹', '老虎堂',
  '日出茶太', '大苑子', '一芳', '九茶', '廖老大茶坊'
];

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function nominatimSearch(query, bbox) {
  return new Promise((resolve) => {
    let url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&limit=15&countrycodes=tw`;
    if (bbox) {
      url += `&viewbox=${bbox[1]},${bbox[0]},${bbox[3]},${bbox[2]}&bounded=1`;
    }
    https.get(url, { headers: { 'User-Agent': 'nova-pages-geocoder/1.0' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch(e) { resolve([]); }
      });
    }).on('error', () => resolve([]));
  });
}

function extractArea(displayName) {
  const parts = displayName.split(',');
  for (const p of parts) {
    const trimmed = p.trim();
    if (trimmed.match(/.區$/) || trimmed.match(/.市$/) || trimmed.match(/.鎮$/) || trimmed.match(/.鄉$/)) {
      return trimmed;
    }
  }
  return '';
}

function inBBox(lat, lng, bbox) {
  return lat >= bbox[0] && lat <= bbox[2] && lng >= bbox[1] && lng <= bbox[3];
}

async function main() {
  const results = {};
  let totalFound = 0;

  for (const [county, bbox] of Object.entries(countyBBox)) {
    console.log(`\n=== ${county} ===`);
    const countyShops = [];
    const seen = new Set();

    for (const brand of brands) {
      const query = `${brand} ${county}`;
      console.log(`  Searching: ${query}`);
      const hits = await nominatimSearch(query, bbox);
      await sleep(1100);

      for (const hit of hits) {
        const lat = parseFloat(hit.lat);
        const lng = parseFloat(hit.lon);
        
        if (!inBBox(lat, lng, bbox)) continue;

        // Check name contains brand
        const dn = hit.display_name || '';
        const brandKey = brand.replace('都', '');
        if (!dn.includes(brand) && !dn.includes(brandKey)) continue;

        // Deduplicate by lat+lng (within ~30m)
        const key = `${lat.toFixed(4)},${lng.toFixed(4)}`;
        if (seen.has(key)) continue;
        seen.add(key);

        const area = extractArea(dn);
        countyShops.push({
          name: brand,
          lat: lat,
          lng: lng,
          area: area,
          categories: ['飲品'],
          rating: 0,
          reviews: 0
        });
      }
    }

    results[county] = countyShops;
    totalFound += countyShops.length;
    console.log(`  ${county}: ${countyShops.length} shops`);

    fs.writeFileSync(path.join(dataDir, county + '-drinks-final.json'), JSON.stringify(countyShops, null, 2), 'utf8');
  }

  console.log(`\n=== DONE ===`);
  console.log(`Total: ${totalFound} shops`);
  for (const [county, shops] of Object.entries(results)) {
    console.log(`${county}: ${shops.length}`);
  }
}

main().catch(console.error);