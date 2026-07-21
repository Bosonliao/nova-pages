const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent(`
    <html><body style="margin:0;padding:10px;background:white;">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 35.9" width="190" height="38">
    <style>.st0{fill:#5B2C87;} .st1{opacity:0.7;}</style>
    ${await readFile()}
    </svg></body></html>
  `);
  await page.screenshot({ path: path.join(__dirname, '..', 'assets', 'drink-logos', '日出茶太.png'), omitBackground: false });
  await browser.close();
  console.log('OK');
})();
