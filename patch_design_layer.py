#!/usr/bin/env python3
# JewelLens — Design Layer patch (verified session work)
# Applies: fonts, tokens+dark theme, theme toggle, spotlit+corners,
# hero fix, chip emoji strip, samples reorder, Daily Stone 12-sign scroller.
import io, sys

f = open('index.html', encoding='utf-8'); s = f.read(); f.close()
orig = s
log = []

def repl(old, new, label, count=1):
    global s
    n = s.count(old)
    if n == 0:
        log.append(('MISS', label, 'anchor not found'))
        return
    if n != count:
        log.append(('WARN', label, 'expected %d, found %d — replacing all' % (count, n)))
    s = s.replace(old, new)
    log.append(('OK', label, ''))

# 1 — FONTS: add Cormorant weight 300 upright + italic
repl(
 'family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400',
 'family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400',
 'fonts: add Cormorant 300')

# 2 — TOKENS: add --gold-line + --glow inside :root
repl(
 '  --gold-dim: rgba(201,152,60,0.12);\n  --text: #1e1a16;',
 '  --gold-dim: rgba(201,152,60,0.12);\n  --gold-line: #b8945f;\n  --glow: rgba(201,152,60,0.15);\n  --text: #1e1a16;',
 'tokens: --gold-line + --glow')

# 3 — DARK THEME block after :root close
repl(
 "  --font-body: 'DM Sans', system-ui, sans-serif;\n}\n",
 "  --font-body: 'DM Sans', system-ui, sans-serif;\n}\n"
 '[data-theme="dark"] {\n'
 '  --bg: #14100b;\n'
 '  --surface: #1c1712;\n'
 '  --surface2: #261f17;\n'
 '  --border: #322a20;\n'
 '  --border2: #3f3527;\n'
 '  --gold: #d4af6a;\n'
 '  --gold-light: #e6c485;\n'
 '  --gold-dark: #c9a978;\n'
 '  --gold-dim: rgba(212,175,106,0.14);\n'
 '  --gold-line: #8a6e44;\n'
 '  --glow: rgba(212,175,106,0.18);\n'
 '  --text: #f0e9dc;\n'
 '  --text2: #c9bda8;\n'
 '  --text3: #9a8d77;\n'
 '}\n',
 'dark theme block')

# 4 — BODY transition (smooth theme swap)
repl(
 'body { background: var(--bg); font-family: var(--font-body); color: var(--text); min-height: 100vh; display: flex; justify-content: center; padding-bottom: 80px; }',
 'body { background: var(--bg); font-family: var(--font-body); color: var(--text); min-height: 100vh; display: flex; justify-content: center; padding-bottom: 80px; transition: background .35s ease, color .35s ease; }',
 'body transition')

# 5 — .app position:relative (theme toggle anchor)
repl(
 '.app { width: 100%; max-width: 420px; padding: 0 20px; }',
 '.app { width: 100%; max-width: 420px; padding: 0 20px; position: relative; }',
 '.app position:relative')

# 6 — HERO headline: 54px / weight 300 / drop nowrap
repl(
 '.hero-headline { font-family: var(--font-display); font-size: 46px; line-height: 1.1; color: var(--text); font-weight: 400; font-style: italic; margin-bottom: 14px; white-space: nowrap; }',
 '.hero-headline { font-family: var(--font-display); font-size: 54px; line-height: 1.08; color: var(--text); font-weight: 300; font-style: italic; margin-bottom: 14px; }',
 'hero headline fix')

# 7 — Spotlit / corners / theme-toggle / ds-scroller CSS (before </style>)
CSS = """
/* ── SPOTLIT FRAME + HAIRLINE CORNERS ── */
.spotlit { position: relative; background:
  radial-gradient(ellipse 70% 60% at 50% 40%, var(--glow), transparent 70%), var(--surface); }
.corner { position: absolute; width: 15px; height: 15px; pointer-events: none; z-index: 2; }
.corner::before, .corner::after { content: ''; position: absolute; background: var(--gold-line); }
.corner::before { width: 15px; height: 1px; }
.corner::after { width: 1px; height: 15px; }
.corner.tl { top: 9px; left: 9px; } .corner.tl::before { top: 0; left: 0; } .corner.tl::after { top: 0; left: 0; }
.corner.tr { top: 9px; right: 9px; } .corner.tr::before { top: 0; right: 0; } .corner.tr::after { top: 0; right: 0; }
.corner.bl { bottom: 9px; left: 9px; } .corner.bl::before { bottom: 0; left: 0; } .corner.bl::after { bottom: 0; left: 0; }
.corner.br { bottom: 9px; right: 9px; } .corner.br::before { bottom: 0; right: 0; } .corner.br::after { bottom: 0; right: 0; }
/* ── THEME TOGGLE ── */
.theme-toggle { position: absolute; top: 14px; right: 4px; width: 34px; height: 34px; border-radius: 50%;
  border: 1px solid var(--border2); background: var(--surface); color: var(--gold-dark); cursor: pointer;
  display: flex; align-items: center; justify-content: center; font-size: 15px; z-index: 20;
  transition: border-color .2s, background .2s; font-family: var(--font-body); }
.theme-toggle:hover { border-color: var(--gold); }
/* ── DAILY STONE 12-SIGN SCROLLER ── */
.ds-scroller { display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; margin-bottom: 18px; }
.ds-sign { flex: 0 0 calc(16.66% - 6px); border: 1px solid var(--border); background: var(--surface);
  border-radius: var(--radius-sm); padding: 8px 2px; cursor: pointer; display: flex; flex-direction: column;
  align-items: center; gap: 3px; transition: all .15s; }
.ds-sign:hover { border-color: var(--gold); }
.ds-sign.active { border-color: var(--gold); background: var(--gold-dim); }
.ds-glyph { font-size: 16px; color: var(--gold-dark); line-height: 1; }
.ds-signname { font-size: 8.5px; letter-spacing: .03em; color: var(--text3); text-transform: uppercase; }
.ds-sign.active .ds-signname { color: var(--text2); }
</style>"""
repl('</style>', CSS, 'spotlit/corner/toggle/scroller CSS')

# 8 — THEME TOGGLE button after <div class="app">
repl(
 '<div class="app">\n',
 '<div class="app">\n'
 '<button class="theme-toggle" id="theme-toggle" onclick="toggleTheme()" title="Switch theme" aria-label="Switch theme">\u2600</button>\n',
 'theme toggle button')

# 9 — UPLOAD ZONE: spotlit + corners
repl(
 '  <div class="upload-zone" id="upload-zone" onclick="document.getElementById(\'fi\').click()" ondragover="event.preventDefault()" ondrop="handleDrop(event)">\n    <div id="upload-idle">',
 '  <div class="upload-zone spotlit" id="upload-zone" onclick="document.getElementById(\'fi\').click()" ondragover="event.preventDefault()" ondrop="handleDrop(event)">\n'
 '    <span class="corner tl"></span><span class="corner tr"></span><span class="corner bl"></span><span class="corner br"></span>\n'
 '    <div id="upload-idle">',
 'upload zone spotlit')

# 10 — RESULTS IMAGE: spotlit + corners
repl(
 '    <div class="img-wrap">\n      <img id="prev-img" class="preview" alt="Your jewellery piece"/>',
 '    <div class="img-wrap spotlit">\n'
 '      <span class="corner tl"></span><span class="corner tr"></span><span class="corner bl"></span><span class="corner br"></span>\n'
 '      <img id="prev-img" class="preview" alt="Your jewellery piece"/>',
 'results image spotlit')

# 11 — COMPARE SLOT A + B: spotlit + corners
repl(
 '      <div class="compare-slot" id="cslot-a" onclick="document.getElementById(\'cfi-a\').click()">\n        <svg',
 '      <div class="compare-slot spotlit" id="cslot-a" onclick="document.getElementById(\'cfi-a\').click()">\n'
 '        <span class="corner tl"></span><span class="corner tr"></span><span class="corner bl"></span><span class="corner br"></span>\n        <svg',
 'compare slot A spotlit')
repl(
 '      <div class="compare-slot" id="cslot-b" onclick="document.getElementById(\'cfi-b\').click()">\n        <svg',
 '      <div class="compare-slot spotlit" id="cslot-b" onclick="document.getElementById(\'cfi-b\').click()">\n'
 '        <span class="corner tl"></span><span class="corner tr"></span><span class="corner bl"></span><span class="corner br"></span>\n        <svg',
 'compare slot B spotlit')

# 12 — CHIPS: strip emoji -> plain text
chip_map = [
 ("\U0001f48d Ring", "Ring"), ("\u2b55 Bangle", "Bangle"),
 ("\U0001f4ff Bracelet", "Bracelet"), ("\U0001faac Necklace", "Necklace"),
 ("\u2728 Earrings", "Earrings"), ("\U0001f52e Pendant", "Pendant"),
 ("\U0001f9b6 Anklet", "Anklet"), ("\U0001f4cc Brooch", "Brooch"),
 ("\U0001fab7 Hair Jewellery", "Hair Jewellery"), ("\U0001f338 Nose Ring", "Nose Ring"),
 ("\U0001f48e Loose Gemstone", "Loose Gemstone"), ("\uff0b Other", "Other"),
]
for emo, plain in chip_map:
    repl('>' + emo + '</div>', '>' + plain + '</div>', 'chip: ' + plain)

# 13 — SAMPLES REORDER: move sample-section below the Analyse button
start_marker = '  <div class="sample-section">'
end_marker = 'See what JewelLens can identify \u2014 no upload needed</p>\n  </div>\n'
si = s.find(start_marker)
ei = s.find(end_marker)
if si != -1 and ei != -1:
    block = s[si:ei + len(end_marker)]
    s = s[:si] + s[si + len(block):]            # remove from top
    anchor = '  <button class="analyse-btn" id="analyse-btn" disabled onclick="startAnalysis()">Upload a photo &amp; select product type</button>\n  <div class="spacer"></div>\n'
    if anchor in s:
        s = s.replace(anchor, anchor + '\n' + block, 1)
        log.append(('OK', 'samples reorder', 'moved below Analyse button'))
    else:
        s = s[:si] + block + s[si:]              # put back if anchor missing
        log.append(('MISS', 'samples reorder', 'analyse-btn anchor not found — reverted'))
else:
    log.append(('MISS', 'samples reorder', 'sample-section block not found'))

# 14 — DAILY STONE: ZODIAC_ORDER + ZODIAC_GLYPHS + peekSign + scroller in render
repl(
 "var ZODIAC_ELEMENTS={'Aries':'Fire'",
 "var ZODIAC_ORDER=['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];\n"
 "var ZODIAC_GLYPHS={'Aries':'\u2648','Taurus':'\u2649','Gemini':'\u264a','Cancer':'\u264b','Leo':'\u264c','Virgo':'\u264d','Libra':'\u264e','Scorpio':'\u264f','Sagittarius':'\u2650','Capricorn':'\u2651','Aquarius':'\u2652','Pisces':'\u2653'};\n"
 "function peekSign(sign){ showDailyStone(sign); }\n"
 "var ZODIAC_ELEMENTS={'Aries':'Fire'",
 'daily stone: order/glyphs/peekSign')

# inject scroller HTML at top of showDailyStone render
repl(
 "  var el=document.getElementById('ds-result');\n  el.innerHTML='<div class=\"ds-card\">",
 "  var el=document.getElementById('ds-result');\n"
 "  var scroller='<div class=\"ds-scroller\">';\n"
 "  for(var zi=0;zi<ZODIAC_ORDER.length;zi++){var zs=ZODIAC_ORDER[zi];scroller+='<button class=\"ds-sign'+(zs===sign?' active':'')+'\" onclick=\"peekSign(\\''+zs+'\\')\"><span class=\"ds-glyph\">'+ZODIAC_GLYPHS[zs]+'</span><span class=\"ds-signname\">'+zs+'</span></button>';}\n"
 "  scroller+='</div>';\n"
 "  el.innerHTML=scroller+'<div class=\"ds-card\">",
 'daily stone: scroller render')

# 15 — THEME functions + boot restore (button onclick target)
repl(
 "(function(){ try{ var el=document.getElementById('api-key'); if(el&&_apiKey){ el.value=_apiKey; document.getElementById('key-status').textContent='\u2713 Key loaded'; } }catch(e){} })();\n",
 "(function(){ try{ var el=document.getElementById('api-key'); if(el&&_apiKey){ el.value=_apiKey; document.getElementById('key-status').textContent='\u2713 Key loaded'; } }catch(e){} })();\n"
 "\n/* \u2500\u2500 THEME \u2500\u2500 */\n"
 "function applyTheme(t){\n"
 "  if(t==='dark'){ document.documentElement.setAttribute('data-theme','dark'); }\n"
 "  else { document.documentElement.removeAttribute('data-theme'); }\n"
 "  var b=document.getElementById('theme-toggle');\n"
 "  if(b){ b.textContent=(t==='dark'?'\u263e':'\u2600'); b.title=(t==='dark'?'Switch to light':'Switch to dark'); }\n"
 "}\n"
 "function toggleTheme(){\n"
 "  var cur=document.documentElement.getAttribute('data-theme')==='dark'?'dark':'light';\n"
 "  var next=cur==='dark'?'light':'dark';\n"
 "  _set('jl_theme',next); applyTheme(next);\n"
 "}\n"
 "(function(){ try{ applyTheme(_get('jl_theme')==='dark'?'dark':'light'); }catch(e){} })();\n",
 'theme functions + boot restore')

# write
f = open('index.html', 'w', encoding='utf-8'); f.write(s); f.close()

print('CHANGED %d bytes -> %d bytes\n' % (len(orig), len(s)))
miss = 0
for status, label, note in log:
    print('  [%s] %s%s' % (status, label, ('  -- ' + note) if note else ''))
    if status == 'MISS': miss += 1
print('\n%d edits, %d MISالسES' % (len(log), miss) if False else '\n%d edits, %d misses' % (len(log), miss))
sys.exit(1 if miss else 0)
