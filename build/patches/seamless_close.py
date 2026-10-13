# -*- coding: utf-8 -*-
"""No seam between the black and the light.

The panel had a hard top edge, so the two sections met on a line. It now
starts at the same black as the section above it and travels up to white
across the first half of its own height -- the light arrives as a gradient
rather than as a new block laid on top.

The inset-and-open animation goes with it: an opaque panel inset from the
edges would have shown those same hard lines down both sides.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """    /* ---- closing ---------------------------------------------------------- */
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
    }"""
new = """    /* ---- closing ---------------------------------------------------------- */
    /* It starts at the same black as the section above and climbs to white
       over its own first half, so there is no line where one ends and the
       other begins -- the light simply arrives. */
    .rec-wrap > section.rec-close { padding:0; }
    .rec-close { position:relative; min-height:140vh; }
    .rec-close-panel { height:140vh;
                       background:linear-gradient(180deg,
                         #000000 0%, #06060B 10%, #231D44 30%,
                         #EFEAFF 62%, #FFFFFF 100%); }"""
assert old in s, 'closing styles changed'
s = s.replace(old, new, 1)

old = """      .rec-close-panel { margin-inline:20px; }"""
new = """      .rec-close, .rec-close-panel { min-height:110vh; height:110vh; }"""
assert old in s, 'responsive closing rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('the light arrives without a seam')
