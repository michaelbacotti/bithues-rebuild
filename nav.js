// nav.js — Bithues shared navigation
(function () {
  var nav = document.getElementById('site-nav');
  if (nav) {
    nav.innerHTML = [
      '<nav class="nav">',
      '  <div class="nav-inner">',
      '    <a href="/" class="nav-logo">Bithues</a>',
      '    <div class="nav-links">',
      '      <a href="/reviews.html" class="nav-link">Reviews</a>',
      '      <a href="/articles.html" class="nav-link">Articles</a>',
      '      <a href="/stories.html" class="nav-link">Stories</a>',
      '      <a href="/about.html" class="nav-link">About</a>',
      '    </div>',
      '  </div>',
      '</nav>'
    ].join('\n');
  }
})();