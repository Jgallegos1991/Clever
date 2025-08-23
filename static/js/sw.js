// Minimal service worker for Clever PWA
const CACHE = 'clever-shell-v1';
const CORE = [
  '/',
  '/static/css/style.css',
  '/static/js/three-bridge.js',
  '/static/js/three.min.js',
  '/static/js/orb_engine.js',
  '/static/js/ui.js',
  '/static/js/main.js',
  '/static/img/favicon.svg',
  '/static/manifest.webmanifest'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(CORE)).then(self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  // network-first for HTML, cache-first for static
  if (req.mode === 'navigate') {
    e.respondWith(fetch(req).catch(() => caches.match('/')));
    return;
  }
  if (req.url.includes('/static/')) {
    e.respondWith(caches.match(req).then(res => res || fetch(req).then(r => {
      const copy = r.clone();
      caches.open(CACHE).then(c => c.put(req, copy));
      return r;
    })));
    return;
  }
});
// Minimal service worker for Clever PWA
const CACHE = 'clever-cache-v1';
const ASSETS = [
  '/',
  '/static/css/style.css',
  '/static/js/three-bridge.js',
  '/static/js/orb_engine.js',
  '/static/js/ui.js',
  '/static/js/main.js',
  '/static/img/favicon.svg'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.map(k => (k === CACHE) ? null : caches.delete(k)))));
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  if (url.origin === location.origin) {
    e.respondWith(
      caches.match(e.request).then((res) => res || fetch(e.request).then((r) => {
        const copy = r.clone();
        caches.open(CACHE).then((c) => c.put(e.request, copy));
        return r;
      }).catch(() => caches.match('/')))
    );
  }
});
