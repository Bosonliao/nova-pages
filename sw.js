// Service Worker for Nova Pages PWA
const CACHE_NAME = 'nova-pages-v2';
const ASSETS = [
  '/nova-pages/taiwan-travel.html',
  '/nova-pages/taiwan-travel-ja.html',
  '/nova-pages/manifest.json',
  '/nova-pages/pwa-icon-192.png',
  '/nova-pages/pwa-icon-512.png',
  '/nova-pages/favicon-32.png',
  '/nova-pages/apple-touch-icon.png'
];

// Install - precache key assets only
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

// Activate - clean old caches and claim clients
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// Fetch - only serve from cache for precached assets, NEVER intercept data files
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  
  const url = new URL(event.request.url);
  
  // Only handle same-origin requests
  if (url.origin !== self.location.origin) return;
  
  // Skip data files - let the page fetch them directly from network
  if (url.pathname.includes('/data/') || url.pathname.includes('/data-ja/')) {
    return;
  }
  
  // For precached assets, serve from cache then update
  event.respondWith(
    caches.match(event.request)
      .then((cached) => {
        if (cached) {
          // Update cache in background
          fetch(event.request).then((response) => {
            if (response && response.status === 200) {
              const clone = response.clone();
              caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
            }
          }).catch(() => {});
          return cached;
        }
        // Not in cache, fetch from network
        return fetch(event.request).then((response) => {
          if (response && response.status === 200) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          }
          return response;
        });
      })
  );
});
