with open('taiwan-travel.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 升級 getUserLocation — 加 localStorage 記住定位
old_func = """function getUserLocation() {
  if (!navigator.geolocation) { return; }
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      userLocation = { lat: pos.coords.latitude, lng: pos.coords.longitude };
      const banner = document.getElementById('geo-banner');
      if (banner) banner.classList.add('hide');
      render();
    },
    (err) => {
      const banner = document.getElementById('geo-banner');
      if (banner) banner.classList.add('hide');
      render();
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 300000 }
  );
}"""

new_func = """function getUserLocation() {
  if (!navigator.geolocation) { return; }
  // 嘗試用上次記住的位置（瀏覽器記住權限後永久有效）
  try {
    const saved = localStorage.getItem('userLocation');
    if (saved) {
      userLocation = JSON.parse(saved);
      const banner = document.getElementById('geo-banner');
      if (banner) banner.classList.add('hide');
      render();
    }
  } catch(e) {}
  // 重新定位（瀏覽器記住權限後不會再問，直接回傳位置）
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      userLocation = { lat: pos.coords.latitude, lng: pos.coords.longitude };
      try { localStorage.setItem('userLocation', JSON.stringify(userLocation)); } catch(e) {}
      const banner = document.getElementById('geo-banner');
      if (banner) banner.classList.add('hide');
      render();
    },
    (err) => {
      // 定位失敗時：如果有記住的位置就用舊的，隱藏 banner
      // 如果沒有記住的位置，保留 banner 讓使用者可以重試
      if (!userLocation) {
        const banner = document.getElementById('geo-banner');
        if (banner) { banner.classList.remove('hide'); banner.querySelector('span').textContent = '⚠️ 定位失敗，請再試一次'; }
      } else {
        const banner = document.getElementById('geo-banner');
        if (banner) banner.classList.add('hide');
      }
      render();
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 300000 }
  );
}"""

if old_func in content:
    content = content.replace(old_func, new_func)
    print("Updated getUserLocation with localStorage")
else:
    print("ERROR: could not find getUserLocation")

with open('taiwan-travel.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")