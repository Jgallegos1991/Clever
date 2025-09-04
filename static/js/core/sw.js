// Minimal service worker for Clever
// This avoids 404s and provides a hook for future offline caching.
// It does not cache anything aggressive by default.

self.addEventListener('install', (event) => {
  // Activate immediately on install
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  // Take control of uncontrolled clients (pages)
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
  // Passthrough for now; no caching to ensure strict offline correctness
  return;
});
