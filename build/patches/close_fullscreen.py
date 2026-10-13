# -*- coding: utf-8 -*-
"""The closing section empties out and opens to the full screen.

The copy and the buttons go. What is left is the light ground itself, which
arrives as an inset, rounded panel and then opens: the side margins run out
to the edges and the corners flatten, over the same moment the section comes
into view.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

m = re.search(r'( *<section class="rec-close">\n)(.*?)( *</section>\n)', s, re.S)
assert m, 'closing section not found'
assert 'Start hiring today' in m.group(2), 'closing content changed'
s = s[:m.start(2)] + '          <div class="rec-close-panel"></div>\n' + s[m.end(2):]

start = s.index('    /* ---- closing ----')
end = s.index('    /* ---- suggestions ------')
block = s[start:end]
assert '.rec-close-btn' in block, 'closing styles changed'
s = s[:start] + """    /* ---- closing ---------------------------------------------------------- */
    /* An empty light ground that opens to the full screen: it arrives as an
       inset panel with rounded corners and then runs out to the edges. */
    .rec-wrap > section.rec-close { padding:0; }
    .rec-close { position:relative; margin-top:-40px; min-height:100vh; }
    .rec-close-panel { height:100vh; margin-inline:56px; border-radius:40px 40px 0 0;
                       background:linear-gradient(180deg, #EFEAFF 0%, #FFFFFF 62%);
                       transition:margin .95s cubic-bezier(.22,.61,.36,1),
                                  border-radius .95s cubic-bezier(.22,.61,.36,1); }
    .rec-close.is-on .rec-close-panel { margin-inline:0; border-radius:0; }
    @media (prefers-reduced-motion: reduce) {
      .rec-close-panel { transition:none; }
    }

""" + s[end:]

old = """      .rec-close { padding:84px 24px 96px; }"""
new = """      .rec-close-panel { margin-inline:20px; }"""
assert old in s, 'responsive closing rule changed'
s = s.replace(old, new, 1)

for dead in ('rec-close-in', 'rec-close-btn', 'rec-close-alt', 'rec-close-acts'):
    assert dead not in s, 'a reference to ' + dead + ' is left'

io.open(p, 'w', encoding='utf-8').write(s)
print('closing section is an empty panel that opens')
