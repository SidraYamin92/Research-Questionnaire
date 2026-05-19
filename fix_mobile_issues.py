"""
Fix all Likert scales in index.html:
1. Wrap the inner content in a .likert-row div
2. Add label-low class to first label (left), label-high to second (right)
3. Also add touchmove overscroll prevention in script.js
"""

import re

# ── 1. Fix index.html ──────────────────────────────────────────────────────

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Pattern: <div class="likert-scale">
#              <span class="likert-label">LABEL_LOW</span>
#              <div class="likert-options">...</div>
#              <span class="likert-label">LABEL_HIGH</span>
#          </div>
#
# We want to wrap the inner content in <div class="likert-row">

def replace_likert(m):
    full = m.group(0)

    # Extract parts
    low_match  = re.search(r'<span class="likert-label">(.+?)</span>', full)
    high_match = re.findall(r'<span class="likert-label">(.+?)</span>', full)
    opts_match = re.search(r'<div class="likert-options">.*?</div>', full, re.DOTALL)

    if not low_match or not opts_match or len(high_match) < 2:
        return full   # leave as-is if we can't parse

    low_text  = high_match[0]
    high_text = high_match[1]
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

new_html = pattern.sub(replace_likert, html)

changes = len(pattern.findall(html))
print(f"✅ Likert scales updated: {changes} found and rebuilt")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("✅ index.html saved")

# ── 2. Fix script.js – prevent pull-to-refresh on Android ─────────────────

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

pull_to_refresh_fix = """
// ===== PREVENT ANDROID PULL-TO-REFRESH =====
(function () {
    let startY = 0;
    document.addEventListener('touchstart', function (e) {
        startY = e.touches[0].clientY;
    }, { passive: true });

    document.addEventListener('touchmove', function (e) {
        const y = e.touches[0].clientY;
        // Block pull-down when already at the top of the page
        if (y > startY && window.scrollY === 0) {
            e.preventDefault();
        }
    }, { passive: false });
})();
"""

# Only add once
if 'PREVENT ANDROID PULL-TO-REFRESH' not in js:
    js = pull_to_refresh_fix + js
    print("✅ Pull-to-refresh prevention added to script.js")
else:
    print("ℹ️  Pull-to-refresh fix already present in script.js")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("\n🎉 Both fixes applied successfully!")
print("   1. Likert scale labels now clearly show low/high anchors")
print("   2. Android pull-to-refresh disabled (no more accidental restarts)")
