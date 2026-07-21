import re

with open('taiwan-travel.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 移除 detectCityByCoords 函數
start = content.find('// 縣市座標偵測')
if start == -1:
    start = content.find('function detectCityByCoords')
if start != -1:
    # 找到函數結尾 (return null;\n})
    end = content.find('}\n', content.find('return null;', start))
    if end != -1:
        end += 2
        # 也移除前面的空行
        while start > 0 and content[start-1] == '\n':
            start -= 1
        content = content[:start] + content[end:]
        print("Removed detectCityByCoords function")

# 2. 恢復 getUserLocation 成功 callback — 移除自動切換邏輯，改回單純 render()
# 找到成功 callback 裡的自動切換代碼
old_success = """      // 自動切換到使用者所在的縣市
      const detectedCity = detectCityByCoords(userLocation.lat, userLocation.lng);
      if (detectedCity && detectedCity !== currentCounty) {
        const oldCounty = currentCounty;
        selectCounty(detectedCity);
        // 顯示提示
        const tip = document.createElement('div');
        tip.style.cssText = 'position:fixed;top:60px;left:50%;transform:translateX(-50%);background:#4caf50;color:#fff;padding:8px 20px;border-radius:20px;font-size:14px;z-index:1001;box-shadow:0 2px 12px rgba(0,0,0,.3);animation:slideDown .4s ease;';
        tip.textContent = '📍 已自動切換到 ' + detectedCity;
        document.body.appendChild(tip);
        setTimeout(() => { tip.style.opacity='0'; tip.style.transition='opacity .5s'; setTimeout(()=>tip.remove(), 500); }, 3000);
      } else {
        render();
      }"""
new_success = "      render();"
if old_success in content:
    content = content.replace(old_success, new_success)
    print("Restored success callback to simple render()")
else:
    print("WARNING: Could not find success callback auto-switch code")

# 3. 恢復 err callback — 移除修改過的邏輯，改回原始的隱藏 banner + render()
old_err = """      // 定位失敗時不隱藏 banner，讓使用者可以再點「允許定位」
      // 但如果之前已經定位成功過(userLocation已存在)，保持靜默
      if (!userLocation) {
        const banner = document.getElementById('geo-banner');
        if (banner) { banner.classList.remove('hide'); banner.querySelector('span').textContent = '⚠️ 定位失敗，請再試一次'; }
      }
      render();"""
new_err = """      const banner = document.getElementById('geo-banner');
      if (banner) banner.classList.add('hide');
      render();"""
if old_err in content:
    content = content.replace(old_err, new_err)
    print("Restored err callback to original hide+render")
else:
    print("WARNING: Could not find err callback code")

with open('taiwan-travel.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")