import os, re, json

root = "/Users/mike/.openclaw/workspace-bacottibot/websites/bithues-rebuild-2026-05-13"
dirs = ["articles", "reviews", "stories"]

for dir_name in dirs:
    dir_path = os.path.join(root, dir_name)
    if not os.path.exists(dir_path):
        continue
    for fname in os.listdir(dir_path):
        if not fname.endswith(".html"):
            continue
        fpath = os.path.join(dir_path, fname)
        with open(fpath) as f:
            content = f.read()
        
        # Skip if already has ld+json
        if 'application/ld+json' in content:
            continue
        
        # Determine page type - check for various tag/pill class patterns
        if "tag--article" in content or "tag-article" in content:
            page_type = "Article"
            section = "Articles"
            section_url = "https://www.bithues.com/articles"
        elif "tag--book-review" in content or "pill-book-review" in content or "tag--review" in content:
            page_type = "Book"
            section = "Reviews"
            section_url = "https://www.bithues.com/reviews"
        elif "tag--short-story" in content or "tag--story" in content:
            page_type = "ShortStory"
            section = "Stories"
            section_url = "https://www.bithues.com/stories"
        else:
            # Try to infer from URL/directory structure
            if dir_name == "articles":
                page_type = "Article"
                section = "Articles"
                section_url = "https://www.bithues.com/articles"
            elif dir_name == "reviews":
                page_type = "Book"
                section = "Reviews"
                section_url = "https://www.bithues.com/reviews"
            elif dir_name == "stories":
                page_type = "ShortStory"
                section = "Stories"
                section_url = "https://www.bithues.com/stories"
            else:
                print(f"Skipping (no page type): {dir_name}/{fname}")
                continue
        
        # Get page title
        title_match = re.search(r'<title>([^<]+)</title>', content)
        page_title = title_match.group(1) if title_match else ""
        
        # Get canonical URL
        canon_match = re.search(r'<link rel="canonical" href="([^"]+)"', content)
        canonical = canon_match.group(1) if canon_match else f"https://www.bithues.com/{dir_name}/{fname}"
        
        # Build BreadcrumbList JSON-LD
        breadcrumb = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.bithues.com/"},
                {"@type": "ListItem", "position": 2, "name": section, "item": section_url},
                {"@type": "ListItem", "position": 3, "name": page_title}
            ]
        }
        
        # Build page-type schema
        page_schema = {
            "@context": "https://schema.org",
            "@type": page_type,
            "headline": page_title,
            "url": canonical,
            "publisher": {"@type": "Organization", "name": "Bithues", "url": "https://www.bithues.com"}
        }
        
        if page_type == "Book":
            page_schema["name"] = page_title.replace(" — Review", "").replace("| Bithues", "").strip()
        
        breadcrumb_json = json.dumps(breadcrumb, indent=2)
        page_schema_json = json.dumps(page_schema, indent=2)
        
        # Build insertion string
        schema_block = f'<script type="application/ld+json">\n{breadcrumb_json}\n</script>\n<script type="application/ld+json">\n{page_schema_json}\n</script>\n'
        
        # Insert after canonical link
        if '<link rel="canonical"' in content:
            content = content.replace(
                '<link rel="canonical"',
                '<link rel="canonical"\n' + schema_block,
                1  # Only first occurrence
            )
            with open(fpath, "w") as f:
                f.write(content)
            print(f"Added schema to: {dir_name}/{fname}")

print("Done")