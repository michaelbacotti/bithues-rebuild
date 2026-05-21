#!/usr/bin/env python3
"""Fix malformed style blocks in story HTML files.

Two cases:
1. Files with a <style> block + orphan CSS text outside it (between adsense script and </head>)
   → Remove orphan text, append it inside the existing </style> block
2. Files with NO <style> block at all (orphan CSS between adsense script and </head>)
   → Wrap the orphan CSS in <style> tags in the correct location (before </head>)
"""

import re
import os

STORY_DIR = "/Users/mike/.openclaw/workspace-bacottibot/websites/bithues-rebuild-2026-05-13/stories"

ORPHAN_CSS = """/* ─── Segmented Reader Mode ─────────────────────────── */
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
"""

def fix_file_has_style(filepath):
    """Files that have a </style> block — append orphan CSS inside it."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if '/* ─── Segmented Reader Mode' not in content:
        return False

    # Check if already inside a <style> block
    orphan_start = content.find('/* ─── Segmented Reader Mode')
    style_open_count = content[:orphan_start].count('<style>')
    style_close_count = content[:orphan_start].count('</style>')
    if style_open_count > style_close_count:
        return False  # already inside style block

    # Find end of orphan CSS (right before </head>)
    orphan_end = content.find('</head>', orphan_start)
    if orphan_end == -1:
        return False

    # Remove the orphan CSS text
    new_content = content[:orphan_start] + content[orphan_end:]

    # Insert CSS before </style>
    style_close_idx = new_content.find('</style>')
    if style_close_idx == -1:
        print(f"  ERROR: No </style> in {os.path.basename(filepath)}")
        return False

    new_content = new_content[:style_close_idx] + '\n\n' + ORPHAN_CSS + new_content[style_close_idx:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def fix_file_no_style(filepath):
    """Files with no <style> block at all — wrap orphan CSS in <style> tags."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if '/* ─── Segmented Reader Mode' not in content:
        return False

    # Check if already inside a <style> block
    orphan_start = content.find('/* ─── Segmented Reader Mode')
    style_open_count = content[:orphan_start].count('<style>')
    style_close_count = content[:orphan_start].count('</style>')
    if style_open_count > style_close_count:
        return False  # already inside style block

    # Find end of orphan CSS (right before </head>)
    orphan_end = content.find('</head>', orphan_start)
    if orphan_end == -1:
        return False

    orphan_css_text = content[orphan_start:orphan_end]

    # Replace orphan CSS text with <style> wrapped version, placed before </head>
    new_content = content[:orphan_start] + '<style>\n' + orphan_css_text + '</style>\n' + content[orphan_end:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def main():
    story_files = [
        "american-voices.html",
        "before-the-streetlights-came-on.html",
        "city-of-wonders.html",
        "ice-memory.html",
        "jaspers-flight.html",
        "mabi.html",
        "oliver-and-the-ocean.html",
        "rules-of-the-game.html",
        "the-borrowed-life.html",
        "the-cartographer-of-sea-serpents.html",
        "the-disclosure.html",
        "the-door-between-worlds.html",
        "the-echoes-return.html",
        "the-ember-song.html",
        "the-forbidden-library.html",
        "the-forgotten-minute.html",
        "the-harvest.html",
        "the-humble-mind.html",
        "the-last-arena.html",
        "the-last-garden.html",
        "the-last-gift.html",
        "the-last-signal.html",
        "the-last-song.html",
        "the-last-winter.html",
        "the-listen.html",
        "the-other-side.html",
        "the-question.html",
        "the-seed-library-at-the-end-of-may.html",
        "the-weight-of-summer-light.html",
        "they-walk-among-us.html",
    ]

    fixed = []
    for fname in story_files:
        path = os.path.join(STORY_DIR, fname)
        if not os.path.exists(path):
            print(f"Not found: {path}")
            continue

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        if '</style>' in content:
            result = fix_file_has_style(path)
        else:
            result = fix_file_no_style(path)

        if result:
            fixed.append(fname)
            print(f"Fixed: {fname}")

    print(f"\nTotal fixed: {len(fixed)}")

if __name__ == "__main__":
    main()