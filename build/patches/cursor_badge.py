# -*- coding: utf-8 -*-
"""A multiplayer-style cursor parked on the last word.

It is decorative, so it is hidden from assistive tech and takes no part in
layout: the span is zero-sized and everything inside it is absolutely placed,
which keeps the headline centred exactly as it was.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = '              <span class="rec-grad">world.</span></h1>'
new = """              <span class="rec-grad">world</span><span class="rec-cursor" aria-hidden="true"><svg viewBox="0 0 20 22"><path d="M2 1.6 L2 19.4 L6.6 15.1 L9.5 21.4 L12.4 20 L9.5 13.9 L16 13.4 Z"/></svg><b>You</b></span></h1>"""
assert old in s, 'headline markup changed'
s = s.replace(old, new, 1)

old = '    .rec-hero-sub { max-width:54ch;'
new = """    /* the cursor: zero-width so it never shifts the centred headline */
    .rec-cursor { position:relative; display:inline-block; width:0; height:0;
                  vertical-align:baseline; }
    .rec-cursor svg { position:absolute; left:6px; top:-16px; width:21px; height:23px;
                      fill:#2684FF; transform:rotate(78deg); filter:drop-shadow(0 2px 4px rgba(38,132,255,.35)); }
    .rec-cursor b { position:absolute; left:26px; top:4px; padding:3px 10px 4px;
                    border-radius:100px; background:linear-gradient(100deg,#2684FF,#6E6BFF);
                    color:#fff; font-size:13px; font-weight:500; line-height:1.3;
                    letter-spacing:0; white-space:nowrap;
                    box-shadow:0 2px 8px rgba(38,132,255,.3); }

    .rec-hero-sub { max-width:54ch;"""
assert s.count(old) == 1, 'sub rule anchor moved'
s = s.replace(old, new, 1)

old = """      .rec-hero-sub { font-size:16px; margin-top:28px; }"""
new = """      .rec-hero-sub { font-size:16px; margin-top:28px; }
      .rec-cursor svg { left:2px; top:-12px; width:16px; height:18px; }
      .rec-cursor b { left:18px; top:2px; font-size:11px; padding:2px 8px 3px; }"""
assert old in s, 'responsive sub rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('cursor added')
