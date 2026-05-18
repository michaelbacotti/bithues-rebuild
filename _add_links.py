#!/usr/bin/env python3
"""Add internal links to Bithues articles before share-bar div."""
import os
import re
import sys

ARTICLES_DIR = 'articles'
REVIEWS_DIR = 'reviews'

# Structured link block template
LINK_BLOCK_TEMPLATE = '''<div style="margin:2.5rem 0;padding:1.5rem;background:var(--surface);border-radius:var(--radius);border:1px solid var(--border);">
<h3 style="font-size:1rem;font-weight:600;margin-bottom:1rem;font-family:var(--font-heading,Georgia,serif);">Continue Reading</h3>
<div style="display:flex;flex-wrap:wrap;gap:0.75rem;">
{links}
</div>
</div>
'''

def make_link_block(links_html):
    return LINK_BLOCK_TEMPLATE.format(links=links_html)

def make_pill_links(links):
    """Convert list of (text, href) to pill HTML."""
    pills = []
    for text, href in links:
        pills.append(f'<a href="{href}" style="display:inline-block;padding:6px 14px;background:#f5f0e8;color:#3a2f1e;border:1px solid #3a2f1e;border-radius:3px;text-decoration:none;font-size:.85rem;">{text}</a>')
    return '\n'.join(pills)

def get_article_title(path):
    """Extract a readable title from filename."""
    basename = os.path.basename(path)
    name = basename.replace('.html', '')
    # Convert slug to title
    name = name.replace('-', ' ').replace('.html', '')
    return name.title()

# ─── Link sets for different article topics ───────────────────────────

BOOKS_LIKE_LINKS = [
    ("Best Books for Book Clubs", "/articles/best-books-book-clubs.html"),
    ("Browse Fiction Reviews", "/reviews/"),
    ("Books Like The Midnight Library", "/articles/books-like-the-midnight-library.html"),
]

# Per-article custom links (topic-based)
ARTICLE_LINKS = {
    "books-like-anxious-people": [
        ("Best Books for Book Clubs", "/articles/best-books-book-clubs.html"),
        ("Books Like The Midnight Library", "/articles/books-like-the-midnight-library.html"),
        ("Books Like Dark Matter", "/articles/books-like-dark-matter.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "books-like-atomic-habits": [
        ("Best Business Books 2026", "/articles/best-business-books-2026.html"),
        ("Best Books Discipline & Willpower", "/articles/best-books-discipline-willpower.html"),
        ("Books Like Dark Matter", "/articles/books-like-dark-matter.html"),
        ("Business & Leadership Guide", "/articles/business-leadership-guide.html"),
    ],
    "books-like-dark-matter": [
        ("Best Sci-Fi Books for Beginners", "/articles/books-like-sci-fi-beginners.html"),
        ("Books Like Project Hail Mary", "/articles/books-like-project-hail-mary.html"),
        ("Best Books for Entrepreneurs", "/articles/best-books-for-entrepreneurs.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "books-like-dune": [
        ("Complete Fantasy Encyclopedia", "/articles/complete-fantasy-encyclopedia.html"),
        ("Best Books for Book Clubs", "/articles/best-books-book-clubs.html"),
        ("Reading Order Guide: High Fantasy", "/articles/reading-order-guide-high-fantasy.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "books-like-enders-game": [
        ("Best Sci-Fi Books for Beginners", "/articles/books-like-sci-fi-beginners.html"),
        ("Books Like Hyperion", "/articles/books-like-hyperion.html"),
        ("Books Like The Martian", "/articles/books-like-the-martian.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "books-like-hyperion": [
        ("Best Sci-Fi Books for Beginners", "/articles/books-like-sci-fi-beginners.html"),
        ("Books Like Ender's Game", "/articles/books-like-enders-game.html"),
        ("Books Like Project Hail Mary", "/articles/books-like-project-hail-mary.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "books-like-physics-of-time": [
        ("Quantum Physics for Beginners", "/articles/quantum-physics-beginners.html"),
        ("Best Sci-Fi Books for Beginners", "/articles/books-like-sci-fi-beginners.html"),
        ("Quantum Physics Beginners Guide", "/articles/quantum-physics-beginners-guide.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "books-like-project-hail-mary": [
        ("Best Sci-Fi Books for Beginners", "/articles/books-like-sci-fi-beginners.html"),
        ("Books Like The Martian", "/articles/books-like-the-martian.html"),
        ("Books Like Hyperion", "/articles/books-like-hyperion.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "books-like-sci-fi-beginners": [
        ("Books Like The Martian", "/articles/books-like-the-martian.html"),
        ("Books Like Ender's Game", "/articles/books-like-enders-game.html"),
        ("Books Like Dark Matter", "/articles/books-like-dark-matter.html"),
        ("Complete Fantasy Encyclopedia", "/articles/complete-fantasy-encyclopedia.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "books-like-the-martian": [
        ("Best Sci-Fi Books for Beginners", "/articles/books-like-sci-fi-beginners.html"),
        ("Books Like Project Hail Mary", "/articles/books-like-project-hail-mary.html"),
        ("Books Like Hyperion", "/articles/books-like-hyperion.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "books-like-the-midnight-library": [
        ("Best Books for Book Clubs", "/articles/best-books-book-clubs.html"),
        ("Books Like Anxious People", "/articles/books-like-anxious-people.html"),
        ("Best Books for Spring 2026", "/articles/best-books-spring-2026.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "books-like-the-name-of-the-wind": [
        ("Complete Fantasy Encyclopedia", "/articles/complete-fantasy-encyclopedia.html"),
        ("Reading Order Guide: High Fantasy", "/articles/reading-order-guide-high-fantasy.html"),
        ("Fantasy for Beginners", "/articles/fantasy-for-beginners.html"),
        ("Best Books for Book Clubs", "/articles/best-books-book-clubs.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
}

# Group B - Best Books/List articles
BEST_BOOKS_LINKS = {
    "best-books-book-clubs": [
        ("Best Books for Spring 2026", "/articles/best-books-spring-2026.html"),
        ("Best Books for Summer 2026", "/articles/best-books-summer-2026.html"),
        ("Best Historical Fiction for Beginners", "/articles/best-historical-fiction-beginners.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "best-books-discipline-willpower": [
        ("Best Business Books 2026", "/articles/best-business-books-2026.html"),
        ("Best Books for Entrepreneurs", "/articles/best-books-for-entrepreneurs.html"),
        ("Business & Leadership Guide", "/articles/business-leadership-guide.html"),
        ("Browse Non-Fiction Reviews", "/reviews/"),
    ],
    "best-books-for-entrepreneurs": [
        ("Best Business Books 2026", "/articles/best-business-books-2026.html"),
        ("Best Books Discipline & Willpower", "/articles/best-books-discipline-willpower.html"),
        ("Business & Leadership Guide", "/articles/business-leadership-guide.html"),
        ("Browse Non-Fiction Reviews", "/reviews/"),
    ],
    "best-books-retired-military": [
        ("Business & Leadership Guide", "/articles/business-leadership-guide.html"),
        ("Best Business Books 2026", "/articles/best-business-books-2026.html"),
        ("Best Memoirs & Biography Guide", "/articles/memoir-biography-guide.html"),
        ("Browse Non-Fiction Reviews", "/reviews/"),
    ],
    "best-books-spring-2026": [
        ("Best Books for Summer 2026", "/articles/best-books-summer-2026.html"),
        ("Best Books for Book Clubs", "/articles/best-books-book-clubs.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "best-books-summer-2026": [
        ("Best Books for Spring 2026", "/articles/best-books-spring-2026.html"),
        ("Best Books for Book Clubs", "/articles/best-books-book-clubs.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "best-business-books-2026": [
        ("Best Books for Entrepreneurs", "/articles/best-books-for-entrepreneurs.html"),
        ("Business & Leadership Guide", "/articles/business-leadership-guide.html"),
        ("Best Books Discipline & Willpower", "/articles/best-books-discipline-willpower.html"),
        ("Browse Non-Fiction Reviews", "/reviews/"),
    ],
    "best-first-time-authors": [
        ("Best Books for Book Clubs", "/articles/best-books-book-clubs.html"),
        ("Best Historical Fiction for Beginners", "/articles/best-historical-fiction-beginners.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "best-historical-fiction-beginners": [
        ("Best Books for Book Clubs", "/articles/best-books-book-clubs.html"),
        ("Best First-Time Authors", "/articles/best-first-time-authors.html"),
        ("Memoir & Biography Guide", "/articles/memoir-biography-guide.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "fantasy-for-beginners": [
        ("Complete Fantasy Encyclopedia", "/articles/complete-fantasy-encyclopedia.html"),
        ("Reading Order Guide: High Fantasy", "/articles/reading-order-guide-high-fantasy.html"),
        ("Books Like The Name of the Wind", "/articles/books-like-the-name-of-the-wind.html"),
        ("Books Like Dune", "/articles/books-like-dune.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "horror-for-beginners": [
        ("Browse Fiction Reviews", "/reviews/"),
        ("Best Books for Book Clubs", "/articles/best-books-book-clubs.html"),
        ("Fantasy for Beginners", "/articles/fantasy-for-beginners.html"),
    ],
    "romance-for-beginners": [
        ("Best Books for Book Clubs", "/articles/best-books-book-clubs.html"),
        ("Browse Fiction Reviews", "/reviews/"),
        ("Fantasy for Beginners", "/articles/fantasy-for-beginners.html"),
    ],
}

# Group C - Genre guides
GENRE_GUIDE_LINKS = {
    "reading-order-guide-high-fantasy": [
        ("Complete Fantasy Encyclopedia", "/articles/complete-fantasy-encyclopedia.html"),
        ("Fantasy for Beginners", "/articles/fantasy-for-beginners.html"),
        ("Books Like The Name of the Wind", "/articles/books-like-the-name-of-the-wind.html"),
        ("Books Like Dune", "/articles/books-like-dune.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "complete-fantasy-encyclopedia": [
        ("Fantasy for Beginners", "/articles/fantasy-for-beginners.html"),
        ("Reading Order Guide: High Fantasy", "/articles/reading-order-guide-high-fantasy.html"),
        ("Horror for Beginners", "/articles/horror-for-beginners.html"),
        ("Romance for Beginners", "/articles/romance-for-beginners.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "business-leadership-guide": [
        ("Best Business Books 2026", "/articles/best-business-books-2026.html"),
        ("Best Books for Entrepreneurs", "/articles/best-books-for-entrepreneurs.html"),
        ("Best Books Discipline & Willpower", "/articles/best-books-discipline-willpower.html"),
        ("Best Memoirs & Biography Guide", "/articles/memoir-biography-guide.html"),
        ("Browse Non-Fiction Reviews", "/reviews/"),
    ],
    "memoir-biography-guide": [
        ("Best Books for Retired Military", "/articles/best-books-retired-military.html"),
        ("Business & Leadership Guide", "/articles/business-leadership-guide.html"),
        ("Best Memoirs & Biography Guide", "/articles/memoir-biography-guide.html"),
        ("Browse Non-Fiction Reviews", "/reviews/"),
    ],
    "kids-reading-guide": [
        ("Berenstain Bears Classic Children's Books", "/articles/berenstain-bears-classic-children's-books.html"),
        ("Eric Carle Classic Children's Books", "/articles/eric-carle-classic-children's-books.html"),
        ("Frog and Toad Classic Children's Books", "/articles/frog-and-toad-classic-children's-books.html"),
        ("Meet Indie Authors", "/articles/meet-indie-authors.html"),
    ],
    "quantum-physics-beginners": [
        ("Quantum Physics Beginners Guide", "/articles/quantum-physics-beginners-guide.html"),
        ("Books Like Physics of Time", "/articles/books-like-physics-of-time.html"),
        ("Best Sci-Fi Books for Beginners", "/articles/books-like-sci-fi-beginners.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "quantum-physics-beginners-guide": [
        ("Quantum Physics for Beginners", "/articles/quantum-physics-beginners.html"),
        ("Books Like Physics of Time", "/articles/books-like-physics-of-time.html"),
        ("Best Sci-Fi Books for Beginners", "/articles/books-like-sci-fi-beginners.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "hopepunk-beginners-guide": [
        ("Best Books for Book Clubs", "/articles/best-books-book-clubs.html"),
        ("Best Books for Spring 2026", "/articles/best-books-spring-2026.html"),
        ("Best Sci-Fi Books for Beginners", "/articles/books-like-sci-fi-beginners.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
    "hopep Fiction": [
        ("Hopepunk Beginners Guide", "/articles/hopepunk-beginners-guide.html"),
        ("Best Sci-Fi Books for Beginners", "/articles/books-like-sci-fi-beginners.html"),
        ("Best Books for Spring 2026", "/articles/best-books-spring-2026.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
}

# Group D - Children's books
CHILDREN_LINKS = {
    "berenstain-bears-classic-children's-books": [
        ("Eric Carle Classic Children's Books", "/articles/eric-carle-classic-children's-books.html"),
        ("Frog and Toad Classic Children's Books", "/articles/frog-and-toad-classic-children's-books.html"),
        ("Kids Reading Guide", "/articles/kids-reading-guide.html"),
        ("Meet Indie Authors", "/articles/meet-indie-authors.html"),
    ],
    "eric-carle-classic-children's-books": [
        ("Berenstain Bears Classic Children's Books", "/articles/berenstain-bears-classic-children's-books.html"),
        ("Frog and Toad Classic Children's Books", "/articles/frog-and-toad-classic-children's-books.html"),
        ("Kids Reading Guide", "/articles/kids-reading-guide.html"),
        ("Meet Indie Authors", "/articles/meet-indie-authors.html"),
    ],
    "frog-and-toad-classic-children's-books": [
        ("Berenstain Bears Classic Children's Books", "/articles/berenstain-bears-classic-children's-books.html"),
        ("Eric Carle Classic Children's Books", "/articles/eric-carle-classic-children's-books.html"),
        ("Kids Reading Guide", "/articles/kids-reading-guide.html"),
        ("Meet Indie Authors", "/articles/meet-indie-authors.html"),
    ],
    "meet-indie-authors": [
        ("Kids Reading Guide", "/articles/kids-reading-guide.html"),
        ("Berenstain Bears Classic Children's Books", "/articles/berenstain-bears-classic-children's-books.html"),
        ("Eric Carle Classic Children's Books", "/articles/eric-carle-classic-children's-books.html"),
        ("Browse Fiction Reviews", "/reviews/"),
    ],
}

# Fallback generic links
GENERIC_ARTICLE_LINKS = [
    ("Best Books for Book Clubs", "/articles/best-books-book-clubs.html"),
    ("Browse Fiction Reviews", "/reviews/"),
    ("Fantasy for Beginners", "/articles/fantasy-for-beginners.html"),
    ("Horror for Beginners", "/articles/horror-for-beginners.html"),
]

def get_links_for_article(filepath):
    """Get the appropriate links for an article based on its filename."""
    basename = os.path.basename(filepath)
    
    # Check all custom link sets
    for link_map in [ARTICLE_LINKS, BEST_BOOKS_LINKS, GENRE_GUIDE_LINKS, CHILDREN_LINKS]:
        for key, links in link_map.items():
            if key in basename:
                return links
    
    return GENERIC_ARTICLE_LINKS

def remove_old_related_guides(content):
    """Remove old 'Related Guides' text if present."""
    # Pattern: text at end of article paragraph before share-bar
    patterns = [
        # Ending pattern for paginated "Books Like" articles
        r'Related Guides\s*Best Books for Book Clubs\s*Browse Fiction Reviews\s*Books Like [A-Za-z ]+\s*(?=</p>\s*<div class="share-bar">)',
        # Generic Related Guides pattern
        r'Related Guides\s*[^<]*(?=<div class="share-bar">)',
    ]
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    return content

def add_links_before_sharebar(content, filepath):
    """Add the structured links block before share-bar div."""
    links = get_links_for_article(filepath)
    link_block = make_link_block(make_pill_links(links))
    
    # Check if already has related-links div
    if 'class="related-links"' in content or 'id="related-links"' in content:
        return content, False
    
    # Remove old Related Guides text first
    content = remove_old_related_guides(content)
    
    # Pattern: before <div class="share-bar">
    pattern = r'(<div class="share-bar">)'
    if re.search(pattern, content):
        content = re.sub(pattern, link_block + r'\n  \1', content, count=1)
        return content, True
    
    # Fallback: before <div id="site-footer">
    pattern2 = r'(<div id="site-footer">)'
    if re.search(pattern2, content):
        content = re.sub(pattern2, link_block + r'\n  \1', content, count=1)
        return content, True
    
    return content, False

def process_file(filepath):
    """Process a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, modified = add_links_before_sharebar(content, filepath)
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    files = sys.argv[1:] if len(sys.argv) > 1 else []
    if not files:
        print("Usage: python add_links.py file1.html file2.html ...")
        return
    
    modified_count = 0
    for f in files:
        if process_file(f):
            modified_count += 1
            print(f"Modified: {f}")
        else:
            print(f"No change: {f}")
    
    print(f"\nTotal modified: {modified_count}/{len(files)}")

if __name__ == '__main__':
    main()