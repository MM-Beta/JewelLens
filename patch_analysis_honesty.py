#!/usr/bin/env python3
# JewelLens - Analysis honesty rewrite (Patch #1)
# Observation/inference discipline + diagnostics, in the MAIN analysis prompt (line ~1239),
# plus a no-invented-carats guard on the Vendor brief chip (line ~1827).
# Anchors verified unique against index__3_.html.
import sys
s = open('index.html', encoding='utf-8').read()
orig = s
log = []

DISCIPLINE = (
 "You are examining PHOTOGRAPHS, not the physical object. Be confident about what the image shows "
 "and explicit about what it cannot. Classify every material claim as observed, inferred, or undetermined, "
 "and word the output to match - never present an inference or an unknown as fact. NEVER describe observations "
 "a photo cannot support: do not claim magnification, loupe, microscopic, or under-magnification inspection unless "
 "an actual close-up or hallmark image is provided. Do not assert metal karat or fineness without a legible hallmark "
 "visible in the image; if none is visible, describe the metal colour and say purity is not determinable from a photo. "
 "For coloured stones, name the most likely identity and the visual look-alikes that cannot be excluded (for example a "
 "red stone consistent with ruby, with spinel, garnet, glass or synthetic not excludable); for small pave or melee do not "
 "state precise cut grades. Never invent or estimate carat or gram weights; give approximate visible dimensions only if a "
 "scale reference is present, otherwise say weight is not determinable from a photo. Flag a treatment only when there is "
 "visible evidence; general industry expectations may be mentioned but must be labelled as general knowledge, not observation. "
 "For visible_red_flags, actively look for tells a photo can show: gas bubbles in stones, doublet or triplet seams, wear "
 "exposing base metal under plating, open or foiled stone backs, glued or uneven settings, mismatched solder. Set "
 "metal_confidence and origin_confidence honestly, and stay humble on purity, stone identity, treatment and authenticity "
 "while remaining confident on design, construction, era and tradition. "
)

reps = [
 # 1. Inject discipline rules into the main prompt
 ("Trust this selection if the image shows any jewellery piece. Respond ONLY with valid JSON",
  "Trust this selection if the image shows any jewellery piece. " + DISCIPLINE + "Respond ONLY with valid JSON",
  "discipline-block"),
 # 2. Metal field hint - stop instructing it to assert a karat
 ('"metal":"specific e.g. 22-karat yellow gold or Sterling silver 925"',
  '"metal":"describe the visible metal colour and tone; state a karat or fineness ONLY if a legible hallmark or stamp is visible in the image, otherwise say for example yellow-toned metal consistent with gold and that purity is not determinable from a photo"',
  "metal-hint"),
 # 3. natural_vs_lab - forbid fake magnification, require look-alikes + lab caveat
 ('"natural_vs_lab":"Honest visual assessment with uncertainty caveat"',
  '"natural_vs_lab":"Honest visual assessment from the photo only; never claim magnification or microscopic inspection; name look-alikes that cannot be excluded; state that lab testing is required for certainty"',
  "natural_vs_lab-hint"),
 # 4. cut_performance - no precise cut grades on melee
 ('"cut_performance":"For faceted stones only — visual assessment of light performance, or Not applicable"',
  '"cut_performance":"For faceted stones only — visual assessment of light performance from the photo; do not state precise cut grades for small pave or melee; or Not applicable"',
  "cut_performance-hint"),
 # 5. Vendor brief chip - no invented carats on top of the canonical object
 ("materials with quality markers, craftsmanship tradition if identifiable, and commercial tier.",
  "materials with quality markers, craftsmanship tradition if identifiable, and commercial tier. Do not invent or estimate carat or gram weights; if the analysis has no measurement, describe visible proportions and state that weights and purity require physical measurement and hallmarking.",
  "vendor-carat-guard"),
]

for old, new, label in reps:
    n = s.count(old)
    if n != 1:
        print("ABORT: anchor '%s' found %d times (expected 1). No changes written." % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    log.append(label)

if s == orig:
    print("ABORT: nothing changed.")
    sys.exit(1)

open('index.html', 'w', encoding='utf-8').write(s)
print("OK - applied:", ", ".join(log))
print("bytes %d -> %d" % (len(orig), len(s)))
