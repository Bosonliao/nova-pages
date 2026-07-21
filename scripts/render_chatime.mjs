import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const svgContent = fs.readFileSync(path.join(process.cwd(), 'assets/drink-logos/日出茶太.svg'), 'utf-8');

const browser = await chromium.launch();
const page = await browser.newPage();
await page.setViewportSize({ width: 250, height: 60 });
await page.setContent(`
  <html><body style="margin:0;padding:5px;background:white;">
  ${svgContent}
  </body></html>
`);
await page.screenshot({
  path: path.join(process.cwd(), 'assets/drink-logos/日出茶太.png'),
  omitBackground: false
});
await browser.close();
console.log('OK - Chatime PNG created');
