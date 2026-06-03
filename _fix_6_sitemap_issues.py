#!/usr/bin/env python3
"""Fix sitemap: remove the 3 apostrophe entries (live canonical is correct),
   remove /articles/index, /reviews/index, and orphaned /reviews/21."""

import re

SITEMAP = "/Users/mike/.openclaw/workspace-bacottibot/projects/bithues/website/sitemap.xml"

with open(SITEMAP) as f:
    content = f.read()
original = content

# Remove the 3 apostrophe sitemap entries (live pages have correct canonicals)
for old_url in [
    "https://www.bithues.com/articles/berenstain-bears-classic-children's-books",
    "https://www.bithues.com/articles/eric-carle-classic-children's-books",
    "https://www.bithues.com/articles/frog-and-toad-classic-children's-books",
]:
    content = re.sub(
        r'\s*<url>\s*<loc>' + re.escape(old_url) + r'</loc>.*?</url>\s*',
        '\n', content, flags=re.DOTALL
    )

# Remove redundant /articles/index
content = re.sub(
    r'\s*<url>\s*<loc>https://www\.bithues\.com/articles/index</loc>.*?</url>\s*',
    '\n', content, flags=re.DOTALL
)

# Remove redundant /reviews/index
content = re.sub(
    r'\s*<url>\s*<loc>https://www\.bithues\.com/reviews/index</loc>.*?</url>\s*',
    '\n', content, flags=re.DOTALL
)

# Remove orphaned /reviews/21 (no actual page)
content = re.sub(
    r'\s*<url>\s*<loc>https://www\.bithues\.com/reviews/21</loc>.*?</url>\s*',
    '\n', content, flags=re.DOTALL
)

changed = content != original
with open(SITEMAP, "w") as f:
    f.write(content)

print("Sitemap updated." if changed else "No changes needed.")

# Commit + push
import subprocess
for cmd in [
    ["git", "add", "sitemap.xml"],
    ["git", "commit", "-m", "choresitemap: remove 3 apostrophe entries, /index redundancies, orphaned /reviews/21"],
    ["git", "push"],
]:
    r = subprocess.run(cmd, capture_output=True, text=True, cwd="/Users/mike/.openclaw/workspace-bacottibot/projects/bithues/website")
    if r.returncode != 0:
        print(f"CMD failed: {'cmd'}")
        print(r.stderr[:200])
    else:
        print(f"OK: {cmd[0]}")

print("Done.")
