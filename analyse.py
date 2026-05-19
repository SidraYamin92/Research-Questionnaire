import re

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# Get all sections and their question counts
section_pattern = re.compile(r'<div class="section[^"]*" id="(section-[^"]+)">(.*?)</div>\s*\n\s*(?=<div class="section|$)', re.DOTALL)

# Better: split by section id
parts = re.split(r'(?=<div class="section[^"]*" id="section-)', html)

for part in parts:
    m = re.match(r'<div class="section[^"]*" id="(section-[^"]+)"', part)
    if not m:
        continue
    sid = m.group(1)
    likert  = len(re.findall(r'class="likert-scale"', part))
    radio   = len(re.findall(r'class="radio-group"', part))
    selects = len(re.findall(r'<select ', part))
    areas   = len(re.findall(r'<textarea ', part))
    total   = likert + radio + selects + areas
    
    # get question texts
    qs = re.findall(r'<label[^>]*>\s*(\d+\.[^<]{10,80})', part)
    
    print(f"\n[{sid}] — {total} questions")
    if qs:
        for q in qs:
            print(f"   {q.strip()[:90]}")
    print(f"   (Likert:{likert}  Radio:{radio}  Select:{selects}  Textarea:{areas})")
