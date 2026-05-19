import re

with open('index.html', encoding='utf-8') as f:
    content = f.read()

parts = re.split(r'(?=<div class="section[^"]*" id="section-)', content)
print("=== SECTION QUESTION COUNTS ===")
for part in parts[1:]:
    m = re.match(r'<div class="section[^"]*" id="(section-[^"]+)"', part)
    if m:
        sid = m.group(1)
        qs = part.count('<div class="question">')
        print(f"  {sid}: {qs} questions")

opens = content.count('<div')
closes = content.count('</div>')
print(f"\nDiv balance: {opens} open, {closes} close = {opens - closes}")
print("✅ OK" if opens == closes else "❌ IMBALANCED")
