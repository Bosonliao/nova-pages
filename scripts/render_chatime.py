import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import sync_playwright

svg_path = os.path.join('assets', 'drink-logos', '日出茶太.svg')
out_path = os.path.join('assets', 'drink-logos', '日出茶太.png')

with open(svg_path, 'r', encoding='utf-8') as f:
    svg_content = f.read()

html = '<html><body style="margin:0;padding:5px;background:white;">' + svg_content + '</body></html>'

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_viewport_size({"width": 250, "height": 60})
    page.set_content(html)
    page.screenshot(path=out_path, omit_background=False)
    browser.close()

print('OK - Chatime PNG created')
