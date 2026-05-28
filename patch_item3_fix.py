#!/usr/bin/env python3
"""
JewelLens – Item 3 fixes (run after patch_item3_followup.py):
  1. runFollowUp() rewritten — correct callClaude(imagePayload, prompt, maxTokens) signature
  2. "Lower-cost alternative" chip  →  "Stone alternatives"
  3. Vendor brief chip: solid gold fill + white text when selected

Run: python3 patch_item3_fix.py
Then: git add -A && git commit -m "fix: followup callClaude signature, chip label, vendor colour" && git push
"""

SRC = 'index.html'

with open(SRC, encoding='utf-8') as f:
    src = f.read()

ok, warn = [], []


# ── 1. CSS: vendor brief solid gold when selected ─────────────────────────────

OLD_CSS = '.followup-chip.vendor-chip.selected{background:rgba(201,152,60,0.22)}'
NEW_CSS = '.followup-chip.vendor-chip.selected{background:#c9983c;color:#fff;border-color:#c9983c}'

if OLD_CSS in src:
    src = src.replace(OLD_CSS, NEW_CSS, 1)
    ok.append('Vendor brief selected state → solid gold')
else:
    warn.append('MANUAL CSS: .followup-chip.vendor-chip.selected — set background:#c9983c;color:#fff;border-color:#c9983c')


# ── 2. HTML: chip label swap ──────────────────────────────────────────────────

OLD_CHIP = 'data-q="Lower-cost alternative" onclick="selectFollowupChip(this)">Lower-cost alternative</div>'
NEW_CHIP = 'data-q="Stone alternatives" onclick="selectFollowupChip(this)">Stone alternatives</div>'

if OLD_CHIP in src:
    src = src.replace(OLD_CHIP, NEW_CHIP, 1)
    ok.append('Chip: "Lower-cost alternative" → "Stone alternatives"')
else:
    warn.append('MANUAL HTML: change data-q and text of "Lower-cost alternative" chip to "Stone alternatives"')


# ── 3. JS: rewrite runFollowUp() with correct callClaude signature ────────────
#
# callClaude(imagePayload, prompt, maxTokens)
#   imagePayload  = [{type:"image",source:{...}}]  or  []
#   prompt        = plain string (merged into user message content)
#   maxTokens     = number
#
# callClaude returns a parsed JSON object (it runs JSON.parse internally).
# So we ask the model to return {"answer":"..."} and read resp.answer.

NEW_FN = (
    'function runFollowUp() {\n'
    '  var chip  = document.querySelector(\'.followup-chip.selected\');\n'
    '  var ta    = document.getElementById(\'followup-input\');\n'
    '  var typed = ta ? ta.value.trim() : \'\';\n'
    '  var label = chip ? chip.dataset.q : \'\';\n'
    '  var q     = typed ? (label ? label + \': \' + typed : typed) : label;\n'
    '  if (!q) { if (ta) ta.focus(); return; }\n'
    '\n'
    '  var btn    = document.getElementById(\'followup-btn\');\n'
    '  var ansBox = document.getElementById(\'followup-answer\');\n'
    '  var ansEl  = document.getElementById(\'followup-ans-text\');\n'
    '  var cpyBtn = document.getElementById(\'followup-copy-btn\');\n'
    '\n'
    '  btn.disabled    = true;\n'
    '  btn.textContent = \'Asking\u2026\';\n'
    '  if (ansBox) ansBox.classList.remove(\'visible\');\n'
    '\n'
    '  var isVendor = (label === \'\u2726 Vendor brief\');\n'
    '  var maxTok   = isVendor ? 1000 : 800;\n'
    '\n'
    '  var instructions = isVendor\n'
    '    ? \'You are a senior jewellery trade buyer. Using the piece analysis provided, write one concise paragraph (4-6 sentences) suitable for forwarding to a manufacturer or supplier. Include: exact piece type, construction method, materials with quality markers, craftsmanship tradition if identifiable, and commercial tier. Include any specific requirements the user mentions. Use professional B2B trade language only. No consumer-facing styling language.\'\n'
    '    : \'You are a jewellery expert. Answer only the specific question asked, using the piece analysis provided. Be concise (3-5 sentences), direct, and factual. Do not repeat the full analysis.\';\n'
    '\n'
    '  var ctx    = window.lastAnalysis ? \'Piece analysis:\\n\' + JSON.stringify(window.lastAnalysis) + \'\\n\\n\' : \'\';\n'
    '  var prompt = instructions + \'\\n\\n\' + ctx + \'Question: \' + q + \'\\n\\nRespond with valid JSON only in this exact format: {"answer":"your response here"}\';\n'
    '\n'
    '  var imgPayload = window.lastImageBase64\n'
    '    ? [{type:\'image\',source:{type:\'base64\',media_type:window.lastImageType||\'image/jpeg\',data:window.lastImageBase64}}]\n'
    '    : [];\n'
    '\n'
    '  callClaude(imgPayload, prompt, maxTok)\n'
    '    .then(function(resp) {\n'
    '      var text = (resp && resp.answer) ? resp.answer : \'\';\n'
    '      if (!text) text = \'No answer returned. Please try again.\';\n'
    '      if (ansEl)  ansEl.textContent  = text;\n'
    '      if (ansBox) ansBox.classList.add(\'visible\');\n'
    '      if (cpyBtn) cpyBtn.onclick = function() {\n'
    '        var self = this;\n'
    '        function done() {\n'
    '          self.textContent = \'Copied \u2713\';\n'
    '          setTimeout(function() { self.textContent = \'Copy answer\'; }, 2000);\n'
    '        }\n'
    '        var p = navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject();\n'
    '        p.then(done).catch(function() {\n'
    '          var tmp = document.createElement(\'textarea\');\n'
    '          tmp.value = text; document.body.appendChild(tmp);\n'
    '          tmp.select(); document.execCommand(\'copy\');\n'
    '          document.body.removeChild(tmp); done();\n'
    '        });\n'
    '      };\n'
    '      btn.disabled    = false;\n'
    '      btn.textContent = \'Ask \u2192\';\n'
    '    })\n'
    '    .catch(function() {\n'
    '      if (ansEl)  ansEl.textContent  = \'Something went wrong. Please try again.\';\n'
    '      if (ansBox) ansBox.classList.add(\'visible\');\n'
    '      btn.disabled    = false;\n'
    '      btn.textContent = \'Ask \u2192\';\n'
    '    });\n'
    '}'
)

# Locate the function by finding its start and the next function after it
START = '\nfunction runFollowUp() {'
END   = '\nfunction resetFollowUp() {'

s_idx = src.find(START)
e_idx = src.find(END, s_idx + 1) if s_idx != -1 else -1

if s_idx != -1 and e_idx != -1:
    # Replace from START up to (not including) END
    src = src[:s_idx] + '\n' + NEW_FN + src[e_idx:]
    ok.append('runFollowUp() rewritten with correct callClaude signature')
else:
    warn.append(
        'MANUAL JS: replace the entire runFollowUp() function body.\n'
        '  Key changes:\n'
        '  - Build imgPayload = window.lastImageBase64 ? [{type:"image",...}] : []\n'
        '  - Build prompt string (instructions + analysis + question + JSON instruction)\n'
        '  - Call callClaude(imgPayload, prompt, maxTok)\n'
        '  - Read answer from resp.answer (not resp.content)'
    )


# ── write & report ─────────────────────────────────────────────────────────────

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(src)

print()
for m in ok:   print('\u2714  ' + m)
if warn:
    print()
    for m in warn: print('\u26a0   ' + m)

print()
if not warn:
    print('All clean. Run:')
else:
    print('File written. Fix \u26a0 items manually, then run:')

print('  git add -A && git commit -m "fix: followup callClaude signature, chip label, vendor colour" && git push')
