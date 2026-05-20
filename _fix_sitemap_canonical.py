#!/usr/bin/env python3
"""Fix sitemap canonical mismatch: sitemap uses https://bithues.com/ but pages use https://www.bithues.com/"""

import re

sitemap_path = "/Users/mike/.openclaw/workspace-bacottibot/websites/bithues-rebuild-2026-05-13/sitemap.xml"

with open(sitemap_path, "r") as f:
    content = f.read()

# Fix 1: Replace bithues.com with www.bithues.com everywhere
content = content.replace("https://bithues.com/", "https://www.bithues.com/")

# Fix 2: Remove the duplicate /index entry (the sitemap should NOT list both / and /index)
content = re.sub(r'\s*<url>\s*<loc>https://www\.bithues\.com/index</loc>.*?</url>\s*', '\n', content, flags=re.DOTALL)

with open(sitemap_path, "w") as f:
    f.write(content)

print("Sitemap updated")

# Show what we changed
with open(sitemap_path, "r") as f:
    print(f.read())