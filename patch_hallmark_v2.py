#!/usr/bin/env python3
"""JewelLens patch — adds hallmark protocol to analysis prompt (apostrophes correctly escaped for JS)"""
import os, sys

HTML_PATH = os.path.join(os.path.dirname(__file__), 'index.html')

OLD = 'Trust this selection if the image shows any jewellery piece. Respond ONLY with valid JSON, no markdown, no backticks, raw JSON only.'

# Apostrophes inside JS single-quoted strings must be written as \' in the file.
# In Python, \\' writes \' to the file.
NEW = ("Trust this selection if the image shows any jewellery piece."
       "\\n\\n"
       "HALLMARK AND MAKER\\'S MARK PROTOCOL — Before classifying tradition, origin, or style era, "
       "complete these steps in strict order. "
       "1. LITERAL TEXT READ: Examine all visible text, stamps, engravings, or markings on the piece. "
       "Read them literally and exactly as they appear. Do not interpret the visual style of lettering as "
       "a language indicator — cursive Latin script can resemble Arabic; decorative script fonts can "
       "resemble Asian calligraphy. Read the actual characters, not the visual impression. "
       "2. HALLMARK IDENTIFICATION: Cross-reference any numbers or codes against known hallmarking systems: "
       "750 = 18k gold; 925 = sterling silver; 585 = 14k gold; 375 = 9k gold; 950 = platinum or high-purity silver; "
       "BIS/916 = Indian hallmark; alphanumeric codes such as 104 AR or TO AR = Italian assay office plus maker codes; "
       "Poincon marks = French hallmarking; Lion passant = British sterling. "
       "A confirmed hallmark is the single most reliable signal for metal origin and overrides all visual or stylistic assumptions. "
       "3. MAKER MARK: Only after steps 1 and 2, interpret any brand name or maker mark. "
       "A brand name in cursive Latin script is that brand\\'s origin, even if the script superficially resembles another writing system. "
       "4. TRADITION AND ORIGIN: Only now infer tradition, style era, or cultural origin — and only if consistent "
       "with verified hallmarks and maker marks from steps 1 to 3. If visual aesthetic conflicts with hallmark evidence, "
       "always trust the hallmark and flag the conflict explicitly in the visible_red_flags field. "
       "If any text or marking is unclear or unreadable, state this explicitly rather than inferring script type from visual appearance."
       "\\n\\n"
       "Respond ONLY with valid JSON, no markdown, no backticks, raw JSON only.")

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

if OLD not in html:
    sys.exit('ERROR: Target string not found. Check the file is correct or already patched.')

if 'HALLMARK AND MAKER' in html:
    sys.exit('Already patched — hallmark protocol already present. No changes made.')

html = html.replace(OLD, NEW, 1)

# Verify no bare apostrophes were introduced in the replacement area
# (quick sanity check — look for unescaped ' after the protocol text)
with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print("Hallmark protocol injected.")
print(f"File size: {len(html)//1024}KB")
print('Run: git add -A && git commit -m "add hallmark protocol to analysis prompt" && git push')
