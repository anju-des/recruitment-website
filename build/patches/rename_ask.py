# -*- coding: utf-8 -*-
"""`ask` is the flow's own function; the paste button cannot have the name.

var is function-scoped, so a `var ask` anywhere in that IIFE shadows
ask(step) -- the thing that builds every question screen -- for the
whole of it. draw() then called a button.
"""
import io
import re

p = 'jd_starts_flow.py'
s = io.open(p, encoding='utf-8').read()

head = s.index('WIRE_JS = r"""') + len('WIRE_JS = r"""')
tail = s.index('"""\n\nWIRE_ANCHOR')
block = s[head:tail]

assert 'var ask = document.createElement' in block, 'nothing to rename'
block = re.sub(r'\bask\b', 'offer', block)
block = block.replace(
    "      var offer = document.createElement('button');",
    "      // not `ask`: that name builds a question screen one scope out\n"
    "      var offer = document.createElement('button');")

s = s[:head] + block + s[tail:]
# the only `ask` left in the block is the comment saying why
code = re.sub(r'//.*', '', block)
assert re.search(r'\bask\b', code) is None, 'an ask survives in code'
io.open(p, 'w', encoding='utf-8').write(s)
print('renamed', block.count('offer'), 'uses')
