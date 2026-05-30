#!/usr/bin/env python3
# JewelLens — cleanup patch (against index__3 real file)
# (a) Treatments & Origin: separate the two merged sentences with a line break
# (b) Compare tab: "Maang Tikka" -> "Hair Jewellery" (consistent global label)
# (c) Cut style tags: stop rendering them + drop from prompt (nothing uses them)
import sys
s = open('index.html', encoding='utf-8').read()
orig = s; log = []
def repl(old, new, label, expect=1):
    global s
    n = s.count(old)
    if n != expect:
        log.append(('MISS', label, 'found %d (need %d)' % (n, expect))); return
    s = s.replace(old, new); log.append(('OK', label, ''))

# (a) readable separator between natural_vs_lab and surface_treatment
repl(
 "var _treat=[r.natural_vs_lab,r.surface_treatment].filter(Boolean).join(' ');",
 "var _treat=[r.natural_vs_lab,r.surface_treatment].filter(Boolean).join('<br>');",
 'treatments: line-break separator')

# (b) Maang Tikka -> Hair Jewellery in BOTH compare dropdowns
repl('<option>Maang Tikka</option>', '<option>Hair Jewellery</option>',
     'compare: Maang Tikka -> Hair Jewellery', expect=2)

# (c1) stop rendering tags (hide the container so no gap is left)
repl(
 'document.getElementById(\'p-tags\').innerHTML=(r.style_tags||[]).slice(0,6).map(function(t){ return \'<span class="tag">\'+t+\'</span>\'; }).join(\'\');',
 '(function(pt){ if(pt){ pt.innerHTML=\'\'; pt.style.display=\'none\'; } })(document.getElementById(\'p-tags\'));',
 'tags: stop rendering + hide')

# (c2) drop style_tags from the prompt (no longer used)
repl(
 '"style_tags":["up to 5 distinctive tags using era, tradition, technique or motif — never generic filler such as gold earrings or statement piece"],',
 '',
 'prompt: drop style_tags')

open('index.html', 'w', encoding='utf-8').write(s)
miss = sum(1 for x in log if x[0] == 'MISS')
print('%d -> %d bytes\n' % (len(orig), len(s)))
for st, lbl, note in log: print('  [%s] %s%s' % (st, lbl, ('  -- ' + note) if note else ''))
print('\n%d edits, %d misses' % (len(log), miss))
sys.exit(1 if miss else 0)
