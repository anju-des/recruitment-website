# -*- coding: utf-8 -*-
"""Two real bugs in the field's animation.

1. The haze was landing ON TOP of the card. Animating opacity/transform on
   .rec-compose made it a stacking context, and inside one, z-index:-1
   children paint above the element's own background instead of behind the
   whole thing. The animation moves to a wrapper, so the card itself forms no
   stacking context and the haze sits behind it again.

2. The scroll class did nothing. The entrance ran with `fill: both`, so its
   final opacity/transform kept applying forever -- and animation values beat
   normal rules in the cascade, so `.is-out` was silently overridden. It now
   uses `backwards`, which only fills before the animation starts.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- markup: wrap the form -------------------------------------------------
old = '              <form class="rec-compose" onsubmit="return false">'
new = ('              <div class="rec-compose-wrap">\n'
       '              <form class="rec-compose" onsubmit="return false">')
assert old in s, 'form open changed'
s = s.replace(old, new, 1)

old = '              </form>\n'
new = '              </form>\n              </div>\n'
assert s.count(old) == 1, 'form close changed'
s = s.replace(old, new, 1)

# ---- css: the wrapper carries the motion, the card carries the look --------
old = """    .rec-compose { position:relative; width:100%; max-width:820px; margin:48px auto 0; text-align:left;"""
new = """    .rec-compose-wrap { width:100%; max-width:820px; margin:48px auto 0; }
    .rec-compose { position:relative; width:100%; text-align:left;"""
assert old in s, 'compose rule changed'
s = s.replace(old, new, 1)

old = """    .rec-compose { animation:rec-field-in .62s cubic-bezier(.22,.61,.36,1) .12s both;
                   transition:opacity .34s cubic-bezier(.22,.61,.36,1),
                              transform .34s cubic-bezier(.22,.61,.36,1); }
    .rec-compose.is-out { opacity:0; transform:translateY(-22px) scale(.94);
                          pointer-events:none; }
    @media (prefers-reduced-motion: reduce) {
      .rec-compose { animation:none; transition:none; }
      .rec-compose.is-out { opacity:1; transform:none; pointer-events:auto; }
    }"""
new = """    /* `backwards`, not `both`: a forwards-filling animation keeps applying its
       end values, and animation values outrank normal rules -- which would
       leave .is-out unable to move anything. */
    .rec-compose-wrap { animation:rec-field-in .62s cubic-bezier(.22,.61,.36,1) .12s backwards;
                        transition:opacity .34s cubic-bezier(.22,.61,.36,1),
                                   transform .34s cubic-bezier(.22,.61,.36,1); }
    .rec-compose-wrap.is-out { opacity:0; transform:translateY(-22px) scale(.94);
                               pointer-events:none; }
    @media (prefers-reduced-motion: reduce) {
      .rec-compose-wrap { animation:none; transition:none; }
      .rec-compose-wrap.is-out { opacity:1; transform:none; pointer-events:auto; }
    }"""
assert old in s, 'field animation block changed'
s = s.replace(old, new, 1)

old = '      .rec-compose { margin-top:36px; }'
new = '      .rec-compose-wrap { margin-top:36px; }'
assert old in s, 'responsive compose rule changed'
s = s.replace(old, new, 1)

# ---- script: the wrapper is what moves -------------------------------------
old = "    var field = document.querySelector('.rec-compose');"
new = "    var field = document.querySelector('.rec-compose-wrap');"
assert old in s, 'scroll script changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('stacking context and fill-mode fixed')
