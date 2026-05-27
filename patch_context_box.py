#!/usr/bin/env python3
"""JewelLens patch — adds optional context box to Analyse screen"""
import os, sys

HTML_PATH = os.path.join(os.path.dirname(__file__), 'index.html')

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

errors = []

# ── 1. CSS ──────────────────────────────────────────────────────────────────
CSS_MARKER = '</style>'
CSS_BLOCK = """
/* Context box */
.context-wrap{margin-top:12px;}
.context-label{font-size:10px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--text3);margin-bottom:6px;}
.context-optional{font-weight:400;letter-spacing:0;text-transform:none;color:var(--text3);}
.context-textarea{width:100%;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);padding:10px 12px;font-family:var(--font-body);font-size:12px;color:var(--text);line-height:1.6;resize:none;transition:border-color .2s;height:62px;}
.context-textarea:focus{outline:none;border-color:var(--gold);}
.context-count{font-size:10px;color:var(--text3);text-align:right;margin-top:4px;}"""

if '/* Context box */' in html:
    print("CSS already patched.")
else:
    pos = html.rfind(CSS_MARKER)
    if pos == -1:
        errors.append("CSS: cannot find </style>")
    else:
        html = html[:pos] + CSS_BLOCK + '\n' + html[pos:]
        print("CSS injected.")

# ── 2. HTML ──────────────────────────────────────────────────────────────────
HTML_ANCHOR = '  <div class="spacer"></div>\n  <p class="section-label">Step 2'
CONTEXT_HTML = """  <div class="context-wrap">
    <p class="context-label">Tell us what you know <span class="context-optional">(optional)</span></p>
    <textarea class="context-textarea" id="piece-context" maxlength="280" rows="2" placeholder="e.g. Found in grandmother&#39;s box &middot; Bought in Japan 1960s &middot; Seller says 18k gold &middot; Has a stamp I can&#39;t read"></textarea>
    <p class="context-count" id="context-count">280 characters remaining</p>
  </div>
"""

if 'piece-context' in html:
    print("HTML already patched.")
else:
    pos = html.find(HTML_ANCHOR)
    if pos == -1:
        errors.append("HTML: cannot find Step 2 spacer anchor")
    else:
        html = html[:pos] + CONTEXT_HTML + html[pos:]
        print("HTML injected.")

# ── 3. JS — declare userCtx before gatekeeper ────────────────────────────────
JS_ANCHOR_CTX = "  var gatekeeper='CRITICAL FIRST CHECK"
CTX_DECL = "  var userCtx=(document.getElementById('piece-context').value||'').trim();\n"

if 'var userCtx=' in html:
    print("JS userCtx already declared.")
else:
    pos = html.find(JS_ANCHOR_CTX)
    if pos == -1:
        errors.append("JS: cannot find gatekeeper declaration")
    else:
        html = html[:pos] + CTX_DECL + html[pos:]
        print("JS userCtx declaration injected.")

# ── 4. JS — inject userCtx into prompt string ────────────────────────────────
OLD_PROMPT_FRAG = "'+productType+'. Trust this selection"

NEW_PROMPT_FRAG = (
    "'+productType+'."
    "+(userCtx?"
    "' The user has provided this additional context about the piece. "
    "Treat as unverified user belief, not established fact. "
    "If context contradicts visual evidence or hallmarks, flag the contradiction "
    "in visible_red_flags rather than deferring to it: \""
    "'+userCtx+'"
    "\"':'')+"
    "' Trust this selection"
)

if 'unverified user belief' in html:
    print("JS prompt already patched.")
elif OLD_PROMPT_FRAG not in html:
    errors.append("JS prompt: cannot find productType anchor — check prompt was not already modified")
else:
    html = html.replace(OLD_PROMPT_FRAG, NEW_PROMPT_FRAG, 1)
    print("JS prompt injected.")

# ── 5. JS — clear context textarea in resetApp() ────────────────────────────
RESET_ANCHOR = "  try{ document.getElementById('rate-up').classList.remove('rated');"
CTX_RESET = "  var pi=document.getElementById('piece-context'); if(pi) pi.value='';\n  var cc=document.getElementById('context-count'); if(cc) cc.textContent='280 characters remaining';\n"

if "pi.value=''" in html:
    print("JS reset already patched.")
else:
    pos = html.find(RESET_ANCHOR)
    if pos == -1:
        errors.append("JS reset: cannot find rate-up anchor in resetApp()")
    else:
        html = html[:pos] + CTX_RESET + html[pos:]
        print("JS reset injected.")

# ── 6. JS — character counter event listener ────────────────────────────────
LISTENER_ANCHOR = "try{ document.getElementById('ctype-a').addEventListener('change',updateCompareBtn); }catch(e){}"
CTX_LISTENER = ("try{ document.getElementById('piece-context').addEventListener('input',function(){"
                "var rem=280-this.value.length;"
                "var c=document.getElementById('context-count');"
                "if(c) c.textContent=rem+' character'+(rem===1?'':'s')+' remaining';"
                "}); }catch(e){}\n")

if "context-count" in html and "rem+' character" in html:
    print("JS listener already patched.")
elif LISTENER_ANCHOR not in html:
    errors.append("JS listener: cannot find ctype-a listener anchor")
else:
    html = html.replace(LISTENER_ANCHOR, CTX_LISTENER + LISTENER_ANCHOR, 1)
    print("JS listener injected.")

# ── WRITE + REPORT ────────────────────────────────────────────────────────────
if errors:
    print("\nERRORS — file NOT saved:")
    for e in errors:
        print(" -", e)
    sys.exit(1)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDone. File size: {len(html)//1024}KB")
print('Run: git add -A && git commit -m "add optional context box to analyse screen" && git push')
