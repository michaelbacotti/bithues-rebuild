(function () {
  var params = new URLSearchParams(window.location.search);
  var q = params.get('q') || '';
  var resultsContainer = document.querySelector('.search-page-results');
  if (!q) {
    resultsContainer.innerHTML = '<p>Enter a search term above.</p>';
    return;
  }
  var input = document.querySelector('.search-page-input');
  if (input) input.value = q;

  fetch('/search.json').then(function (r) { return r.json(); }).then(function (data) {
    var results = data.filter(function (item) {
      return item.title.toLowerCase().includes(q.toLowerCase()) ||
             item.category.toLowerCase().includes(q.toLowerCase()) ||
             item.summary.toLowerCase().includes(q.toLowerCase());
    });
    if (results.length === 0) {
      resultsContainer.innerHTML = '<p>No results found for "' + q + '".</p>';
      return;
    }
    resultsContainer.innerHTML = '<ul class="article-list">' + results.map(function (r) {
      var tagClass = 'tag--review';
      if (r.category === 'Article') tagClass = 'tag--article';
      else if (r.category === 'Short Story') tagClass = 'tag--story';
      return '<li class="card"><p class="card-meta-top"><span class="tag ' + tagClass + '">' + r.category + '</span></p>' +
             '<h2 class="card-title"><a href="' + r.url + '">' + r.title + '</a></h2>' +
             '<p class="card-excerpt">' + r.summary + '</p></li>';
    }).join('') + '</ul>';
  }).catch(function () {
    resultsContainer.innerHTML = '<p>Error loading search.</p>';
  });
})();