const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const svgContent = fs.readFileSync(path.join(__dirname, '..', 'assets/drink-logos/日出茶太.svg'), 'utf-8');
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 250, height: 60 });
  const html = '<html><body style="margin:0;padding:5px;background:white;">' + svgContent + '</body></html>';
  await page.setContent(html);
  await page.screenshot({
    path: path.join(__dirname, '..', 'assets/drink-logos', '日出茶太.png'),
    omitBackground: false
  });
  await browser.close();
  console.log('OK - Chatime PNG created');
})();
