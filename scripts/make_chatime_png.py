from PIL import Image, ImageOps
import urllib.request, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# The old white SVG was already downloaded. Let's use a different approach:
# Download the old white SVG, render to image with browser, then process

# Actually, let's just use the old PNG (the green leaf from favicon) as a placeholder
# and mark it as unknown. Instead, let me try a different strategy.

# Let me get the Chatime logo from a different source - their Facebook page or a news article

# Actually the simplest fix: use PIL to create a colored version from the SVG
# Since we can't easily convert SVG on Windows, let me just use a text-based approach

# Create a simple text logo for Chatime
from PIL import Image as PILImage, ImageDraw, ImageFont

# Try to find a suitable font
try:
    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 20)
except:
    font = ImageFont.load_default()

# Purple color matching Chatime brand
img = PILImage.new('RGBA', (120, 40), (255, 255, 255, 0))
draw = ImageDraw.Draw(img)
draw.text((5, 8), "Chatime", fill=(91, 44, 135, 255), font=font)

# Add the speech bubble
draw.ellipse([2, 5, 18, 21], outline=(91, 44, 135, 255), width=2)
draw.ellipse([8, 8, 14, 14], fill=(91, 44, 135, 255))

img.save('assets/drink-logos/日出茶太.png')
print("Created text-based Chatime logo")
