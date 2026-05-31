#!/usr/bin/env python3
# JewelLens - Patch #1b (applies on top of patch_analysis_honesty.py / #1a)
# 1) Tier -> workmanship tier, no material-based inflation (fixes FINE->LUXURY drift)
# 2) Vendor brief -> karat buyer-specified, 5-10 qty, labelled-estimate-only carats
# 3) Stone alternatives -> cap length (fixes 800-token truncation -> JSON parse error)
# 4) Raise maxTok for Stone alternatives so it has room
import sys
s = open('index.html', encoding='utf-8').read()
orig = s
log = []

reps = [
 # 1. TIER (main prompt only; anchor includes ',"value_factors"' so it does NOT match the Compare prompt)
 ('"tier":"fashion or fine or luxury","value_factors"',
  '"tier":"fashion or fine or luxury — judge ONLY by visible construction and design quality as a workmanship tier; assume nothing about whether stones are natural or the metal is solid, and do not inflate the tier on the assumption of genuine materials","value_factors"',
  "tier-workmanship"),

 # 2. VENDOR BRIEF clause (replaces the #1a carat clause + tail)
 ("Do not invent or estimate carat or gram weights; if the analysis has no measurement, describe visible proportions and state that weights and purity require physical measurement and hallmarking. Include any specific requirements the user mentions. Use professional B2B trade language only. No consumer-facing styling language.",
  "You may give an approximate centre-stone size only if it is clearly labelled as a visual estimate to be confirmed; never state exact carat or gram weights as known, and require the manufacturer to confirm all weights, dimensions and purity in their technical specification. Do not state the metal karat as a known fact; if the analysis does not confirm purity, request the metal in a buyer-specified karat (for example 14K or 18K) rather than asserting one. State a minimum order quantity of 5 to 10 pieces or pairs and request FOB pricing and lead time; do not invent larger production-run figures. Include any specific requirements the user mentions. Use professional B2B trade language only. No consumer-facing styling language.",
  "vendor-karat-qty-carat"),

 # 3. STONE ALTERNATIVES brevity cap (anchor unique to that instruction)
 ("and note any practical consideration for the setter.",
  "and note any practical consideration for the setter. Keep the whole answer under 110 words: one short sentence per stone covering why it works plus one brief practical note.",
  "stonealt-brevity"),

 # 4. maxTok: give Stone alternatives room
 ("isVendor ? 1000 : 800;",
  "isVendor ? 1000 : (isStoneAlt ? 1300 : 800);",
  "stonealt-maxtok"),
]

for old, new, label in reps:
    n = s.count(old)
    if n != 1:
        print("ABORT: anchor '%s' found %d times (expected 1). No changes written." % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    log.append(label)

if s == orig:
    print("ABORT: nothing changed."); sys.exit(1)

open('index.html', 'w', encoding='utf-8').write(s)
print("OK - applied:", ", ".join(log))
print("bytes %d -> %d" % (len(orig), len(s)))
