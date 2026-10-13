# -*- coding: utf-8 -*-
"""Take the two result windows out altogether.

Markup, styles and the observer that revealed them all go; the page now ends
with Mira's own window.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- markup ----------------------------------------------------------------
m = re.search(r'\n *<!-- WHAT CAME OF IT -->\n *<section class="rec-more-sec">.*?'
              r'\n *</section>\n', s, re.S)
assert m, 'the results section was not found'
s = s[:m.start()] + '\n' + s[m.end():]

# ---- css -------------------------------------------------------------------
old = """    /* the results, in a section of their own further down */
    .rec-more-sec { min-height:100vh; display:grid; place-items:center; }
    .rec-more { display:flex; align-items:stretch; gap:24px; }
"""
assert old in s, 'results section rules changed'
s = s.replace(old, '', 1)

old = """    /* they arrive one after the other once their own section is in view */
    .rec-win--2, .rec-win--3 { opacity:0; transform:translateY(28px);
                               transition:opacity .7s ease, transform .7s ease; }
    .rec-more-sec.is-on .rec-win--2,
    .rec-more-sec.is-on .rec-win--3 { opacity:1; transform:none; }
    .rec-more-sec.is-on .rec-win--3 { transition-delay:.35s; }
"""
assert old in s, 'results reveal rules changed'
s = s.replace(old, '', 1)

# the side styles sit after .rec-ask-right, not before it
start = s.index('    /* the side windows match the tall one, with their action at the foot */')
TAIL = '.rec-side-btn:hover { background:#E4E7EE; }'
end = s.index(TAIL) + len(TAIL) + 1
block = s[start:end]
assert '.rec-side-btn' in block, 'side window styles changed'
s = s[:start] + s[end:]

old = """      .rec-chat-sec, .rec-more-sec { min-height:0; margin-top:0; padding-block:60px; }"""
new = """      .rec-chat-sec { min-height:0; margin-top:0; padding-block:60px; }"""
assert old in s, 'responsive section rule changed'
s = s.replace(old, new, 1)

old = """      .rec-more { flex-direction:column; align-items:stretch; }
"""
assert old in s, 'responsive results rule changed'
s = s.replace(old, '', 1)

# ---- script ----------------------------------------------------------------
m = re.search(r'\n  // The two result windows arrive one after the other.*?\n  \}\(\)\);\n', s, re.S)
assert m, 'the results observer was not found'
s = s[:m.start()] + '\n' + s[m.end():]

for dead in ('rec-more', 'rec-win--2', 'rec-win--3', 'rec-side'):
    assert dead not in s, 'a reference to ' + dead + ' is left'

io.open(p, 'w', encoding='utf-8').write(s)
print('result windows removed')
