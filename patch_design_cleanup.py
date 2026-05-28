#!/usr/bin/env python3
"""JewelLens design cleanup — 6 targeted changes"""
import os, sys

HTML_PATH = os.path.join(os.path.dirname(__file__), 'index.html')

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

errors = []
changes = []

def replace_once(old, new, label):
    global html
    if old not in html:
        errors.append(label + ': anchor not found')
        return
    html = html.replace(old, new, 1)
    changes.append(label)

# ── 1. CSS — hero padding 48px → 28px ──────────────────────────────────────
replace_once(
    'padding: 48px 0 24px;',
    'padding: 28px 0 16px;',
    'Hero padding reduced'
)

# ── 2. CSS — section-label color: text3 → gold-dark ────────────────────────
replace_once(
    '.section-label { font-size: 10px; font-weight: 500; letter-spacing: .14em; color: var(--text3); margin-bottom: 10px; text-transform: uppercase; }',
    '.section-label { font-size: 10px; font-weight: 500; letter-spacing: .14em; color: var(--gold-dark); margin-bottom: 10px; text-transform: uppercase; }',
    'Section label darkened to gold-dark'
)

# ── 3. CSS — sample-strip-label color: text3 → gold-dark ───────────────────
replace_once(
    '.sample-strip-label{font-size:10px;font-weight:500;letter-spacing:.14em;color:var(--text3);margin-bottom:10px;text-transform:uppercase;}',
    '.sample-strip-label{font-size:10px;font-weight:500;letter-spacing:.14em;color:var(--gold-dark);margin-bottom:10px;text-transform:uppercase;}',
    'Sample strip label darkened'
)

# ── 4. CSS — context-label color: text3 → gold-dark ────────────────────────
replace_once(
    '.context-label{font-size:10px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--text3);margin-bottom:6px;}',
    '.context-label{font-size:10px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--gold-dark);margin-bottom:6px;}',
    'Context label darkened'
)

# ── 5. HTML — remove hero-divider line ─────────────────────────────────────
replace_once(
    '\n    <div class="hero-divider"></div>',
    '',
    'Hero divider removed'
)

# ── 6. HTML — remove usage bar (the confusing empty box) ───────────────────
replace_once(
    '\n  <div class="usage-bar">\n    <div class="usage-dots" id="usage-dots"></div>\n    <div class="usage-text" id="usage-text"></div>\n  </div>',
    '',
    'Usage bar removed'
)

# ── 7. HTML — collapse 3 note lines into 1 + remove metal disclaimer ────────
replace_once(
    '  <p class="upload-hint">✦ Works with camera photos, screenshots and saved images · Auto-optimised before sending</p>\n  <p class="privacy-note">🔒 Your photos are analysed and not stored by JewelLens</p>\n  <p class="privacy-note" style="margin-top:4px">⚠ Metal identification is visual only — hallmark certificates confirm purity.</p>',
    '  <p class="upload-hint">🔒 Photos not stored &middot; Camera, WhatsApp &amp; screenshots welcome &middot; Auto-optimised</p>',
    '3 note lines collapsed to 1, metal disclaimer removed'
)

# ── REPORT ──────────────────────────────────────────────────────────────────
if errors:
    print("\nERRORS — file NOT saved:")
    for e in errors:
        print(" -", e)
    sys.exit(1)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print("Done. Changes applied:")
for c in changes:
    print(" ✓", c)
print(f"\nFile size: {len(html)//1024}KB")
print('Run: git add -A && git commit -m "design cleanup: tighter layout, gold labels, remove clutter" && git push')
