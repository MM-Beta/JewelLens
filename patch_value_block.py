#!/usr/bin/env python3
# JewelLens — Value Block patch
# - resale_signal -> smart per-piece value_factors block (no price, ever)
# - merge Natural vs Lab + Surface -> one "Treatments & Origin" row
# - Cut Performance shown only when applicable
# - Confidence shown as a word (Strong/Good/Limited), bar unchanged
# - Style tags trimmed to distinctive few; no price anywhere incl .txt export
import sys
s = open('index.html', encoding='utf-8').read()
orig = s
log = []
def repl(old, new, label):
    global s
    if s.count(old) != 1:
        log.append(('MISS', label, 'found %d (need 1)' % s.count(old))); return
    s = s.replace(old, new); log.append(('OK', label, ''))

# 1 — PROMPT: resale_signal -> value_factors object
repl(
 '"resale_signal":"one factual sentence",',
 '"value_factors":{"drivers":"the one or two things that most drive THIS specific piece\'s value","demand":"current demand or liquidity for this category, one short phrase","raises":"what would raise its value","lowers":"what would lower its value"},',
 'prompt: value_factors field')

# 2 — PROMPT: trim style tags to distinctive few
repl(
 '"style_tags":["tag"],',
 '"style_tags":["up to 5 distinctive tags using era, tradition, technique or motif — never generic filler such as gold earrings or statement piece"],',
 'prompt: distinctive style tags')

# 3 — PROMPT: hard no-price rule
repl(
 'raw JSON only.\\n\\n{',
 'raw JSON only. Never state or estimate any price, monetary value, or retail figure in any field — JewelLens never prices pieces; describe what affects value instead.\\n\\n{',
 'prompt: no-price rule')

# 4 — value-cell helpers, injected before renderResults
HELPERS = r'''function jlStripPrice(t){ return (t||'').replace(/[₹$€£]\s?[\d,]+\s*([-–to]+\s*[₹$€£]?\s?[\d,]+)?\+?/g,'').replace(/\bretail(ing|s)?\b/gi,'').replace(/\s{2,}/g,' ').replace(/\s+([.,;])/g,'$1').trim(); }
function jlValueCell(r){
  var vf=r.value_factors;
  if(vf&&(vf.drivers||vf.raises||vf.lowers||vf.demand)){
    var p=[];
    if(vf.drivers)p.push(vf.drivers);
    if(vf.demand)p.push('<strong>Demand:</strong> '+vf.demand);
    if(vf.raises)p.push('<strong>Raises value:</strong> '+vf.raises);
    if(vf.lowers)p.push('<strong>Lowers value:</strong> '+vf.lowers);
    p.push('<em style="color:var(--text3)">JewelLens won\'t guess a price — values swing too much. For a real figure, use a GIA-listed jeweller.</em>');
    return p.join('<br>');
  }
  return jlStripPrice(r.resale_signal||'');
}
function renderResults(r){'''
repl('function renderResults(r){', HELPERS, 'value-cell helpers')

# 5 — CONFIDENCE: percentage -> word
repl(
 "document.getElementById('p-conf-pct').textContent=score+'%';",
 "document.getElementById('p-conf-pct').textContent=(score>=80?'Strong':(score>=60?'Good':'Limited'));",
 'confidence -> word')

# 6 — DETAIL ROWS: rebuild (conditional cut perf, merged treatments, value block)
OLD_ROWS = """  var rows=[
    ['Metal',(r.metal||'')+(r.metal_confidence==='low'?' (approx.)':'')],
    ['Construction',r.construction_method||''],
    ['Stones',r.stones?r.stones.map(function(s){ return s.name+(s.cut?' · '+s.cut:''); }).join(', '):'None'],
    ['Cut Performance',r.cut_performance||'—'],
    ['Natural vs Lab',r.natural_vs_lab||'—'],
    ['Surface',r.surface_treatment||''],
    ['Style Era',r.style_era||''],
    ['Tradition',r.craftsmanship_tradition||''],
    ['Tier','<span class="tier-pill tier-'+(r.tier||'fashion')+'">'+(r.tier||'fashion').charAt(0).toUpperCase()+(r.tier||'fashion').slice(1)+'</span>'],
    ['Resale Signal',r.resale_signal||'']
  ];"""
NEW_ROWS = r'''  var rows=[
    ['Metal',(r.metal||'')+(r.metal_confidence==='low'?' (approx.)':'')],
    ['Construction',r.construction_method||''],
    ['Stones',r.stones?r.stones.map(function(s){ return s.name+(s.cut?' · '+s.cut:''); }).join(', '):'None']
  ];
  if(r.cut_performance && !/^\s*not applicable/i.test(r.cut_performance)) rows.push(['Cut Performance',r.cut_performance]);
  var _treat=[r.natural_vs_lab,r.surface_treatment].filter(Boolean).join(' ');
  if(_treat) rows.push(['Treatments & Origin',_treat+' <em style="color:var(--text3)">(visual estimate)</em>']);
  rows.push(['Style Era',r.style_era||'']);
  rows.push(['Tradition',r.craftsmanship_tradition||'']);
  rows.push(['Tier','<span class="tier-pill tier-'+(r.tier||'fashion')+'">'+(r.tier||'fashion').charAt(0).toUpperCase()+(r.tier||'fashion').slice(1)+'</span>']);
  rows.push(['What Affects Value',jlValueCell(r)]);'''
repl(OLD_ROWS, NEW_ROWS, 'detail rows rebuild')

# 7 — STYLE TAGS: cap at 6
repl(
 "document.getElementById('p-tags').innerHTML=(r.style_tags||[]).map(",
 "document.getElementById('p-tags').innerHTML=(r.style_tags||[]).slice(0,6).map(",
 'style tags cap')

# 8 — .TXT EXPORT: drop price, use value drivers
repl(
 "    'Resale: '+r.resale_signal,'',",
 "    'Value: '+(r.value_factors&&r.value_factors.drivers?r.value_factors.drivers:jlStripPrice(r.resale_signal||'')),'',",
 'txt export: value, no price')

open('index.html', 'w', encoding='utf-8').write(s)
miss = sum(1 for x in log if x[0] == 'MISS')
print('%d -> %d bytes\n' % (len(orig), len(s)))
for st, lbl, note in log:
    print('  [%s] %s%s' % (st, lbl, ('  -- ' + note) if note else ''))
print('\n%d edits, %d misses' % (len(log), miss))
sys.exit(1 if miss else 0)
