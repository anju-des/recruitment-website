# -*- coding: utf-8 -*-
"""The banner card: lifted, unbordered, and sanded in blue and purple.

The sand has to be a layer behind the content rather than the card's own
background. A mask applies to everything the element paints, children
included, so masking the card itself would eat the words along with the fill.
"""
import io
import sys

NOISE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
         "width='180' height='180'%3E%3Cfilter id='c'%3E%3CfeTurbulence "
         "type='fractalNoise' baseFrequency='0.62' numOctaves='3' "
         "stitchTiles='stitch'/%3E%3CfeColorMatrix type='matrix' "
         "values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 "
         "0.33 0.33 0.33 0 -0.26'/%3E%3C/filter%3E%3Crect "
         "width='180' height='180' filter='url(%23c)'/%3E%3C/svg%3E\")")

OLD = """                    margin-bottom:clamp(30px, 4.5vh, 64px);
                    border-radius:clamp(18px, 1.6vw, 26px);
                    padding:clamp(28px, 3.2vw, 50px) clamp(26px, 3.2vw, 54px);
                    background:linear-gradient(135deg,
                      rgba(150,110,245,.26) 0%, rgba(58,86,226,.15) 100%);
                    box-shadow:inset 0 0 0 1px rgba(201,184,255,.18);
                    opacity:var(--fin, 0);
                    transform:translateY(calc((1 - var(--fin, 0)) * 18px)); }"""

NEW = """                    margin-top:clamp(-56px, -4.5vh, -24px);
                    margin-bottom:clamp(30px, 4.5vh, 64px);
                    border-radius:clamp(18px, 1.6vw, 26px);
                    padding:clamp(28px, 3.2vw, 50px) clamp(26px, 3.2vw, 54px);
                    background:linear-gradient(118deg,
                      rgba(60,84,214,.20) 0%, rgba(132,96,242,.16) 100%);
                    opacity:var(--fin, 0);
                    transform:translateY(calc((1 - var(--fin, 0)) * 18px)); }
    /* The card's own sand, built like the rest of the page's: the blue-into-
       purple wash is what is painted and the noise masks it, so the speckles
       carry the colour. It has to be a layer behind the content -- a mask
       applies to everything an element paints, children included, so masking
       the card itself would eat the words along with the fill. */
    .rec-foot-cta::before { content:""; position:absolute; inset:0; z-index:0;
                            border-radius:inherit; pointer-events:none;
                            opacity:.62;
                            background:linear-gradient(118deg,
                              rgba(74,104,240,.92) 0%,
                              rgba(118,88,238,.86) 52%,
                              rgba(176,124,252,.80) 100%);
                            -webkit-mask-image:@NOISE@;
                            mask-image:@NOISE@;
                            -webkit-mask-size:150px 150px;
                            mask-size:150px 150px; }
    .rec-foot-cta-say, .rec-foot-cta-act { position:relative; z-index:1; }""".replace('@NOISE@', NOISE)


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, s.count(OLD))
    io.open(path, 'w', encoding='utf-8').write(s.replace(OLD, NEW, 1))
    print('sanded', path)


for p in sys.argv[1:]:
    patch(p)
