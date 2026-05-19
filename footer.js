// footer.js — Bithues shared footer
(function () {
  var footer = document.getElementById('site-footer');
  if (footer) {
    footer.innerHTML = [
      '<footer class="footer">',
      '  <div class="footer-inner">',
      '    <a href="/" class="footer-brand">Bithues</a>',
      '    <nav class="footer-nav">',
      '      <a href="/which-book-should-i-read-next/">Find Books</a>',
      '      <a href="/reviews">Reviews</a>',
      '      <a href="/articles">Articles</a>',
      '      <a href="/stories">Stories</a>',
      '      <a href="/about">About</a>',
      '      <a href="/contact">Contact</a>',
      '      <a href="/terms">Terms</a>',
      '      <a href="/privacy">Privacy</a>',
      '    </nav>',
      '    <p class="footer-copy">&copy; ' + new Date().getFullYear() + ' Bithues. All rights reserved.</p>',
      '  </div>',
      '</footer>'
    ].join('\n');
  }
})();
