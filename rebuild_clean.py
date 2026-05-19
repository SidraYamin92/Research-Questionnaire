"""
CLEAN REBUILD of index.html from the verified backup.
Strategy: split file into sections, modify each section independently, rejoin.
This guarantees all injected items stay INSIDE their sections.
"""
import re

with open('index_backup_trimmed.html', encoding='utf-8') as f:
    original = f.read()

# ── Helper: A single Likert question block ────────────────────────────────────
def likert_block(qtext, name, low, high, start_required=True):
    req_attr = ' required' if start_required else ''
    return f'''\n            <div class="question">
                <label>QQ. {qtext} <span class="required">*</span></label>
                <div class="likert-scale">
                    <div class="likert-scale-header" style="display:flex;justify-content:space-between;font-size:0.75rem;margin-bottom:0.2rem;"><span style="color:#ef4444;font-weight:700;">1 = {low}</span><span style="color:#10b981;font-weight:700;">7 = {high}</span></div>
                    <div class="likert-row">
                    <span class="likert-label label-low">1<br>{low}</span>
                    <div class="likert-options">
                        <label><input type="radio" name="{name}" value="1"{req_attr}> 1</label>
                        <label><input type="radio" name="{name}" value="2"> 2</label>
                        <label><input type="radio" name="{name}" value="3"> 3</label>
                        <label><input type="radio" name="{name}" value="4"> 4</label>
                        <label><input type="radio" name="{name}" value="5"> 5</label>
                        <label><input type="radio" name="{name}" value="6"> 6</label>
                        <label><input type="radio" name="{name}" value="7"> 7</label>
                    </div>
                    <span class="likert-label label-high">7<br>{high}</span>
                    </div>
                </div>
            </div>'''

def insert_before_last_button_group(section_html, new_items):
    """Find the LAST <div class="button-group"> in the section and insert before it."""
    idx = section_html.rfind('<div class="button-group">')
    if idx == -1:
        print(f"  WARNING: no button-group found!")
        return section_html
    return section_html[:idx] + new_items + '\n\n            ' + section_html[idx:]

# ── Split file into named section chunks ──────────────────────────────────────
# Pattern: split on section div openings, keep them as part of the chunk
section_pattern = re.compile(r'(?=<div class="section[^"]*" id="section-)')
parts = section_pattern.split(original)
# parts[0] = everything before the first section (head, progress bar, timer, container open)
# parts[1..] = each section starting with its opening div

header = parts[0]
sections = {}
section_order = []

for part in parts[1:]:
    m = re.match(r'<div class="section[^"]*" id="(section-[^"]+)"', part)
    if m:
        sid = m.group(1)
        sections[sid] = part
        section_order.append(sid)

print(f"Found {len(sections)} sections: {section_order}")

# ── 1. DEMOGRAPHICS: Add age + gender before the existing questions ───────────
age_gender = '''            <div class="question">
                <label>QQ. What is your age group? <span class="required">*</span></label>
                <select name="age" required>
                    <option value="">Select...</option>
                    <option value="18-24">18-24 years</option>
                    <option value="25-34">25-34 years</option>
                    <option value="35-44">35-44 years</option>
                    <option value="45-54">45-54 years</option>
                    <option value="55-64">55-64 years</option>
                    <option value="65+">65+ years</option>
                </select>
            </div>

            <div class="question">
                <label>QQ. What is your gender? <span class="required">*</span></label>
                <div class="radio-group">
                    <label><input type="radio" name="gender" value="male" required> Male</label>
                    <label><input type="radio" name="gender" value="female"> Female</label>
                    <label><input type="radio" name="gender" value="other"> Other</label>
                    <label><input type="radio" name="gender" value="prefer-not"> Prefer not to say</label>
                </div>
            </div>\n\n'''

# Insert at the start of demographics — after the <p class="section-intro"> line
demo = sections['section-demographics']
demo = re.sub(
    r'(<p class="section-intro">.*?</p>\s*)',
    r'\1' + age_gender,
    demo, count=1, flags=re.DOTALL
)
sections['section-demographics'] = demo
print("✅ Age + Gender added to demographics")

# ── 2. TRUST: Add 4 missing items (currently 8, need 12) ─────────────────────
trust_add = (
    likert_block("The AI understands my preferences.", "trust-understands", "Strongly disagree", "Strongly agree") +
    likert_block("The AI's behavior is predictable.", "trust-predictable", "Strongly disagree", "Strongly agree", False) +
    likert_block("The AI acts consistently.", "trust-consistent", "Strongly disagree", "Strongly agree", False) +
    likert_block("I would follow the AI's recommendations.", "trust-follow", "Strongly disagree", "Strongly agree", False)
)
sections['section-trust'] = insert_before_last_button_group(sections['section-trust'], trust_add)
print("✅ Trust: 4 items added → 12/12")

# ── 3. COGNITIVE (REI): Add 4 missing items (currently 6, need 10) ────────────
rei_add = (
    likert_block("I can usually feel when something is right or wrong.", "rei-feel", "Does not describe me at all", "Describes me very well") +
    likert_block("I trust my gut feelings.", "rei-gut", "Does not describe me at all", "Describes me very well", False) +
    likert_block("I prefer tasks that require thinking.", "rei-pref-think", "Does not describe me at all", "Describes me very well", False) +
    likert_block("I enjoy analyzing problems systematically.", "rei-analyze", "Does not describe me at all", "Describes me very well", False)
)
sections['section-cognitive'] = insert_before_last_button_group(sections['section-cognitive'], rei_add)
print("✅ REI-10: 4 items added → 10/10")

# ── 4. TAM: Add 2 missing items (currently 4, need 6) ────────────────────────
tam_add = (
    likert_block("AI shopping interfaces are clear and understandable.", "tam-clear", "Strongly disagree", "Strongly agree") +
    likert_block("It's easy to get AI to do what I want.", "tam-easy", "Strongly disagree", "Strongly agree", False)
)
sections['section-tam'] = insert_before_last_button_group(sections['section-tam'], tam_add)
print("✅ TAM: 2 items added → 6/6")

# ── 5. Rejoin all parts ───────────────────────────────────────────────────────
rebuilt = header + ''.join(sections[sid] for sid in section_order)

# ── 6. Renumber ALL questions sequentially (QQ. or existing numbers) ──────────
counter = [0]
def renumber(m):
    counter[0] += 1
    return f'<label>{counter[0]}. {m.group(2)}'

rebuilt = re.sub(r'<label>(QQ|\d+)\. (.)', renumber, rebuilt)
total = counter[0]
print(f"✅ Renumbered: {total} questions total")

# ── 7. Update welcome screen info ─────────────────────────────────────────────
rebuilt = re.sub(
    r'(<li>📝 <strong>Questions:</strong> )\d+( questions</li>)',
    rf'\g<1>{total}\2', rebuilt
)
rebuilt = re.sub(
    r'(<li>⏱️ <strong>Time Required:</strong> )[^<]+(</li>)',
    r'\g<1>15-18 minutes\2', rebuilt
)

# ── 8. Fix the thank-you stats box ───────────────────────────────────────────
rebuilt = re.sub(
    r'(<div class="stat-number">)\d+(</div>\s*<div class="stat-label">Questions Answered)',
    rf'\g<1>{total}\2', rebuilt
)

# ── 9. Add pull-to-refresh prevention to body CSS ────────────────────────────
rebuilt = rebuilt.replace(
    '</head>',
    '''    <style>
        html, body { overscroll-behavior: none; }
    </style>
</head>'''
)

# ── 10. Verify structure ───────────────────────────────────────────────────────
opens = rebuilt.count('<div')
closes = rebuilt.count('</div>')
print(f"\nStructure check: <div>={opens}  </div>={closes}  balance={opens-closes}")

# Per-section question count check
parts_check = re.split(r'(?=<div class="section[^"]*" id="section-)', rebuilt)
for part in parts_check[1:]:
    m = re.match(r'<div class="section[^"]*" id="(section-[^"]+)"', part)
    if m:
        sid = m.group(1)
        qs = part.count('<div class="question">')
        print(f"  {sid}: {qs} questions")

# ── 11. Save ──────────────────────────────────────────────────────────────────
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(rebuilt)

print(f"\n🎉 Done! index.html rebuilt cleanly with {total} questions")
print("   Sections are properly bounded — no content leakage")
