self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('pharmacy-system-v1').then((cache) => {
            return cache.addAll([
                '/',
                '/static/background.jpg',
                '/static/icon.png'
            ]);
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});