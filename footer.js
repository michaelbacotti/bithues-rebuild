// footer.js — Bithues shared footer
(function () {
  var footer = document.getElementById('site-footer');
  if (footer) {
    footer.innerHTML = [
      '<footer class="footer">',
      '  <div class="footer-inner">',
      '    <a href="/" class="footer-brand">Bithues</a>',
      '    <nav class="footer-nav">',
      '      <a href="/reviews.html">Reviews</a>',
      '      <a href="/articles.html">Articles</a>',
      '      <a href="/stories.html">Stories</a>',
      '      <a href="/about.html">About</a>',
      '    </nav>',
      '    <p class="footer-copy">&copy; ' + new Date().getFullYear() + ' Bithues. All rights reserved.</p>',
      '  </div>',
      '</footer>'
    ].join('\n');
  }
})();