#!/usr/bin/env python3
# JewelLens — HOTFIX: an unescaped apostrophe in "piece's" closed the single-quoted
# prompt string early, throwing a SyntaxError that broke the entire <script> block
# (so handleFile became undefined and uploads stopped working).
# Fix: reword to remove the apostrophe entirely.
import sys
s = open('index.html', encoding='utf-8').read()
orig = s
old = "the one or two things that most drive THIS specific piece's value"
new = "the one or two things that most affect the value of this specific piece"
n = s.count(old)
if n != 1:
    print("MISS: found %d occurrences (need exactly 1) — stop, do not push." % n)
    sys.exit(1)
s = s.replace(old, new)
open('index.html', 'w', encoding='utf-8').write(s)
print("%d -> %d bytes\n  [OK] removed stray apostrophe in value_factors prompt\n\n1 edit, 0 misses" % (len(orig), len(s)))
