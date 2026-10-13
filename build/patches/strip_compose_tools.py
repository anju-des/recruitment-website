# -*- coding: utf-8 -*-
"""Drop the JD / Link / Skills row and the rule above it.

With nothing on the left, the footer no longer divides anything, so the
border goes with the buttons and the action sits on its own.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

m = re.search(r'\n *<div class="rec-compose-tools">.*?</div>\n', s, re.S)
assert m, 'tools row not found'
s = s[:m.start()] + '\n' + s[m.end():]
assert 'rec-compose-tools' not in s.split('EXTRA_CSS')[0], 'tools markup left behind'

old = """    .rec-compose-foot { display:flex; align-items:center; justify-content:space-between;
                        gap:16px; border-top:1px solid #eef0f4; padding-top:12px; }"""
new = """    .rec-compose-foot { display:flex; align-items:center; justify-content:flex-end; }"""
assert old in s, 'footer rule changed'
s = s.replace(old, new, 1)

for rule in [
    """    .rec-compose-tools { display:flex; align-items:center; gap:6px; }
""",
    """    .rec-compose-tools button { display:inline-flex; align-items:center; gap:7px;
                                background:transparent; border:none; cursor:pointer;
                                color:#475569; font-size:14px;
                                font-weight:500; padding:7px 11px; border-radius:9px;
                                transition:background .12s, color .12s; }
""",
    """    .rec-compose-tools button:hover { background:#f1f5f9; color:#1e293b; }
""",
    """    .rec-compose-tools svg { width:16px; height:16px; }
""",
]:
    assert rule in s, 'tools css not found as expected: ' + rule[:40]
    s = s.replace(rule, '', 1)

old = """      .rec-compose-foot { flex-direction:column; align-items:stretch; gap:10px; }
"""
assert old in s, 'responsive footer rule changed'
s = s.replace(old, '', 1)

assert 'rec-compose-tools' not in s, 'a tools reference is left'
io.open(p, 'w', encoding='utf-8').write(s)
print('tools row and rule removed')
