// footer.js — Bithues
(function () {
 var footer = document.getElementById('site-footer');
 if (footer) {
  footer.innerHTML = [
   '<div class="main-footer">',
   ' <div class="footer-grid">',
   '  <div class="footer-brand">',
   '   <h4>Bithues</h4>',
   '   <p>Short fiction for curious readers. Stories that explore what it means to be alive — in worlds familiar, strange, and somewhere in between.</p>',
   '  </div>',
   '  <div class="footer-nav">',
   '   <h5>Read</h5>',
   '   <ul>',
   '    <li><a href="/stories">All Stories</a></li>',
   '    <li><a href="/about">About</a></li>',
   '    <li><a href="/contact">Contact</a></li>',
   '   </ul>',
   '  </div>',
   '  <div class="footer-nav">',
   '   <h5>Legal</h5>',
   '   <ul>',
   '    <li><a href="/privacy">Privacy Policy</a></li>',
   '    <li><a href="/terms">Terms of Service</a></li>',
   '   </ul>',
   '  </div>',
   ' </div>',
   ' <div class="footer-bottom">',
   '  <p>&copy; 2026 Bithues. All rights reserved.</p>',
   '  <p>All stories are fiction. Any resemblance to actual events is coincidental.</p>',
   ' </div>',
   '</div>'
  ].join('\n');
 }
})();