const { chromium } = require('C:/Users/USER/AppData/Roaming/npm/node_modules/n8n/node_modules/playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  const shops = [
    { city: 'taipei', name: '冷水坑', county: '台北', area: '陽明山' },
    { city: 'newtaipei', name: '碧潭', county: '新北', area: '新店' },
    { city: 'taichung', name: '審計新村', county: '台中', area: '西區' },
    { city: 'tainan', name: '神農街', county: '台南', area: '中西區' },
    { city: 'kaohsiung', name: '橋頭糖廠', county: '高雄', area: '橋頭' }
  ];

  const results = [];

  for (const shop of shops) {
    try {
      const query = encodeURIComponent(shop.name + ' ' + shop.county + shop.area);
      await page.goto('https://www.google.com/maps/search/' + query, { waitUntil: 'networkidle', timeout: 20000 });
      await page.waitForTimeout(4000);

      // Try to find rating - look for spans with X.X pattern
      const ratingText = await page.evaluate(() => {
        const allSpans = document.querySelectorAll('span');
        for (const span of allSpans) {
          const text = span.textContent.trim();
          if (/^\d\.\d$/.test(text)) return text;
        }
        // Try aria-label with star info
        const els = document.querySelectorAll('[aria-label]');
        for (const el of els) {
          const label = el.getAttribute('aria-label') || '';
          if (/[\d.]+\s*(星|star)/i.test(label)) {
            const match = label.match(/([\d.]+)/);
            if (match) return match[1];
          }
        }
        return null;
      });

      // Try to find reviews count
      const reviewsText = await page.evaluate(() => {
        const allSpans = document.querySelectorAll('span');
        for (const span of allSpans) {
          const text = span.textContent.trim();
          if (/[\d,]+\s*(則評論|reviews|篇評論|則Google評論)/.test(text)) return text;
        }
        // Also try divs
        const allDivs = document.querySelectorAll('div');
        for (const div of allDivs) {
          const text = div.textContent.trim();
          if (/^[\d,]+\s*(則評論|reviews)$/.test(text)) return text;
        }
        return null;
      });

      let rating = null;
      let reviews = null;

      if (ratingText) {
        const match = ratingText.match(/([\d.]+)/);
        if (match) rating = parseFloat(match[1]);
      }

      if (reviewsText) {
        const match = reviewsText.match(/([\d,]+)/);
        if (match) reviews = parseInt(match[1].replace(/,/g, ''));
      }

      results.push({ ...shop, rating, reviews });
      console.log(shop.name + ': rating=' + rating + ', reviews=' + reviews);
    } catch(e) {
      results.push({ ...shop, rating: null, reviews: null, error: e.message });
      console.log(shop.name + ': ERROR - ' + e.message);
    }
    await page.waitForTimeout(3000);
  }

  // Write results to a temp file
  fs.writeFileSync(__dirname + '/rating_results.json', JSON.stringify(results, null, 2), 'utf8');
  console.log('\nResults saved to scripts/rating_results.json');
  console.log(JSON.stringify(results, null, 2));

  await browser.close();
})();