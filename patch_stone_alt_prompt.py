#!/usr/bin/env python3
"""
JewelLens – Stone alternatives prompt fix
Changes the "Stone alternatives" chip instruction from cost-reduction
to design-compatibility language.

Run: python3 patch_stone_alt_prompt.py
Then: git add -A && git commit -m "fix: stone alternatives → design-compatible suggestion prompt" && git push
"""

SRC = 'index.html'

with open(SRC, encoding='utf-8') as f:
    src = f.read()

OLD = (
    "  var isVendor = (label === '\u2726 Vendor brief');\n"
    "  var maxTok   = isVendor ? 1000 : 800;\n"
    "\n"
    "  var instructions = isVendor\n"
    "    ? 'You are a senior jewellery trade buyer. Using the piece analysis provided, write one concise paragraph (4-6 sentences) suitable for forwarding to a manufacturer or supplier. Include: exact piece type, construction method, materials with quality markers, craftsmanship tradition if identifiable, and commercial tier. Include any specific requirements the user mentions. Use professional B2B trade language only. No consumer-facing styling language.'\n"
    "    : 'You are a jewellery expert. Answer only the specific question asked, using the piece analysis provided. Be concise (3-5 sentences), direct, and factual. Do not repeat the full analysis.';"
)

NEW = (
    "  var isVendor   = (label === '\u2726 Vendor brief');\n"
    "  var isStoneAlt = (label === 'Stone alternatives');\n"
    "  var maxTok     = isVendor ? 1000 : 800;\n"
    "\n"
    "  var instructions = isVendor\n"
    "    ? 'You are a senior jewellery trade buyer. Using the piece analysis provided, write one concise paragraph (4-6 sentences) suitable for forwarding to a manufacturer or supplier. Include: exact piece type, construction method, materials with quality markers, craftsmanship tradition if identifiable, and commercial tier. Include any specific requirements the user mentions. Use professional B2B trade language only. No consumer-facing styling language.'\n"
    "    : isStoneAlt\n"
    "      ? 'You are a jewellery designer and gemologist. Based on the piece analysis, suggest 3-4 stones that would work as genuine design alternatives in this piece \u2014 not cheaper substitutes, but stones that complement the setting style, metal colour, and craftsmanship tradition. Consider colour harmony, hardness suitability for the construction method, and visual character. Each suggestion should feel like a deliberate design choice. Name each stone, describe why it works aesthetically, and note any practical consideration for the setter.'\n"
    "      : 'You are a jewellery expert. Answer only the specific question asked, using the piece analysis provided. Be concise (3-5 sentences), direct, and factual. Do not repeat the full analysis.';"
)

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print('\u2714  Stone alternatives prompt updated \u2014 design-compatibility language applied')
else:
    print('\u26a0   Anchor not found. The instructions block may look slightly different in your file.')
    print('    Manually find the "var instructions = isVendor" block in runFollowUp()')
    print('    and add an isStoneAlt branch between isVendor and the generic fallback.')

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(src)

print()
print('Next:')
print('  git add -A && git commit -m "fix: stone alternatives \u2192 design-compatible suggestion prompt" && git push')
