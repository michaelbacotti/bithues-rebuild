// footer.js — Bithues
(function () {
 var footer = document.getElementById('site-footer');
 if (!footer) { return; }
 footer.innerHTML =
  '<div class="main-footer">'
  + '<div class="footer-grid">'
  + '<div class="footer-brand">'
  + '<h4>Bithues</h4>'
  + '<p>Honest book reviews. Original short fiction. Stories that explore what it means to be alive — in worlds familiar, strange, and somewhere in between.</p>'
  + '</div>'
  + '<div class="footer-newsletter">'
  + '<h5>Newsletter</h5>'
  + '<p>Get new book reviews in your inbox. No spam, unsubscribe anytime.</p>'
  + '<form action="https://buttondown.email/api/emails/embed-subscribe/bithues" method="post" target="_blank" class="newsletter-form">'
  + '<!-- TODO: Replace buttondown.email embed URL with actual account after signup -->'
  + '<input type="email" name="email" placeholder="your@email.com" required>'
  + '<button type="submit">Subscribe</button>'
  + '</form>'
  + '</div>'
  + '<div class="footer-nav">'
  + '<h5>Read</h5>'
  + '<ul>'
  + '<li><a href="/stories">All Stories</a></li>'
  + '<li><a href="/about">About</a></li>'
  + '<li><a href="/contact">Contact</a></li>'
  + '</ul>'
  + '</div>'
  + '<div class="footer-nav">'
  + '<h5>Collections</h5>'
  + '<ul>'
  + '<li><a href="/collections/">All Collections</a></li>'
  + '<li><a href="/collections/little-mike-books/">Little Mike Picture Books</a></li>'
  + '<li><a href="/collections/otomi-saga/">The Otomí Saga</a></li>'
  + '<li><a href="/collections/physics-consciousness/">Physics, Consciousness &amp; Time</a></li>'
  + '<li><a href="/book-match/">Book Match</a></li>'
  + '</ul>'
  + '</div>'
  + '<div class="footer-nav">'
  + '<h5>Legal</h5>'
  + '<ul>'
  + '<li><a href="/privacy">Privacy Policy</a></li>'
  + '<li><a href="/terms">Terms of Service</a></li>'
  + '</ul>'
  + '</div>'
  + '</div>'
  + '<div class="footer-bottom">'
  + '<p>&copy; 2026 Bithues. All rights reserved.</p>'
  + '<p>All stories are fiction. Any resemblance to actual events is coincidental.</p>'
  + '<p>Articles and book reviews may include factual content. Book links are affiliate links — we may earn a small commission at no extra cost to you.</p>'
  + '</div>'
  + '</div>';
})();
// Chapter card expand/collapse
(function () {
  // Create backdrop element
  var backdrop = document.createElement('div');
  backdrop.className = 'chapter-card-body-backdrop';
  document.body.appendChild(backdrop);

  backdrop.addEventListener('click', function() {
    document.querySelectorAll('.chapter-card[open]').forEach(function(card) {
      card.removeAttribute('open');
      card.querySelector('.chapter-card-header').setAttribute('aria-expanded', 'false');
    });
    backdrop.classList.remove('active');
  });

  // Close on Escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      document.querySelectorAll('.chapter-card[open]').forEach(function(card) {
        card.removeAttribute('open');
        card.querySelector('.chapter-card-header').setAttribute('aria-expanded', 'false');
      });
      backdrop.classList.remove('active');
    }
  });

  document.querySelectorAll('.chapter-card-header').forEach(function(header) {
    header.addEventListener('click', function() {
      var card = header.closest('.chapter-card');
      var isOpen = card.hasAttribute('open');
      // Close all others first (accordion behavior)
      document.querySelectorAll('.chapter-card[open]').forEach(function(openCard) {
        if (openCard !== card) {
          openCard.removeAttribute('open');
          openCard.querySelector('.chapter-card-header').setAttribute('aria-expanded', 'false');
        }
      });
      // Toggle this one
      if (isOpen) {
        card.removeAttribute('open');
        header.setAttribute('aria-expanded', 'false');
        backdrop.classList.remove('active');
      } else {
        card.setAttribute('open', '');
        header.setAttribute('aria-expanded', 'true');
        backdrop.classList.add('active');
        card.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  });
})();
