#!/usr/bin/env node
/**
 * Transform all Bithues story HTML files to add segmented reader mode.
 */

const fs = require('fs');
const path = require('path');

const STORIES_DIR = path.join(__dirname, 'stories');

const SEGMENTED_CSS = `
/* ─── Segmented Reader Mode ─────────────────────────── */
.story-page-segment{display:block}
.story-page-segment[style*="display:none"]{display:none!important}

.story-page-nav{display:flex;justify-content:space-between;align-items:center;padding:20px 0;border-top:1px solid var(--color-border-light);margin-top:32px}
.story-page-indicator{font-size:13px;color:var(--color-text-muted);font-family:var(--font-sans)}
.story-page-buttons{display:flex;gap:10px}
.story-nav-btn{background:none;border:1px solid var(--color-border);border-radius:4px;padding:8px 16px;font-size:13px;font-weight:600;color:var(--color-text-muted);cursor:pointer;transition:all .2s}
.story-nav-btn:hover:not(:disabled){border-color:var(--color-accent);color:var(--color-accent)}
.story-nav-btn:disabled{opacity:.35;cursor:not-allowed}

.story-resume-toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:var(--color-text);color:var(--color-bg);font-size:13px;font-family:var(--font-sans);padding:10px 20px;border-radius:6px;opacity:0;transition:opacity .3s;z-index:200;pointer-events:none}
.story-resume-toast.show{opacity:1}

.no-js .story-page-segment{display:block!important}
`;

// JS — uses history.replaceState (not location.replace) to avoid page reload
const SEGMENTED_JS = `
<script>
// Segmented story reader
(function(){
  var readerBody = document.querySelector('.reader-body');
  if (!readerBody) return;
  var allPs = Array.from(readerBody.querySelectorAll('p'));
  if (allPs.length === 0) return;

  var chunkSize = 3;
  var pages = [];
  for (var i = 0; i < allPs.length; i += chunkSize) {
    pages.push(allPs.slice(i, i + chunkSize));
  }
  var totalPages = pages.length;

  // Move all p tags into segmented divs
  allPs.forEach(function(p){ p.parentNode.removeChild(p); });
  pages.forEach(function(chunk, idx) {
    var div = document.createElement('div');
    div.className = 'story-page-segment';
    div.setAttribute('data-page', idx + 1);
    div.id = 'page-' + (idx + 1);
    if (idx > 0) div.style.display = 'none';
    chunk.forEach(function(p){ div.appendChild(p); });
    readerBody.appendChild(div);
  });

  // Nav bar
  var nav = document.createElement('div');
  nav.className = 'story-page-nav';
  nav.innerHTML =
    '<span class="story-page-indicator">Page <span id="current-page-num">1</span> of <span id="total-pages-num">' + totalPages + '</span></span>' +
    '<div class="story-page-buttons">' +
      '<button id="prev-page-btn" class="story-nav-btn" disabled>Previous</button>' +
      '<button id="next-page-btn" class="story-nav-btn">Next</button>' +
    '</div>';
  readerBody.parentNode.insertBefore(nav, readerBody.nextSibling);

  // Toast
  var toast = document.createElement('div');
  toast.className = 'story-resume-toast';
  toast.id = 'story-resume-toast';
  document.body.appendChild(toast);

  var currentPage = 1;
  var slug = window.location.pathname.split('/').pop().replace('.html','');

  function showPage(n) {
    if (n < 1 || n > totalPages) return;
    document.querySelectorAll('.story-page-segment').forEach(function(el){ el.style.display = 'none'; });
    var target = document.getElementById('page-' + n);
    if (target) target.style.display = 'block';
    var curEl = document.getElementById('current-page-num');
    if (curEl) curEl.textContent = n;
    var prevBtn = document.getElementById('prev-page-btn');
    var nextBtn = document.getElementById('next-page-btn');
    if (prevBtn) prevBtn.disabled = (n === 1);
    if (nextBtn) nextBtn.disabled = (n === totalPages);
    currentPage = n;
    if (history.replaceState) history.replaceState(null, '', '#page-' + n);
    try { localStorage.setItem('bithues-story-' + slug, n); } catch(e){}
    var reader = document.getElementById('reader-container');
    if (reader) reader.scrollIntoView({behavior:'smooth', block:'start'});
  }

  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(function(){ toast.classList.remove('show'); }, 3000);
  }

  document.getElementById('next-page-btn').addEventListener('click', function(){ showPage(currentPage + 1); });
  document.getElementById('prev-page-btn').addEventListener('click', function(){ showPage(currentPage - 1); });

  document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); showPage(currentPage + 1); }
    if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); showPage(currentPage - 1); }
  });

  (function(){
    var savedPage = 1;
    try { savedPage = parseInt(localStorage.getItem('bithues-story-' + slug)) || 1; } catch(e){}
    var hashM = window.location.hash.match(/^#page-(\d+)$/);
    var startPage = hashM ? parseInt(hashM[1]) : savedPage;
    if (startPage > totalPages) startPage = 1;
    if (startPage > 1) { showPage(startPage); showToast('Resume from page ' + startPage); }
    else { showPage(1); }
  })();

  // Per-page scroll progress bar
  var bar = document.getElementById('story-progress-bar');
  var container = document.getElementById('reader-container');
  if (bar && container) {
    function updateProgress() {
      var rect = container.getBoundingClientRect();
      var total = container.offsetHeight - window.innerHeight;
      var scrolled = Math.max(0, -rect.top);
      var pct = total > 0 ? Math.min(100, (scrolled / total) * 100) : 0;
      bar.style.width = pct + '%';
    }
    window.addEventListener('scroll', updateProgress, {passive:true});
    updateProgress();
  }
})();
<\/script>
`;

function transformStory(html) {
  // 1. Inject CSS before </head>
  if (!html.includes('/* ─── Segmented Reader Mode')) {
    html = html.replace('</head>', SEGMENTED_CSS + '\n</head>');
  }

  // 2. Remove old inline script blocks (progress bar + bookmark)
  // Match any <script> block containing these patterns:
  html = html.replace(
    /<script>\s*\/\/ Progress bar[\s\S]*?<\/script>\s*/g,
    ''
  );
  html = html.replace(
    /<script>\s*\(adsbygoogle[\s\S]*?<\/script>\s*/g,
    ''
  );
  // Also remove the standalone (adsbygoogle = ...) push call
  html = html.replace(
    /<script>\s*\(adsbygoogle\s*=\s*window\.adsbygoogle[\s\S]*?<\/script>\s*/g,
    ''
  );

  // 3. Remove the clipboard bookmark script by looking for the whole script block
  // The bookmark block starts with getElementById('reader-bookmark-btn')
  html = html.replace(
    /<script>[\s\S]*?getElementById\s*\(\s*['"]reader-bookmark-btn['"]\s*\)[\s\S]*?<\/script>\s*/g,
    ''
  );

  // 4. Append our segmented JS before </body>
  if (!html.includes('// Segmented story reader')) {
    html = html.replace('</body>', SEGMENTED_JS + '\n</body>');
  }

  return html;
}

function getStoryFiles(dir) {
  return fs.readdirSync(dir)
    .filter(f => f.endsWith('.html'))
    .filter(f => f !== 'index.html')
    .map(f => path.join(dir, f));
}

const files = getStoryFiles(STORIES_DIR);
console.log('Found', files.length, 'story files');
files.forEach(filePath => {
  const original = fs.readFileSync(filePath, 'utf8');
  const transformed = transformStory(original);
  fs.writeFileSync(filePath, transformed, 'utf8');
  console.log('✓ Transformed:', path.basename(filePath));
});
console.log('\nDone.');