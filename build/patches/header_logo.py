# -*- coding: utf-8 -*-
"""A header carrying the Mira logo.

The logo file is an SVG wrapper around a bitmap, so it goes in as its own
file with explicit dimensions rather than inline -- 90KB of base64 in the
page would delay everything behind it.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = '      <div class="rec-wrap">\n'
new = """      <header class="rec-head">
        <a class="rec-logo" href="explore-services.html">
          <img src="mira-logo.svg" width="1152" height="365" alt="Mira">
        </a>
      </header>

      <div class="rec-wrap">
"""
assert s.count(old) == 1, 'wrap opening moved'
s = s.replace(old, new, 1)

old = '    /* ---- announcement chip ------------------------------------------- */\n'
new = """    /* ---- header ---------------------------------------------------------- */
    .rec-head { display:flex; align-items:center; height:72px; padding:0 48px; }
    .rec-logo { display:inline-flex; }
    .rec-logo img { height:30px; width:auto; display:block; }

""" + old
assert old in s, 'chip css marker moved'
s = s.replace(old, new, 1)

# the hero measures the screen minus whatever sits above it
old = '    "--rec-chrome:8px;", 1)'
new = '    "--rec-chrome:80px;", 1)'
assert old in s, 'chrome token changed'
s = s.replace(old, new, 1)

old = '      .rec-wrap > section { padding:32px 24px; }'
new = (old + '\n'
       '      .rec-head { height:64px; padding:0 24px; }\n'
       '      .rec-logo img { height:26px; }')
assert old in s, 'responsive section rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('header added')
