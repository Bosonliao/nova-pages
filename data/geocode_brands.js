// Geocode drink shops using Nominatim with brand names + county
const fs = require('fs');
const path = require('path');
const https = require('https');

const dataDir = path.join(__dirname);

// Major bubble tea brands known in Taiwan
const brands = [
  '50嵐', '清心福全', 'CoCo都可', '迷客夏', '八曜和茶', '麻古茶坊',
  '龜記茗品', '五桐號', '一沐日', '可不可熟成紅茶', '茶的魔手',
  '茶聚', 'COMEBUY', '茶湯會', '鮮茶道', '珍煮丹', '老虎堂',
  '日出茶太', '大苑子', '一芳', '自來水果汁冰品', '九茶',
  '廖老大茶坊', '清心福全冷飲站'
];

const counties = [
  { cn: '彰化', en: 'Changhua' },
  { cn: '嘉義', en: 'Chiayi' },
  { cn: '新竹', en: 'Hsinchu' },
  { cn: '花蓮', en: 'Hualien' },
  { cn: '高雄', en: 'Kaohsiung' },
  { cn: '基隆', en: 'Keelung' },
  { cn: '金馬', en: 'Kinmen' },
  { cn: '苗栗', en: 'Miaoli' },
  { cn: '南投', en: 'Nantou' },
  { cn: '新北', en: 'New Taipei' },
  { cn: '澎湖', en: 'Penghu' },
  { cn: '屏東', en: 'Pingtung' },
  { cn: '台中', en: 'Taichung' },
  { cn: '台南', en: 'Tainan' },
  { cn: '台北', en: 'Taipei' },
  { cn: '台東', en: 'Taitung' },
  { cn: '桃園', en: 'Taoyuan' },
  { cn: '宜蘭', en: 'Yilan' },
  { cn: '雲林', en: 'Yunlin' }
];

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function nominatimSearch(query) {
  return new Promise((resolve) => {
    const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&limit=10&countrycodes=tw`;
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

// Extract area (district) from display_name
function extractArea(displayName, countyCn) {
  const parts = displayName.split(',');
  for (const p of parts) {
    const trimmed = p.trim();
    // Look for district/area markers
    if (trimmed.match(/.區$/) || trimmed.match(/.市$/) || trimmed.match(/.鎮$/) || trimmed.match(/.鄉$/)) {
      return trimmed.replace(/^[臺台]/, '');
    }
  }
  return '';
}

async function main() {
  const results = {};
  counties.forEach(c => { results[c.cn] = []; });

  let totalFound = 0;

  for (const county of counties) {
    console.log(`\n=== ${county.cn} ===`);
    const countyShops = [];

    for (const brand of brands) {
      // Search for brand + county name in Chinese
      const query = `${brand} ${county.cn}`;
      console.log(`  Searching: ${query}`);
      const hits = await nominatimSearch(query);
      await sleep(1100); // 1 req/sec

      for (const hit of hits) {
        const lat = parseFloat(hit.lat);
        const lng = parseFloat(hit.lon);
        
        // Verify it's in Taiwan and roughly in the right county
        // Skip if name doesn't contain the brand
        if (!hit.display_name.includes(brand) && !hit.display_name.includes(brand.replace('都', ''))) {
          // Some brands have slight name variations
          if (brand === 'CoCo都可' && !hit.display_name.includes('CoCo') && !hit.display_name.includes('coco')) continue;
          if (brand === '清心福全冷飲站' && !hit.display_name.includes('清心')) continue;
          if (brand !== 'CoCo都可' && brand !== '清心福全冷飲站' && !hit.display_name.includes(brand)) continue;
        }

        // Deduplicate by name + coords (within 50m)
        const dup = countyShops.find(s => 
          s.name === brand && 
          Math.abs(s.lat - lat) < 0.0005 && 
          Math.abs(s.lng - lng) < 0.0005
        );
        if (dup) continue;

        const area = extractArea(hit.display_name, county.cn);
        countyShops.push({
          name: brand,
          lat: lat,
          lng: lng,
          area: area,
          categories: ['飲品'],
          rating: 0,
          reviews: 0
        });
        totalFound++;
      }
    }

    results[county.cn] = countyShops;
    console.log(`  ${county.cn}: ${countyShops.length} shops found`);

    // Save to file
    const fname = county.cn + '-drinks-geocoded.json';
    fs.writeFileSync(path.join(dataDir, fname), JSON.stringify(countyShops, null, 2), 'utf8');
  }

  console.log(`\n=== DONE ===`);
  console.log(`Total shops found: ${totalFound}`);
  
  // Summary
  for (const county of counties) {
    console.log(`${county.cn}: ${results[county.cn].length}`);
  }
}

main().catch(console.error);