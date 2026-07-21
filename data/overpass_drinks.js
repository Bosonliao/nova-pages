// Search for bubble tea / drink shops in Taiwan using Overpass API
const fs = require('fs');
const path = require('path');
const https = require('https');

const dataDir = path.join(__dirname);

// County center coordinates for filtering
const countyCenters = {
  '彰化': { lat: 24.0663, lng: 120.5417, name: 'changhua' },
  '嘉義': { lat: 23.4800, lng: 120.4491, name: 'chiayi' },
  '新竹': { lat: 24.8036, lng: 120.9686, name: 'hsinchu' },
  '花蓮': { lat: 23.9871, lng: 121.6016, name: 'hualien' },
  '高雄': { lat: 22.6273, lng: 120.3014, name: 'kaohsiung' },
  '基隆': { lat: 25.1276, lng: 121.7392, name: 'keelung' },
  '金馬': { lat: 24.4327, lng: 118.3186, name: 'kinmen' },
  '苗栗': { lat: 24.5617, lng: 120.8214, name: 'miaoli' },
  '南投': { lat: 23.8388, lng: 120.9876, name: 'nantou' },
  '新北': { lat: 25.0120, lng: 121.4653, name: 'newtaipei' },
  '澎湖': { lat: 23.5653, lng: 119.6151, name: 'penghu' },
  '屏東': { lat: 22.6692, lng: 120.4866, name: 'pingtung' },
  '台中': { lat: 24.1477, lng: 120.6736, name: 'taichung' },
  '台南': { lat: 22.9908, lng: 120.2133, name: 'tainan' },
  '台北': { lat: 25.0330, lng: 121.5654, name: 'taipei' },
  '台東': { lat: 22.7583, lng: 121.1444, name: 'taitung' },
  '桃園': { lat: 24.9936, lng: 121.3014, name: 'taoyuan' },
  '宜蘭': { lat: 24.7020, lng: 121.7375, name: 'yilan' },
  '雲林': { lat: 23.7000, lng: 120.5370, name: 'yunlin' }
};

// Known bubble tea brands to match
const brands = [
  '50嵐','清心福全','CoCo','都可','迷客夏','八曜和茶','麻古','龜記','五桐號',
  '一沐日','可不可','茶魔','季緣','茶聚','COMEBUY','茶湯會','鮮茶道','珍煮丹',
  '老虎堂','日出茶太','茶的魔手','一芳','大苑子','自來水','九茶','茶棧',
  '廖老大','清心','50lan','Comebuy','TEA','茶葉','飲品','手搖'
];

function overpassQuery(query) {
  return new Promise((resolve, reject) => {
    const data = 'data=' + encodeURIComponent(query);
    const options = {
      hostname: 'overpass-api.de',
      path: '/api/interpreter',
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'nova-pages-geocoder/1.0'
      }
    };
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(body)); }
        catch(e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function main() {
  // Query all bubble tea / drink shops in Taiwan
  const query = `
    [out:json][timeout:120];
    area["ISO3166-2"="TW"]->.tw;
    (
      node["amenity"="cafe"]["cuisine"="bubble_tea"](area.tw);
      node["amenity"="cafe"]["bubble_tea"="yes"](area.tw);
      node["shop"="beverages"]["name"](area.tw);
      node["amenity"="cafe"]["name"~"50嵐|清心|CoCo|迷客夏|八曜|麻古|龜記|五桐|茶|飲|手搖|珍煮|老虎|日出|大苑子|一芳|廖老大",i](area.tw);
      node["amenity"="fast_food"]["name"~"50嵐|清心|CoCo|迷客夏|八曜|麻古|龜記|五桐|茶|飲|手搖|珍煮|老虎|日出|大苑子|一芳|廖老大",i](area.tw);
    );
    out center tags 5000;
  `;
  
  console.log('Querying Overpass API for bubble tea shops in Taiwan...');
  const result = await overpassQuery(query);
  const elements = result.elements || [];
  console.log('Found', elements.length, 'drink-related OSM nodes');

  // Group by county using coordinates
  const byCounty = {};
  Object.keys(countyCenters).forEach(c => { byCounty[c] = []; });

  for (const el of elements) {
    const lat = el.lat || (el.center && el.center.lat);
    const lng = el.lon || (el.center && el.center.lon);
    if (!lat || !lng) continue;
    
    const name = el.tags && el.tags.name;
    if (!name) continue;

    // Find nearest county
    let nearest = null;
    let minDist = Infinity;
    for (const [county, center] of Object.entries(countyCenters)) {
      const dist = Math.pow(lat - center.lat, 2) + Math.pow(lng - center.lng, 2);
      if (dist < minDist) {
        minDist = dist;
        nearest = county;
      }
    }
    
    if (nearest && minDist < 1.5) { // within reasonable distance
      byCounty[nearest].push({
        name: name,
        lat: lat,
        lng: lng,
        area: el.tags['addr:district'] || el.tags['addr:suburb'] || '',
        categories: ['飲品'],
        rating: 0,
        reviews: 0
      });
    }
  }

  // Output summary
  for (const [county, shops] of Object.entries(byCounty)) {
    console.log(`${county}: ${shops.length} shops`);
    // Write to drink file
    const fname = countyCenters[county].name + '-drinks-osm.json';
    fs.writeFileSync(path.join(dataDir, fname), JSON.stringify(shops, null, 2), 'utf8');
  }

  console.log('\nDone! OSM drink data written to *-drinks-osm.json files');
}

main().catch(console.error);