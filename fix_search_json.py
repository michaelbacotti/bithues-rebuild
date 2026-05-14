import json
from collections import defaultdict

with open('search.json', 'r') as f:
    data = json.load(f)

# Normalize category function
def normalize_category(item):
    cat = item.get('category', '')
    t = item.get('type', '')

    # Normalize known bad values
    if cat in ('article', 'review', 'storie', 'story'):
        if t == 'review': return 'Book Review'
        if t == 'story': return 'Short Story'
        if cat == 'article': return 'Article'
        if cat == 'review': return 'Book Review'
        if cat in ('storie', 'story'): return 'Short Story'

    if cat == 'Book Review' and t == 'review': return 'Book Review'
    if cat == 'Article' and t == 'article': return 'Article'
    if cat == 'Short Story' and t == 'story': return 'Short Story'

    # If category is missing or bad, infer from type or url
    if not cat or cat in ('article', 'review', 'storie', 'story', 'MISSING'):
        if t == 'review' or '/reviews/' in item.get('url',''): return 'Book Review'
        if t == 'story' or '/stories/' in item.get('url',''): return 'Short Story'
        if t == 'article' or '/articles/' in item.get('url',''): return 'Article'
        return 'Article'

    return cat

# Step 1: Normalize categories
for item in data:
    item['category'] = normalize_category(item)

# Step 2: Deduplicate by title — keep entry with:
# 1. Most complete data (has summary > excerpt > empty)
# 2. Prefer /reviews/ URLs for Book Reviews, /articles/ for Articles, /stories/ for Short Stories
def completeness_score(item):
    score = 0
    if item.get('summary'): score += 3
    if item.get('excerpt'): score += 1
    url = item.get('url','')
    cat = item.get('category','')
    if cat == 'Book Review' and '/reviews/' in url: score += 2
    if cat == 'Article' and '/articles/' in url: score += 2
    if cat == 'Short Story' and '/stories/' in url: score += 2
    return score

seen = {}  # title -> list of items
for item in data:
    title = item.get('title','')
    if title not in seen:
        seen[title] = []
    seen[title].append(item)

deduped = []
for title, items in seen.items():
    if len(items) == 1:
        deduped.append(items[0])
    else:
        # Keep the best one
        items.sort(key=completeness_score, reverse=True)
        deduped.append(items[0])

print(f'Before: {len(data)} entries, After: {len(deduped)} entries')
print(f'Duplicates removed: {len(data) - len(deduped)}')

# Show what was kept for duplicates
for title, items in seen.items():
    if len(items) > 1:
        items.sort(key=completeness_score, reverse=True)
        print(f'  DUPLICATE: "{title}" -> keeping {items[0]["url"]} (score={completeness_score(items[0])})')

with open('search.json', 'w') as f:
    json.dump(deduped, f, indent=2, ensure_ascii=False)

print('Done. search.json updated.')