// nav.js — Bithues shared navigation
(function () {
  var nav = document.getElementById('site-nav');
  if (nav) {
    nav.innerHTML = [
      '<nav class="nav">',
      '  <div class="nav-inner">',
      '    <a href="/" class="nav-logo">Bithues</a>',
      '    <div class="nav-links">',
      '      <a href="/which-book-should-i-read-next/" class="nav-link">Find Books</a>',
      '      <a href="/reviews.html" class="nav-link">Reviews</a>',
      '      <a href="/articles.html" class="nav-link">Articles</a>',
      '      <a href="/stories.html" class="nav-link">Stories</a>',
      '      <a href="/about.html" class="nav-link">About</a>',
      '    </div>',
      '    <div class="nav-search">',
      '      <button class="search-toggle" aria-label="Search">',
      '        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
      '      </button>',
      '      <div class="search-panel">',
      '        <input type="text" class="search-input" placeholder="Search..." autocomplete="off">',
      '        <div class="search-results"></div>',
      '      </div>',
      '    </div>',
      '  </div>',
      '</nav>'
    ].join('\n');
  }

  // ── Search ───────────────────────────────────────────────
  var searchToggle = document.querySelector('.search-toggle');
  var searchPanel = document.querySelector('.search-panel');
  var searchInput = document.querySelector('.search-input');
  var searchResults = document.querySelector('.search-results');
  var searchIndex = null;

  if (searchToggle && searchPanel) {
    searchToggle.addEventListener('click', function () {
      searchPanel.classList.add('open');
      searchInput.focus();
    });

    searchInput.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        searchPanel.classList.remove('open');
        searchInput.value = '';
        searchResults.innerHTML = '';
      }
      if (e.key === 'Enter') {
        var q = searchInput.value.trim();
        if (q.length > 0) {
          window.location.href = '/search.html?q=' + encodeURIComponent(q);
        }
      }
    });

    searchInput.addEventListener('input', function () {
      var q = searchInput.value.trim().toLowerCase();
      if (q.length < 2) {
        searchResults.innerHTML = '';
        return;
      }
      if (!searchIndex) {
        fetch('/search.json').then(function (r) { return r.json(); }).then(function (data) {
          searchIndex = data;
          performSearch(q);
        });
      } else {
        performSearch(q);
      }
    });

    function performSearch(q) {
      var results = searchIndex.filter(function (item) {
        return item.title.toLowerCase().includes(q) ||
               item.category.toLowerCase().includes(q) ||
               item.summary.toLowerCase().includes(q);
      }).slice(0, 6);

      if (results.length === 0) {
        searchResults.innerHTML = '<div class="search-no-results">No results found.</div>';
        return;
      }

      searchResults.innerHTML = results.map(function (r) {
        return '<a href="' + r.url + '" class="search-result-item">' +
          '<span class="result-title">' + r.title + '</span>' +
          '<span class="result-category">' + r.category + '</span>' +
          '<span class="result-summary">' + r.summary + '</span>' +
          '</a>';
      }).join('');
    }

    document.addEventListener('click', function (e) {
      if (!searchPanel.contains(e.target) && !searchToggle.contains(e.target)) {
        searchPanel.classList.remove('open');
      }
    });
  }
})();