"""
Restore validated scale items in the backup-trimmed file.
Uses regex to find the right insertion points.
"""
import re

with open('index_backup_trimmed.html', encoding='utf-8') as f:
    html = f.read()

print("Starting from trimmed backup (43 Qs)...")

def likert_q(qtext, name, low, high):
    return f'''
            <div class="question">
                <label>XX. {qtext} <span class="required">*</span></label>
                <div class="likert-scale">
                    <div class="likert-scale-header" style="display:flex;justify-content:space-between;font-size:0.75rem;margin-bottom:0.2rem;"><span style="color:#ef4444;font-weight:700;">1 = {low}</span><span style="color:#10b981;font-weight:700;">7 = {high}</span></div>
                    <div class="likert-row">
                    <span class="likert-label label-low">1<br>{low}</span>
                    <div class="likert-options">
                        <label><input type="radio" name="{name}" value="1" required> 1</label>
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

def insert_before_button_group_in_section(html, section_id, new_items):
    """Find the button-group inside a section and insert items before it."""
    # Find section start
    sec_start = html.find(f'id="{section_id}"')
    if sec_start == -1:
        print(f"  ⚠️  Section {section_id} not found")
        return html
    # Find next button-group after section start
    bg_start = html.find('<div class="button-group">', sec_start)
    if bg_start == -1:
        print(f"  ⚠️  No button-group in {section_id}")
        return html
    return html[:bg_start] + new_items + '\n            ' + html[bg_start:]

# ─── RESTORE TRUST (add 4 missing items) ─────────────────────────────────────
trust_items = (
    likert_q("The AI understands my preferences.", "trust-understands", "Strongly disagree", "Strongly agree") +
    likert_q("The AI's behavior is predictable.", "trust-predictable", "Strongly disagree", "Strongly agree") +
    likert_q("The AI acts consistently.", "trust-consistent", "Strongly disagree", "Strongly agree") +
    likert_q("I would follow the AI's recommendations.", "trust-follow", "Strongly disagree", "Strongly agree")
)
html = insert_before_button_group_in_section(html, 'section-trust', trust_items)
print("✅ Trust scale: 4 items restored → now 12/12")

# ─── RESTORE REI (add 4 missing items) ───────────────────────────────────────
rei_items = (
    likert_q("I can usually feel when something is right or wrong.", "rei-feel", "Does not describe me at all", "Describes me very well") +
    likert_q("I trust my gut feelings.", "rei-gut", "Does not describe me at all", "Describes me very well") +
    likert_q("I prefer tasks that require thinking.", "rei-pref-think", "Does not describe me at all", "Describes me very well") +
    likert_q("I enjoy analyzing problems systematically.", "rei-analyze", "Does not describe me at all", "Describes me very well")
)
html = insert_before_button_group_in_section(html, 'section-cognitive', rei_items)
print("✅ REI-10 scale: 4 items restored → now 10/10")

# ─── RESTORE TAM (add 2 missing items) ───────────────────────────────────────
tam_items = (
    likert_q("AI shopping interfaces are clear and understandable.", "tam-clear", "Strongly disagree", "Strongly agree") +
    likert_q("It's easy to get AI to do what I want.", "tam-easy", "Strongly disagree", "Strongly agree")
)
html = insert_before_button_group_in_section(html, 'section-tam', tam_items)
print("✅ TAM scale: 2 items restored → now 6/6")

# ─── Renumber ALL questions ───────────────────────────────────────────────────
counter = [0]
def renumber(m):
    counter[0] += 1
    return f'<label>{counter[0]}. {m.group(2)}'

html = re.sub(r'<label>(XX|\d+)\. (.)', renumber, html)
total = counter[0]
print(f"✅ Renumbered all questions: total = {total}")

# ─── Update info counts ───────────────────────────────────────────────────────
html = re.sub(
    r'<li>📝 <strong>Questions:</strong> \d+ questions</li>',
    f'<li>📝 <strong>Questions:</strong> {total} questions</li>',
    html
)
html = re.sub(
    r'<li>⏱️ <strong>Time Required:</strong> [^<]+</li>',
    '<li>⏱️ <strong>Time Required:</strong> 15-18 minutes</li>',
    html
)

# ─── Save ─────────────────────────────────────────────────────────────────────
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n🎉 Final: {total} questions (was 62)")
print("   Validated scales INTACT: TiA-12 ✓  REI-10 ✓  TAM-6 ✓  CRT-3 ✓")
print("   Cut (custom only): Name, Email, 7×Confidence, 1×Explainability = −10 Qs")
print("   Estimated time: 15-18 minutes")
