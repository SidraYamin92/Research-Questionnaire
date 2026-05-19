"""
Restore original questionnaire and apply ONLY safe cuts:
  1. Remove Name + Email from demographics (non-essential, helps anonymity)
  2. Remove "How confident are you in this decision?" from each scenario
     (custom repeat question, not part of any validated scale)
  3. Remove 1 overlapping explainability Q (custom question)
  4. Reapply mobile fixes (likert-row wrapper + labels)
  5. Renumber all questions

Keeps INTACT (validated scales):
  - TiA Trust in Automation: all 12 items
  - REI-10: all 10 items
  - TAM: all 6 items
  - CRT: all 3 items
"""

import re, shutil

# Start from the original complete version
shutil.copy('index_COMPLETE.html', 'index.html')
print("✅ Restored from original index_COMPLETE.html")

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# ─── 1. Fix mobile Likert labels on original first ───────────────────────────
def replace_likert(m):
    full = m.group(0)
    high_texts = re.findall(r'<span class="likert-label">(.+?)</span>', full)
    opts_match = re.search(r'<div class="likert-options">.*?</div>', full, re.DOTALL)
    if not opts_match or len(high_texts) < 2:
        return full
    low_text  = high_texts[0]
    high_text = high_texts[1]
    opts_block = opts_match.group(0)
    return (
        '<div class="likert-scale">\n'
        '                    <div class="likert-scale-header" style="display:flex;justify-content:space-between;font-size:0.75rem;margin-bottom:0.2rem;">'
        f'<span style="color:#ef4444;font-weight:700;">1 = {low_text}</span>'
        f'<span style="color:#10b981;font-weight:700;">7 = {high_text}</span>'
        '</div>\n'
        '                    <div class="likert-row">\n'
        f'                    <span class="likert-label label-low">1<br>{low_text}</span>\n'
        f'                    {opts_block}\n'
        f'                    <span class="likert-label label-high">7<br>{high_text}</span>\n'
        '                    </div>\n'
        '                </div>'
    )

pattern = re.compile(
    r'<div class="likert-scale">\s*'
    r'<span class="likert-label">.*?</span>\s*'
    r'<div class="likert-options">.*?</div>\s*'
    r'<span class="likert-label">.*?</span>\s*'
    r'</div>',
    re.DOTALL
)
likert_count = len(pattern.findall(html))
html = pattern.sub(replace_likert, html)
print(f"✅ Mobile Likert labels applied to {likert_count} scales")

# ─── 2. Add overscroll-behavior to body (pull-to-refresh fix) ────────────────
html = html.replace(
    'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\n    min-height: 100vh;',
    'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\n    min-height: 100vh;\n    overscroll-behavior: none;'
)

# ─── 3. Remove Name + Email from demographics ─────────────────────────────────
html = re.sub(
    r'\s*<div class="question">\s*<label>1\. Your Name.*?</div>\s*</div>',
    '', html, flags=re.DOTALL)
html = re.sub(
    r'\s*<div class="question">\s*<label>2\. Your Email.*?</div>\s*</div>',
    '', html, flags=re.DOTALL)
print("✅ Removed Name + Email from demographics")

# ─── 4. Remove "How confident are you" from ALL 7 scenarios ──────────────────
removed = 0
pattern_conf = re.compile(
    r'\s*<div class="question">\s*<label>\d+\. How confident are you in this decision\?.*?</div>\s*</div>',
    re.DOTALL
)
html, removed = pattern_conf.subn('', html)
print(f"✅ Removed 'How confident' question {removed} times (from {removed} scenarios)")

# ─── 5. Remove 1 explainability overlap Q ────────────────────────────────────
html = re.sub(
    r'\s*<div class="question">\s*<label>\d+\. Would AI explanations increase your trust.*?</div>\s*</div>',
    '', html, flags=re.DOTALL)
print("✅ Removed overlapping explainability question")

# ─── 6. Renumber all questions sequentially ──────────────────────────────────
counter = [0]

def renumber(m):
    counter[0] += 1
    return f'<label>{counter[0]}. {m.group(2)}'

html = re.sub(r'<label>(\d+)\. (.)', renumber, html)
print(f"✅ Renumbered all questions: total = {counter[0]}")

# ─── 7. Update welcome screen counts ─────────────────────────────────────────
html = re.sub(
    r'<li>📝 <strong>Questions:</strong> \d+ questions</li>',
    f'<li>📝 <strong>Questions:</strong> {counter[0]} questions</li>',
    html
)
html = re.sub(
    r'<li>⏱️ <strong>Time Required:</strong> [\d\-]+ minutes</li>',
    '<li>⏱️ <strong>Time Required:</strong> 15-18 minutes</li>',
    html
)
html = html.replace(
    'Please provide the following information (8 questions):',
    'Please provide the following information (5 questions):'
)

# ─── 8. Save ──────────────────────────────────────────────────────────────────
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n🎉 Done! Questionnaire trimmed: 62 → {counter[0]} questions")
print("   Validated scales kept INTACT (TiA-12, REI-10, TAM-6, CRT-3)")
print("   Only custom/redundant questions removed")
print("   Estimated time: 15-18 minutes")
