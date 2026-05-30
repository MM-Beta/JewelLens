#!/usr/bin/env python3
# JewelLens — Daily Stone TRIM (against index__3 + cleanup)
# Converts the zodiac/element "personal reading" into a factual one-stone-per-day
# almanac (navratna planetary day-stone, history + how-worn). No horoscope, no
# sign picker, no scroller, no affirmation. Lowest-risk approach: replace only
# DAY_DATA, the initDailyStone branch, showDailyStone, and the screen subtitle.
# Old zodiac functions/markup are left in place but never called (picker is
# display:none and we no longer activate it).
import sys
s = open('index.html', encoding='utf-8').read()
orig = s
log = []

NEW_DATA = """var DAY_DATA=[
  {planet:'Sun',stone:'Ruby',emoji:'\U0001F534',color:'#c0392b',lore:'In the Vedic navratna tradition the ruby is the gem of the Sun, and Burmese pigeon-blood stones were prized across the Mughal and Burmese courts. Roman scholars called the stone carbunculus, imagining an inner flame as the source of its glow.',wear:'Traditionally set in gold and worn on the ring finger. At 9 on the Mohs hardness scale it stands up well to everyday wear.'},
  {planet:'Moon',stone:'Pearl',emoji:'\u26AA',color:'#cfd8dc',lore:'Long associated with the Moon, natural pearls ranked among the most valuable gems on earth before cultured pearls arrived in the early twentieth century. The waters of the Persian Gulf and Basra were the great historic pearling grounds.',wear:'Soft and organic at around 3 on the Mohs scale, so keep pearls away from perfume and acids and store them in a soft pouch. Classically strung as a strand or set in white metal.'},
  {planet:'Mars',stone:'Red Coral',emoji:'\U0001FAB8',color:'#e8562a',lore:'Mediterranean red coral has been traded since antiquity and is tied to Mars in the navratna system, with the Italian town of Torre del Greco as its historic cutting centre. It is organic rather than mineral, formed from the skeleton of a marine colony.',wear:'Porous and soft, so keep it away from heat, acids and household chemicals. It is traditionally set in silver or gold and worn on the ring finger.'},
  {planet:'Mercury',stone:'Emerald',emoji:'\U0001F49A',color:'#1e8449',lore:'Emerald is the navratna gem of Mercury, and the Muzo and Chivor mines of Colombia supplied the celebrated stones of the Mughal and Spanish colonial eras. Egyptian mines linked to Cleopatra were worked for emerald far earlier still.',wear:'Most emeralds carry natural inclusions and can be brittle, so they should never be cleaned in an ultrasonic bath, only with warm soapy water. Protective settings help guard the edges.'},
  {planet:'Jupiter',stone:'Yellow Sapphire',emoji:'\U0001F49B',color:'#e8c200',lore:'Yellow sapphire, known as pukhraj, is the navratna stone of Jupiter and one of the most sought gems in South Asian tradition. Sri Lanka, historically called Ceylon, has been its celebrated source for over two thousand years.',wear:'Very hard and durable at 9 on the Mohs scale, it suits daily wear and is classically set in gold.'},
  {planet:'Venus',stone:'Diamond',emoji:'\U0001F48E',color:'#aab7c4',lore:'Diamond is the navratna gem of Venus, and the Golconda mines of India were the only major world source until the eighteenth century, producing legendary stones such as the Koh-i-Noor. The name comes from the Greek adamas, meaning unconquerable.',wear:'The hardest natural material at 10 on the Mohs scale, though a sharp knock can still chip it. Clean with warm soapy water and a soft brush.'},
  {planet:'Saturn',stone:'Blue Sapphire',emoji:'\U0001F535',color:'#1a3a9f',lore:'Blue sapphire, called neelam, is the navratna gem of Saturn and was historically treated with caution as the fastest-acting stone in the tradition. The Kashmir sapphires found in the 1880s set the global benchmark for colour.',wear:'Hard and durable at 9 on the Mohs scale. It is traditionally set in silver or white gold.'}
];
"""

NEW_SHOW = """function showDailyStone(){
  var day=new Date().getDay();
  var d=DAY_DATA[day];
  var el=document.getElementById('ds-result');
  el.innerHTML='<div class="ds-card"><div class="ds-stone-circle" style="background:'+d.color+'22;border:2px solid '+d.color+'40"><span style="font-size:36px">'+d.emoji+'</span></div><p class="ds-stone-name">'+d.stone+'</p><p class="ds-stone-meta">'+DAY_NAMES[day]+' \u00b7 gem of '+d.planet+'</p><p class="ds-stone-why">'+d.lore+'</p></div><div class="ds-section"><p class="ds-section-label">\u2726 How it is worn</p><p class="ds-section-text">'+d.wear+'</p></div><div class="ds-section"><p class="ds-section-label">\u2726 The planetary link</p><p class="ds-section-text">In the navratna tradition, <strong>'+d.stone+'</strong> is the gem of <strong>'+d.planet+'</strong>, the planet that rules '+DAY_NAMES[day]+'.</p></div>';
  el.classList.remove('hidden');
}
"""

# 1) Replace the whole DAY_DATA array (slice from its start to start of DAY_NAMES)
a = s.find('var DAY_DATA=[')
b = s.find('var DAY_NAMES=', a)
if a == -1 or b == -1:
    log.append(('MISS', 'DAY_DATA array', 'anchors not found'))
else:
    s = s[:a] + NEW_DATA + s[b:]
    log.append(('OK', 'DAY_DATA -> 7 flat factual entries', ''))

# 2) initDailyStone: show today's stone directly (no sign picker)
old_branch = ("  if(_confirmedSign){ showDailyStone(_confirmedSign); }\n"
              "  else{ document.getElementById('ds-sign-picker').classList.add('visible'); }")
if s.count(old_branch) == 1:
    s = s.replace(old_branch, "  showDailyStone();")
    log.append(('OK', 'initDailyStone -> direct render', ''))
else:
    log.append(('MISS', 'initDailyStone branch', 'found %d' % s.count(old_branch)))

# 3) Replace showDailyStone(sign){...} (slice to start of getPlanetNote)
a = s.find('function showDailyStone(sign){')
b = s.find('function getPlanetNote(planet){', a)
if a == -1 or b == -1:
    log.append(('MISS', 'showDailyStone fn', 'anchors not found'))
else:
    s = s[:a] + NEW_SHOW + '\n' + s[b:]
    log.append(('OK', 'showDailyStone -> no-sign factual render', ''))

# 4) Subtitle: drop the "personal reading" framing
old_sub = '<p class="screen-sub">Your personal gemstone reading — updated every day.</p>'
new_sub = '<p class="screen-sub">A stone for each day of the week — and the history behind it.</p>'
if s.count(old_sub) == 1:
    s = s.replace(old_sub, new_sub); log.append(('OK', 'subtitle reworded', ''))
else:
    log.append(('MISS', 'subtitle', 'found %d' % s.count(old_sub)))

open('index.html', 'w', encoding='utf-8').write(s)
miss = sum(1 for x in log if x[0] == 'MISS')
print('%d -> %d bytes\n' % (len(orig), len(s)))
for st, lbl, note in log: print('  [%s] %s%s' % (st, lbl, ('  -- ' + note) if note else ''))
print('\n%d edits, %d misses' % (len(log), miss))
sys.exit(1 if miss else 0)
