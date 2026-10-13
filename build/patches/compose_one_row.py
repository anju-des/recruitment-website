# -*- coding: utf-8 -*-
"""Put the action on the same line as the prompt.

The button moves up into the input row, which removes the footer entirely and
takes roughly 60px out of the field's height.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

m = re.search(r'\n *<div class="rec-compose-foot">\s*'
              r'(<button type="submit" class="rec-compose-post">[^<]*</button>)\s*</div>\n',
              s, re.S)
assert m, 'footer block not found'
button = m.group(1)
s = s[:m.start()] + '\n' + s[m.end():]

old = '                            placeholder="What role are you hiring for?"></textarea>\n'
assert old in s, 'textarea markup changed'
s = s.replace(old, old + '                  ' + button + '\n', 1)

# the row now holds both, so it no longer needs a gap under it
old = '    .rec-compose-headrow { display:flex; align-items:center; gap:12px; margin-bottom:30px; }'
new = '    .rec-compose-headrow { display:flex; align-items:center; gap:16px; }'
assert old in s, 'headrow rule changed'
s = s.replace(old, new, 1)

old = '    .rec-compose-foot { display:flex; align-items:center; justify-content:flex-end; }\n'
assert old in s, 'footer rule changed'
s = s.replace(old, '', 1)

# a shorter box, now that nothing sits below the prompt
old = '                   padding:14px 18px 12px; box-shadow:0 8px 28px rgba(37,99,235,0.12); }'
new = '                   padding:12px 12px 14px 18px; box-shadow:0 8px 28px rgba(37,99,235,0.12); }'
assert old in s, 'compose padding changed'
s = s.replace(old, new, 1)

old = '      .rec-compose-post { width:100%; }\n'
assert old in s, 'responsive button rule changed'
s = s.replace(old, '', 1)

assert 'rec-compose-foot' not in s, 'a footer reference is left'
io.open(p, 'w', encoding='utf-8').write(s)
print('action moved onto the prompt row')
