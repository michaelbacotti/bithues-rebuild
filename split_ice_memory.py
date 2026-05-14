#!/usr/bin/env python3
import re

with open('stories/ice-memory.html', 'r') as f:
    content = f.read()

# Find the giant <p> block
# Split on these phrase boundaries to create new paragraphs:
break_phrases = [
    "The ice remembered things.",
    "listening to ice remember.",
    "local time.",
    "From very far below.",
    "Yuki sat very still.",
    "She recorded her response.",
    "The answer was yes.",
    "Yuki slept."
]

# Find the giant <p>...</p> block
p_match = re.search(r'<p>(.*?)</p>', content, re.DOTALL)
if p_match:
    text = p_match.group(1)
    
    # Split at break phrases
    parts = []
    last_pos = 0
    for phrase in break_phrases:
        idx = text.find(phrase)
        if idx != -1:
            end_idx = idx + len(phrase)
            if end_idx > last_pos:
                parts.append(text[last_pos:end_idx].strip())
                last_pos = end_idx
    if last_pos < len(text):
        parts.append(text[last_pos:].strip())
    
    # Build new paragraphs
    new_paras = ['<p>' + p.strip() + '</p>' for p in parts if p.strip()]
    new_body = '\n\n'.join(new_paras)
    
    # Replace old <p>...</p> with new split version
    content = re.sub(r'<p>.*?</p>', new_body, content, flags=re.DOTALL)
    
    with open('stories/ice-memory.html', 'w') as f:
        f.write(content)
    print(f"Split into {len(parts)} paragraphs")
else:
    print("No <p> block found")