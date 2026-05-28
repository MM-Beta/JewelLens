#!/usr/bin/env python3
"""
JewelLens – Item 3: Follow-up Q&A in Know It tab
=========================================================
Adds, below the Care Tip in the Know It tab:
  • 4 quick-question chips (+ ✦ Vendor brief)
  • Free-text textarea
  • Ask → button  (NOT counted against usage limit)
  • Inline answer box with Copy button

API call:  original image base64  +  full analysis JSON  +  user question
Max tokens: 800 standard / 1000 vendor brief

Run from repo root:
  python3 patch_item3_followup.py
Then:
  git add -A && git commit -m "item3: follow-up Q&A in Know It tab" && git push
"""

import re, sys

SRC = 'index.html'

with open(SRC, encoding='utf-8') as f:
    src = f.read()

ok, warn = [], []


# ═══════════════════════════════════════════════════════════════ 1 · CSS ═══

CSS = """
/* ─── Item 3: Follow-up Q&A ───────────────────────────────────────────────── */
.followup-divider{height:1px;background:rgba(200,180,150,0.4);margin:14px 0}
.followup-section{margin:0 0 10px}
.followup-label{font-size:9px;font-weight:500;letter-spacing:.14em;
  text-transform:uppercase;color:#a87c28;margin-bottom:8px}
.followup-chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
.followup-chip{padding:5px 11px;border-radius:99px;font-size:11px;
  color:#5c4d3a;border:1px solid rgba(200,180,150,0.4);background:#fdfaf5;
  cursor:pointer;transition:all .18s;white-space:nowrap;
  font-family:'DM Sans',sans-serif}
.followup-chip:hover,.followup-chip.selected{
  border-color:#c9983c;color:#a87c28;background:rgba(201,152,60,0.12)}
.followup-chip.vendor-chip{border-color:rgba(201,152,60,.5);
  background:rgba(201,152,60,0.12);color:#a87c28;font-weight:500}
.followup-chip.vendor-chip.selected{background:rgba(201,152,60,0.22)}
.followup-textarea{width:100%;background:#fdfaf5;
  border:1px solid rgba(200,180,150,0.4);border-radius:8px;
  padding:9px 12px;font-size:12px;font-family:'DM Sans',sans-serif;
  color:#1e1a16;resize:none;height:54px;line-height:1.5;
  margin-bottom:8px;transition:border-color .18s;box-sizing:border-box}
.followup-textarea:focus{outline:none;border-color:#c9983c}
.followup-textarea::placeholder{color:#9a8870}
.followup-btn{width:100%;
  background:linear-gradient(135deg,#c9983c,#e0b050);
  color:#fff;border:none;border-radius:8px;padding:10px;font-size:12px;
  font-weight:500;font-family:'DM Sans',sans-serif;cursor:pointer;
  margin-bottom:10px;letter-spacing:.02em}
.followup-btn:disabled{opacity:.6;cursor:wait}
.followup-answer{background:#fdfaf5;
  border:1px solid rgba(200,180,150,0.4);border-radius:8px;
  padding:12px;margin-bottom:10px;display:none}
.followup-answer.visible{display:block}
.followup-ans-label{font-size:9px;letter-spacing:.1em;text-transform:uppercase;
  color:#a87c28;font-weight:500;margin-bottom:6px}
.followup-ans-text{font-size:12px;color:#5c4d3a;line-height:1.65}
.followup-copy{font-size:10px;color:#c9983c;margin-top:8px;display:block;
  padding-top:8px;border-top:1px solid rgba(200,180,150,0.4);
  text-align:right;letter-spacing:.04em;cursor:pointer;
  background:none;border-left:none;border-right:none;border-bottom:none;
  width:100%;font-family:'DM Sans',sans-serif}
.followup-copy:hover{color:#a87c28}
"""

if '</style>' in src:
    src = src.replace('</style>', CSS + '</style>', 1)
    ok.append('CSS inserted')
else:
    warn.append('FAIL CSS: </style> not found')


# ══════════════════════════════════════════════════════════════ 2 · HTML ═══

FOLLOWUP_HTML = (
    '\n        <!-- \u2500\u2500 Item 3: Follow-up Q&A \u2500\u2500 -->'
    '\n        <div class="followup-divider"></div>'
    '\n        <div class="followup-section" id="followup-section">'
    '\n          <div class="followup-label">Ask about this piece</div>'
    '\n          <div class="followup-chips">'
    '\n            <div class="followup-chip" data-q="Lower-cost alternative"'
    ' onclick="selectFollowupChip(this)">Lower-cost alternative</div>'
    '\n            <div class="followup-chip" data-q="Manufacturing complexity"'
    ' onclick="selectFollowupChip(this)">Manufacturing complexity</div>'
    '\n            <div class="followup-chip" data-q="Weight estimate"'
    ' onclick="selectFollowupChip(this)">Weight estimate</div>'
    '\n            <div class="followup-chip vendor-chip" data-q="\u2726 Vendor brief"'
    ' onclick="selectFollowupChip(this)">\u2726 Vendor brief</div>'
    '\n          </div>'
    '\n          <textarea id="followup-input" class="followup-textarea"'
    '\n            placeholder="e.g. What stone could replace the pearl at lower cost?"></textarea>'
    '\n          <button id="followup-btn" class="followup-btn"'
    ' onclick="runFollowUp()">Ask \u2192</button>'
    '\n          <div class="followup-answer" id="followup-answer">'
    '\n            <div class="followup-ans-label">\u2726 Answer</div>'
    '\n            <div class="followup-ans-text" id="followup-ans-text"></div>'
    '\n            <button class="followup-copy" id="followup-copy-btn">Copy answer</button>'
    '\n          </div>'
    '\n        </div>'
    '\n        '
)

html_ok = False
for anchor in ['<div class="rating-row"', "<div class='rating-row'"]:
    if anchor in src:
        src = src.replace(anchor, FOLLOWUP_HTML + anchor, 1)
        ok.append('HTML inserted before .rating-row')
        html_ok = True
        break
if not html_ok:
    warn.append(
        'FAIL HTML: .rating-row not found.\n'
        '  Manually paste the follow-up HTML block before the rating row\n'
        '  in the Know It tab. The block starts with:\n'
        '  <div class="followup-divider"></div>'
    )


# ════════════════════════════════════════════════════════ 3 · JS functions ═══
#
# Written as a normal string so single quotes inside are fine.
# JS literal \n → Python \\n so the backslash-n lands in the file.

JS = """
/* \u2500\u2500\u2500 Item 3: Follow-up Q&A \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */
window.lastAnalysis    = null;
window.lastImageBase64 = null;
window.lastImageType   = 'image/jpeg';

function selectFollowupChip(el) {
  document.querySelectorAll('.followup-chip').forEach(function(c) {
    c.classList.remove('selected');
  });
  el.classList.add('selected');
  var ta = document.getElementById('followup-input');
  if (!ta) return;
  if (el.dataset.q === '\u2726 Vendor brief') {
    ta.value = '';
    ta.placeholder = 'Optional: add specific requirements\u2026';
  } else {
    ta.placeholder = 'Add detail or ask a different question\u2026';
  }
  var ab = document.getElementById('followup-answer');
  if (ab) ab.classList.remove('visible');
}

function runFollowUp() {
  var chip  = document.querySelector('.followup-chip.selected');
  var ta    = document.getElementById('followup-input');
  var typed = ta ? ta.value.trim() : '';
  var label = chip ? chip.dataset.q : '';
  var q     = typed ? (label ? label + ': ' + typed : typed) : label;
  if (!q) { if (ta) ta.focus(); return; }

  var btn    = document.getElementById('followup-btn');
  var ansBox = document.getElementById('followup-answer');
  var ansEl  = document.getElementById('followup-ans-text');
  var cpyBtn = document.getElementById('followup-copy-btn');

  btn.disabled    = true;
  btn.textContent = 'Asking\u2026';
  if (ansBox) ansBox.classList.remove('visible');

  var isVendor = (label === '\u2726 Vendor brief');
  var maxTok   = isVendor ? 1000 : 800;

  var sys = isVendor
    ? 'You are a senior jewellery trade buyer. Using the piece analysis provided, write one concise paragraph (4-6 sentences) suitable for forwarding to a manufacturer or supplier. Include: exact piece type, construction method, materials with quality markers, craftsmanship tradition if identifiable, and commercial tier. If the user has added specific requirements, include them. Use professional B2B trade language only. No consumer-facing styling language.'
    : 'You are a jewellery expert. Answer only the specific question asked, using the piece analysis data provided. Be concise (3-5 sentences), direct, and factual. Do not repeat the full analysis.';

  var ctx    = window.lastAnalysis ? 'Piece analysis:\\n' + JSON.stringify(window.lastAnalysis) + '\\n\\n' : '';
  var usrMsg = ctx + 'Question: ' + q;

  var messages = window.lastImageBase64
    ? [{ role: 'user', content: [
        { type: 'image', source: {
            type: 'base64',
            media_type: window.lastImageType || 'image/jpeg',
            data: window.lastImageBase64 } },
        { type: 'text', text: usrMsg }
      ]}]
    : [{ role: 'user', content: usrMsg }];

  callClaude(messages, sys, maxTok)
    .then(function(resp) {
      var text = '';
      if (resp && resp.content)
        resp.content.forEach(function(b) { if (b.type === 'text') text += b.text; });
      text = text.trim() || 'No answer returned. Please try again.';
      if (ansEl)  ansEl.textContent = text;
      if (ansBox) ansBox.classList.add('visible');
      if (cpyBtn) cpyBtn.onclick = function() {
        var self = this;
        function done() {
          self.textContent = 'Copied \u2713';
          setTimeout(function() { self.textContent = 'Copy answer'; }, 2000);
        }
        var p = navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject();
        p.then(done).catch(function() {
          var tmp = document.createElement('textarea');
          tmp.value = text;
          document.body.appendChild(tmp);
          tmp.select();
          document.execCommand('copy');
          document.body.removeChild(tmp);
          done();
        });
      };
      btn.disabled    = false;
      btn.textContent = 'Ask \u2192';
    })
    .catch(function() {
      if (ansEl)  ansEl.textContent = 'Something went wrong. Please try again.';
      if (ansBox) ansBox.classList.add('visible');
      btn.disabled    = false;
      btn.textContent = 'Ask \u2192';
    });
}

function resetFollowUp() {
  document.querySelectorAll('.followup-chip').forEach(function(c) {
    c.classList.remove('selected');
  });
  var ta = document.getElementById('followup-input');
  if (ta) {
    ta.value = '';
    ta.placeholder = 'e.g. What stone could replace the pearl at lower cost?';
  }
  var ab = document.getElementById('followup-answer');
  if (ab) ab.classList.remove('visible');
  var bt = document.getElementById('followup-btn');
  if (bt) { bt.disabled = false; bt.textContent = 'Ask \u2192'; }
}
"""

last_script = src.rfind('</script>')
if last_script != -1:
    src = src[:last_script] + JS + src[last_script:]
    ok.append('JS functions inserted (selectFollowupChip, runFollowUp, resetFollowUp)')
else:
    warn.append('FAIL JS: </script> not found')


# ══════════════════════════════════════════ 4 · store image in analyzeJewellery ═══
# Parse the actual parameter names from the function signature so we inject correctly.

m = re.search(r'(function\s+analyzeJewellery\s*\(([^)]+)\)\s*\{)', src)
if m:
    plist = [p.strip() for p in m.group(2).split(',')]
    p_img  = plist[0]
    p_type = plist[1] if len(plist) > 1 else "'image/jpeg'"
    inject = (
        '\n  window.lastImageBase64 = ' + p_img + ';'
        '\n  window.lastImageType   = (' + p_type + ') || \'image/jpeg\';'
        '\n'
    )
    src = src.replace(m.group(1), m.group(1) + inject, 1)
    ok.append('Image stored in analyzeJewellery (params: ' + ', '.join(plist) + ')')
else:
    warn.append(
        'MANUAL (analyzeJewellery): add these as first lines inside the function:\n'
        '    window.lastImageBase64 = <imgParam>;\n'
        "    window.lastImageType   = <typeParam> || 'image/jpeg';"
    )


# ═══════════════════════════════════════════════ 5 · store result in renderResults ═══

m2 = re.search(r'(function\s+renderResults\s*\(([^)]+)\)\s*\{)', src)
if m2:
    p_data = m2.group(2).strip().split(',')[0].strip()
    inject2 = '\n  window.lastAnalysis = ' + p_data + ';\n'
    src = src.replace(m2.group(1), m2.group(1) + inject2, 1)
    ok.append('Analysis stored in renderResults (param: ' + p_data + ')')
else:
    warn.append(
        'MANUAL (renderResults): add as first line inside the function:\n'
        '    window.lastAnalysis = <dataParam>;'
    )


# ═══════════════════════════════════════════════════ 6 · reset on new analysis ═══
# Hook resetFollowUp() to whichever screen-switch call starts a new analysis.

RESET_ANCHORS = [
    ("showScreen('sc-analyzing');", "showScreen('sc-analyzing');\n  resetFollowUp();"),
    ('showScreen("sc-analyzing");', 'showScreen("sc-analyzing");\n  resetFollowUp();'),
    ("showScreen('analyzing');",    "showScreen('analyzing');\n  resetFollowUp();"),
    ('showScreen("analyzing");',    'showScreen("analyzing");\n  resetFollowUp();'),
    # fallbacks without trailing semicolon
    ("showScreen('sc-analyzing')", "showScreen('sc-analyzing')\n  resetFollowUp();"),
    ('showScreen("sc-analyzing")', 'showScreen("sc-analyzing")\n  resetFollowUp();'),
]
reset_ok = False
for anchor, replacement in RESET_ANCHORS:
    if anchor in src:
        src = src.replace(anchor, replacement, 1)
        ok.append('resetFollowUp() hooked to ' + anchor)
        reset_ok = True
        break
if not reset_ok:
    warn.append(
        'MANUAL (reset): call resetFollowUp() wherever a new analysis begins\n'
        '    (look for the transition to sc-analyzing or the start of analyzeJewellery)'
    )


# ═══════════════════════════════════════════════════════════════ write & report ═══

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(src)

print()
for msg in ok:
    print('\u2714  ' + msg)

if warn:
    print()
    for msg in warn:
        print('\u26a0   ' + msg)
    print()
    print('File written. Fix \u26a0 items manually, then commit.')
else:
    print()
    print('All patches applied cleanly.')

print()
print('Next step:')
print('  git add -A && git commit -m "item3: follow-up Q&A in Know It tab" && git push')
