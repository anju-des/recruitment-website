# -*- coding: utf-8 -*-
"""A plain statement in the middle of the dark section.

Not a heading and a subheading -- one block of text at one size, where the
first line carries the claim and the lines under it say what that means.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """        <!-- NEXT SECTION (placeholder) -->
        <section class="rec-next" aria-hidden="true"></section>
"""
new = """        <!-- WHAT MIRA DOES -->
        <section class="rec-next">
          <p class="rec-say">
            <strong>Mira reads everything.</strong>
            Every application, scored against your brief.<br>
            Ranked. Explained. Waiting before you ask.
          </p>
        </section>
"""
assert old in s, 'placeholder section changed'
s = s.replace(old, new, 1)

old = """    .rec-next { min-height:160vh; }"""
new = """    .rec-next { min-height:160vh; display:grid; place-items:center; }
    /* one size throughout: the first line is the claim, the rest is what it
       means. Light type, because the sky is dark by the time this is read. */
    .rec-say { max-width:24ch; text-align:center; font-size:34px; font-weight:500;
               line-height:1.45; letter-spacing:-0.015em; color:#9AA3B8;
               text-wrap:balance; }
    .rec-say strong { display:block; font-weight:600; color:#FFFFFF; }
    @media (max-width:1000px) {
      .rec-say { font-size:24px; max-width:22ch; }
    }"""
assert old in s, 'next section rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('statement added')
