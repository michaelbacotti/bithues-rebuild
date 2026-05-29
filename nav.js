// nav.js — Bithues
// Row 1: BITHUES wordmark + tagline + right nav links
// Row 2: section tab bar (Stories / About / Contact)
(function () {

 // ── Row 1: Top Black Bar ──────────────────────────────────
 var utility = document.getElementById('site-utility');
 if (utility) {
  utility.innerHTML = [
   '<nav class="top-bar">',
   ' <a href="/" class="top-wordmark">BITHUES</a>',
   ' <span class="top-tagline">Short fiction for curious readers</span>',
   ' <div class="top-links">',
   '  <a href="/about">About</a>',
   '  <a href="/contact">Contact</a>',
   ' </div>',
   '</nav>'
  ].join('\n');
 }

 // ── Row 2: Section Tab Bar ───────────────────────────────
 var nav = document.getElementById('site-nav');
 if (nav) {
  nav.innerHTML = [
   '<div class="tab-bar">',
   ' <div class="tab-bar-inner">',
   '  <a href="/articles.html">Articles</a>',
   '  <a href="/stories">Stories</a>',
   '  <a href="/reviews.html">Reviews</a>',
   '  <a href="/book-picker.html">Book Picker</a>',
   ' </div>',
   '</div>'
  ].join('\n');
 }

 // ── Active tab highlight ───────────────────────────────────
 var path = window.location.pathname;
 var tabs = document.querySelectorAll('.tab-bar a');
 tabs.forEach(function (tab) {
  var href = tab.getAttribute('href');
  if (href === '/' && path === '/') { tab.classList.add('active'); return; }
  if (href !== '/' && path.startsWith(href)) { tab.classList.add('active'); }
 });

})();