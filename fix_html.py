"""
Stack-based HTML div balancer.
Finds orphaned </div> tags and removes them to balance the document.
"""

from html.parser import HTMLParser
import re

class DivTracker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []   # (tag, position)
        self.orphans = [] # positions of orphaned </div>
        self.pos = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.stack.append(self.getpos())

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.stack:
                self.stack.pop()
            else:
                self.orphans.append(self.getpos())  # (line, col)

with open('index.html', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

tracker = DivTracker()
tracker.feed(content)

print(f"Remaining unclosed opening <div>s: {len(tracker.stack)}")
print(f"Orphaned </div>s: {len(tracker.orphans)}")

if tracker.orphans:
    print("\nOrphaned </div> locations (line, col):")
    for loc in tracker.orphans:
        print(f"  Line {loc[0]}: {lines[loc[0]-1].strip()[:80]}")

# Fix: remove orphaned closing divs
# Work backwards through line numbers so indices stay valid
orphan_lines = sorted(set(loc[0] for loc in tracker.orphans), reverse=True)
print(f"\nLines to remove: {orphan_lines}")

for lnum in orphan_lines:
    idx = lnum - 1  # 0-indexed
    line = lines[idx]
    stripped = line.strip()
    # Only remove if the line is ONLY a closing div (possibly with whitespace)
    if stripped == '</div>':
        print(f"  Removing line {lnum}: '{line}'")
        lines.pop(idx)
    else:
        print(f"  Skipping line {lnum} (has other content): '{stripped}'")

result = '\n'.join(lines)

# Verify balance
opens = result.count('<div')
closes = result.count('</div>')
print(f"\nAfter fix: <div> = {opens}, </div> = {closes}, balance = {opens - closes}")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(result)

print("✅ index.html saved")
