#!/usr/bin/env python3
# JewelLens — Deploy 2 (testing-prep): hero glue, Find It search-term upgrade,
# Vercel Analytics + events, inline "Report a problem" capture.
import sys
s = open('index.html', encoding='utf-8').read()
orig = s
log = []
def repl(old, new, label):
    global s
    if s.count(old) != 1:
        log.append(('MISS', label, 'found %d (need 1)' % s.count(old))); return
    s = s.replace(old, new); log.append(('OK', label, ''))

# 1 — HERO: keep "a story." together (break before "a", not after)
repl(
 'Every piece has a <span class="story-word">story.</span>',
 'Every piece has a&nbsp;<span class="story-word">story.</span>',
 'hero: glue "a story."')

# 2 — FIND IT: demand specific, distinctive search phrases (maker/tradition/era)
repl(
 '"search_terms":{"pinterest":"search string","firstdibs":"search string","etsy":"search string"}',
 '"search_terms":{"pinterest":"a specific, distinctive phrase built from the identified tradition, era, materials and motif — never generic words like gold earrings","firstdibs":"a precise resale phrase naming the house or maker if identifiable, plus era, principal stone and metal","etsy":"a precise phrase blending the tradition, technique and materials that independent makers would actually tag"}',
 'find it: specific search-term instruction')

# 3 — ANALYTICS: Vercel Web Analytics script before </head>
repl(
 '</style>\n</head>',
 '</style>\n'
 '<script>window.va=window.va||function(){(window.vaq=window.vaq||[]).push(arguments);};</script>\n'
 '<script defer src="/_vercel/insights/script.js"></script>\n'
 '</head>',
 'analytics: vercel script')

# 3b — track() helper after config
repl(
 "var FEEDBACK_EMAIL='jewellensapp@gmail.com';",
 "var FEEDBACK_EMAIL='jewellensapp@gmail.com';\n"
 "function track(name,data){ try{ window.va && window.va('event',{name:name,data:data||{}}); }catch(e){} }",
 'analytics: track() helper')

# 3c — app_open event on boot (append to theme boot IIFE I added in Deploy 1)
repl(
 "(function(){ try{ applyTheme(_get('jl_theme')==='dark'?'dark':'light'); }catch(e){} })();",
 "(function(){ try{ applyTheme(_get('jl_theme')==='dark'?'dark':'light'); }catch(e){} })();\n"
 "(function(){ try{ track('app_open'); }catch(e){} })();",
 'analytics: app_open event')

# 3d — sample_viewed event inside loadSample
repl(
 'function loadSample(idx){\n  var s=SAMPLE_DATA[idx];\n  currentResult=s.json;',
 'function loadSample(idx){\n  var s=SAMPLE_DATA[idx];\n  currentResult=s.json;\n  track(\'sample_viewed\',{piece:s.type});',
 'analytics: sample_viewed event')

# 4 — REPORT A PROBLEM button + inline box, after the feedback button
repl(
 '        Suggest a feature or share feedback\n      </button>\n',
 '        Suggest a feature or share feedback\n      </button>\n'
 '      <button class="feedback-btn" onclick="reportWrong()">\n'
 '        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M12 9v4"/><path d="M12 17h.01"/><circle cx="12" cy="12" r="10"/></svg>\n'
 '        Report a problem with this analysis\n      </button>\n'
 '      <div id="wrong-box" class="hidden" style="margin-top:8px">\n'
 '        <textarea class="context-textarea" id="wrong-note" rows="2" maxlength="240" placeholder="What did JewelLens get wrong? e.g. metal is silver not gold &middot; wrong tradition &middot; not this stone"></textarea>\n'
 '        <button class="feedback-btn" style="margin-top:6px" onclick="submitWrong()">Send correction</button>\n'
 '        <p id="wrong-status" style="font-size:11px;color:var(--gold-dark);margin-top:6px"></p>\n'
 '      </div>\n',
 'report-a-problem button + box')

# 4b — reportWrong / submitWrong functions (after track helper)
repl(
 "function track(name,data){ try{ window.va && window.va('event',{name:name,data:data||{}}); }catch(e){} }",
 "function track(name,data){ try{ window.va && window.va('event',{name:name,data:data||{}}); }catch(e){} }\n"
 "function reportWrong(){ var b=document.getElementById('wrong-box'); if(b) b.classList.toggle('hidden'); }\n"
 "function submitWrong(){\n"
 "  var t=document.getElementById('wrong-note'); var note=(t&&t.value||'').trim();\n"
 "  var piece=(typeof currentResult!=='undefined'&&currentResult&&currentResult.piece_type)||'';\n"
 "  if(!note){ var st0=document.getElementById('wrong-status'); if(st0) st0.textContent='Add a quick note first.'; return; }\n"
 "  track('wrong_reported',{piece:piece,note:note.slice(0,90)});\n"
 "  var st=document.getElementById('wrong-status');\n"
 "  if(st){ st.innerHTML='Thank you \\u2014 noted. This is exactly what helps JewelLens improve. <a href=\"mailto:'+FEEDBACK_EMAIL+'?subject='+encodeURIComponent('JewelLens correction')+'&body='+encodeURIComponent('Piece: '+piece+'\\nWhat was wrong: '+note)+'\" style=\"color:var(--gold)\">Email the details too</a>'; }\n"
 "  if(t){ t.value=''; }\n"
 "}",
 'reportWrong/submitWrong functions')

open('index.html', 'w', encoding='utf-8').write(s)
miss = sum(1 for x in log if x[0] == 'MISS')
print('%d bytes -> %d bytes\n' % (len(orig), len(s)))
for st, lbl, note in log:
    print('  [%s] %s%s' % (st, lbl, ('  -- ' + note) if note else ''))
print('\n%d edits, %d misses' % (len(log), miss))
sys.exit(1 if miss else 0)
