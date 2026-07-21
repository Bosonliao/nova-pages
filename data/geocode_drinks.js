// Geocode drink shops using Nominatim (1 req/sec)
const fs = require('fs');
const path = require('path');
const https = require('https');

const dataDir = path.join(__dirname);
const drinkFiles = [
  '彰化-drinks','嘉義-drinks','新竹-drinks','花蓮-drinks','高雄-drinks',
  '基隆-drinks','金馬-drinks','苗栗-drinks','南投-drinks','新北-drinks',
  '澎湖-drinks','屏東-drinks','台中-drinks','台南-drinks','台北-drinks',
  '台東-drinks','桃園-drinks','宜蘭-drinks','雲林-drinks'
];

const countyMap = {
  '彰化':'Changhua','嘉義':'Chiayi','新竹':'Hsinchu','花蓮':'Hualien','高雄':'Kaohsiung',
  '基隆':'Keelung','金馬':'Kinmen','苗栗':'Miaoli','南投':'Nantou','新北':'New Taipei',
  '澎湖':'Penghu','屏東':'Pingtung','台中':'Taichung','台南':'Tainan','台北':'Taipei',
  '台東':'Taitung','桃園':'Taoyuan','宜蘭':'Yilan','雲林':'Yunlin'
};

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function geocode(name, area, county) {
  return new Promise((resolve, reject) => {
    const countyEn = countyMap[county] || county;
    const q = encodeURIComponent(`${name} ${area || ''} ${countyEn} Taiwan`);
    const url = `https://nominatim.openstreetmap.org/search?q=${q}&format=json&limit=1&countrycodes=tw`;
    const options = {
      hostname: 'nominatim.openstreetmap.org',
      path: `/search?q=${q}&format=json&limit=1&countrycodes=tw`,
      headers: { 'User-Agent': 'nova-pages-geocoder/1.0' }
    };
    https.get(url, { headers: { 'User-Agent': 'nova-pages-geocoder/1.0' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json && json[0]) {
            resolve({ lat: parseFloat(json[0].lat), lng: parseFloat(json[0].lon) });
          } else {
            resolve(null);
          }
        } catch(e) { resolve(null); }
      });
    }).on('error', (e) => resolve(null));
  });
}

async function main() {
  let totalDone = 0;
  let totalFound = 0;
  let totalNotFound = 0;

  for (const file of drinkFiles) {
    const fpath = path.join(dataDir, file + '.json');
    const drinks = JSON.parse(fs.readFileSync(fpath, 'utf8'));
    const county = file.replace('-drinks', '');
    let found = 0, notFound = 0;

    console.log(`\n=== ${file} (${drinks.length} shops) ===`);

    for (const shop of drinks) {
      if (shop.lat && shop.lng && shop.lat !== 0 && shop.lng !== 0) {
        found++;
        continue;
      }

      // Try with shop name + area + county
      let coords = await geocode(shop.name, shop.area, county);
      await sleep(1100); // 1 req/sec rate limit

      if (!coords && shop.area) {
        // Try just shop name + county
        coords = await geocode(shop.name, '', county);
        await sleep(1100);
      }

      if (coords) {
        shop.lat = coords.lat;
        shop.lng = coords.lng;
        found++;
        totalFound++;
        console.log(`  ✓ ${shop.name} (${shop.area || ''}) → ${coords.lat}, ${coords.lng}`);
      } else {
        notFound++;
        totalNotFound++;
        console.log(`  ✗ ${shop.name} (${shop.area || ''}) — not found`);
      }
      totalDone++;
    }

    fs.writeFileSync(fpath, JSON.stringify(drinks, null, 2), 'utf8');
    console.log(`${file}: found=${found}, notFound=${notFound}`);
  }

  console.log(`\n=== DONE ===`);
  console.log(`Total: ${totalDone} processed, ${totalFound} found, ${totalNotFound} not found`);
}

main().catch(console.error);