const CACHE_NAME = 'fishing-note-v5';
const urlsToCache = [
  './',
  './index.html',
  './icon-512.png',
  './manifest.json'
];

// 설치 시 즉시 활성화
self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
  );
});

// 이전 캐시 삭제 후 즉시 클라이언트 제어
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      )
    ).then(() => self.clients.claim())
  );
});

// 네트워크 우선 전략: 네트워크 성공 시 캐시 갱신, 실패 시 캐시 반환
self.addEventListener('fetch', event => {
  // HTML 요청은 항상 네트워크 우선 (최신 버전 보장)
  if (event.request.mode === 'navigate' || event.request.url.endsWith('.html')) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          return response;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  // 정적 파일은 캐시 우선 (네트워크 실패 시 캐시)
  event.respondWith(
    caches.match(event.request).then(cached => {
      const networkFetch = fetch(event.request).then(response => {
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        return response;
      });
      return cached || networkFetch;
    })
  );
});
