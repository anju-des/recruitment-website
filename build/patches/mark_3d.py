# -*- coding: utf-8 -*-
"""The mark gets a body and turns into place.

Chained drop-shadows each apply to the result of the one before, so a short
stack of them on the silhouette builds a solid extrusion -- a body behind
the face, in violet, without duplicating the image nine times. The scroll
turns it from a three-quarter view to square-on as it resolves, which is
what makes the depth read.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# a short stack: each step is offset from the last, darkening as it recedes
body = []
shades = ['(124,92,246,.98)', '(114,84,232,.97)', '(104,76,216,.96)',
          '(94,68,198,.95)', '(84,60,180,.94)', '(74,52,162,.93)',
          '(64,44,142,.92)', '(52,36,120,.90)']
for shade in shades:
    body.append('drop-shadow(1px 1.4px 0 rgba%s)' % shade)
extrusion = ('\n                           '.join(body))

old = """                    height:auto;
                    filter:invert(1) brightness(1.9)
                           drop-shadow(0 0 30px rgba(167,139,250,.55));
                    opacity:var(--mark, 0);
                    transform:scale(calc(0.94 + 0.06 * var(--mark, 0))); }"""
new = """                    height:auto; transform-origin:50%% 55%%;
                    filter:invert(1) brightness(1.95)
                           %s
                           drop-shadow(0 16px 26px rgba(16,6,44,.72))
                           drop-shadow(0 0 34px rgba(167,139,250,.50));
                    opacity:var(--mark, 0);
                    /* it turns square-on as it resolves, which is what sells
                       the body behind the face */
                    transform:perspective(900px)
                              rotateY(calc((1 - var(--mark, 0)) * -34deg))
                              rotateX(calc((1 - var(--mark, 0)) * 12deg))
                              scale(calc(0.9 + 0.1 * var(--mark, 0))); }""" % extrusion
assert old in s, 'mark rule changed'
s = s.replace(old, new, 1)

old = """      .rec-orb-core, .rec-orb-glow, .rec-orb-ring, .rec-orb-mark {
        transform:none; }
      .rec-orb-mark { opacity:1; }"""
new = """      .rec-orb-core, .rec-orb-glow, .rec-orb-ring { transform:none; }
      .rec-orb-mark { opacity:1; transform:perspective(900px); }"""
assert old in s, 'reduced motion rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('the mark has a body')
