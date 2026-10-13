# -*- coding: utf-8 -*-
"""Bring the post-a-role field back under the hero copy.

Markup and CSS are lifted from the backup taken before the page was cleared,
so this is the same field as before -- the portal's own, down to the drifting
haze around its edge. Two changes: it inherits the page's Geist instead of
naming Satoshi, and it sits under the subcopy rather than under a lead.
"""
import io
import re

full = io.open('build_recruitment_page.full.py', encoding='utf-8').read()

m = re.search(r'              <form class="rec-compose".*?</form>\n', full, re.S)
assert m, 'composer markup not found in the backup'
markup = m.group(0)

i = full.index('    /* ---- hero composer')
j = full.index('    /* ---- posted role to signed offer')
css = full[i:j].rstrip() + '\n'

# the page is set in Geist now; the field should not name a face of its own
css = css.replace("font-family:'Satoshi',sans-serif; ", '')
css = css.replace(" font-family:'Satoshi',sans-serif;", '')
assert 'Satoshi' not in css, 'a Satoshi reference is left in the field css'

# it follows the subcopy now, so it carries its own gap
css = css.replace('max-width:900px; margin:48px auto 0;',
                  'max-width:820px; margin:48px auto 0;', 1)

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

anchor = '          it arrives. You pay only when someone joins.</p>\n'
assert anchor in s, 'subcopy markup changed'
s = s.replace(anchor, anchor + markup, 1)

anchor = '    /* ---- landing layout ---------------------------------------------- */\n'
assert anchor in s, 'landing layout marker moved'
s = s.replace(anchor, css + '\n' + anchor, 1)

# the footer row stacks on a narrow screen
old = '      .rec-cursor b { left:28px; top:5px; font-size:11px; padding:2px 8px 3px; }'
new = (old + '\n'
       '      .rec-compose { margin-top:36px; }\n'
       '      .rec-compose-foot { flex-direction:column; align-items:stretch; gap:10px; }\n'
       '      .rec-compose-post { width:100%; }')
assert old in s, 'responsive cursor rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('composer restored')
