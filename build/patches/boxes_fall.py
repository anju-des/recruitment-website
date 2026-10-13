# -*- coding: utf-8 -*-
"""Past the statement, the boxes fall in towards Mira.

They are already driven by scroll, so the exit rides the same value the text
leaves on: each box drops, draws in towards the centre line, shrinks and
fades, so they read as going into the window below rather than simply
switching off.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# every box carries how far it sits from the centre, as a fraction of the field
rows = re.findall(r'<div class="rec-box rec-box--d(\d)" style="left:(\d+)%; top:(\d+)%">', s)
assert len(rows) == 8, 'expected eight boxes, found %d' % len(rows)
for d, x, y in rows:
    old = '<div class="rec-box rec-box--d%s" style="left:%s%%; top:%s%%">' % (d, x, y)
    new = ('<div class="rec-box rec-box--d%s" style="left:%s%%; top:%s%%; --fx:%.3f">'
           % (d, x, y, (50 - int(x)) / 100.0))
    assert old in s
    s = s.replace(old, new, 1)

old = """    .rec-boxes { position:absolute; left:50%; top:50%; translate:-50% -50%;
                 width:min(1200px, 92vw); height:640px; pointer-events:none;"""
new = """    .rec-boxes { --field-w:min(1200px, 92vw);
                 position:absolute; left:50%; top:50%; translate:-50% -50%;
                 width:var(--field-w); height:640px; pointer-events:none;"""
assert old in s, 'box field rule changed'
s = s.replace(old, new, 1)

old = """               animation:rec-box-float 9s ease-in-out infinite; }"""
new = """               animation:rec-box-float 9s ease-in-out infinite;
               /* --say-out runs 0 to 1 once the statement starts leaving: the
                  boxes ride it down and inward, towards the window below */
               opacity:calc(var(--d-op, 1) * (1 - var(--say-out, 0)));
               transform:translate(calc(var(--fx, 0) * var(--field-w) * var(--say-out, 0)),
                                   calc(var(--say-out, 0) * 460px))
                         scale(calc(var(--d-scale, 1) * (1 - 0.68 * var(--say-out, 0)))); }"""
assert old in s, 'box rule changed'
s = s.replace(old, new, 1)

old = """    /* depth: all of them sharp, the far ones only dimmer and a touch smaller */
    .rec-box--d1 { opacity:.82; transform:scale(.94);
                   animation-duration:11s; animation-delay:-3s; }
    .rec-box--d2 { opacity:.62; transform:scale(.88);
                   animation-duration:13s; animation-delay:-6s; }"""
new = """    /* depth: all of them sharp, the far ones only dimmer and a touch smaller.
       These are variables rather than declarations so the fall above can
       multiply them instead of being overwritten by them. */
    .rec-box--d1 { --d-op:.82; --d-scale:.94; animation-duration:11s; animation-delay:-3s; }
    .rec-box--d2 { --d-op:.62; --d-scale:.88; animation-duration:13s; animation-delay:-6s; }"""
assert old in s, 'depth rules changed'
s = s.replace(old, new, 1)

old = """    @media (prefers-reduced-motion: reduce) {
      .rec-boxes { opacity:1; transform:none; }
    }"""
new = """    @media (prefers-reduced-motion: reduce) {
      .rec-boxes { opacity:1; transform:none; }
      .rec-box { transform:scale(var(--d-scale, 1)); opacity:var(--d-op, 1); }
    }"""
assert old in s, 'reduced-motion box rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('boxes fall towards the window')
