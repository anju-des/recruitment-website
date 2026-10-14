# -*- coding: utf-8 -*-
"""The banner goes pastel: lavender into pale blue into peach.

The same wash the mock screens sit on further up the page. Going this light
means the card stops being a dark surface, so everything on it has to turn
over with it -- white words on pale lavender are not words. The heading and
copy go dark, the solid button inverts to dark-on-light, and the outlined one
takes an ink border instead of a white one.

The sand stays, in slightly deeper versions of the same three, so the grain
reads as texture in the pastel rather than disappearing into it.
"""
import io
import sys

EDITS = [
    # the fill
    ("""                    background:linear-gradient(118deg,
                      rgba(150,190,255,.26) 0%, rgba(178,144,255,.30) 40%,
                      rgba(240,182,222,.24) 100%);""",
     """                    background:linear-gradient(118deg,
                      rgba(226,216,250,.97) 0%, rgba(238,241,253,.96) 46%,
                      rgba(251,231,220,.95) 100%);"""),

    # the grain over it, a shade deeper so it still shows
    ("""                            opacity:.70;
                            /* purple most of the way, with light blue
                               entering at one corner and pink leaving at the
                               other */
                            background:linear-gradient(118deg,
                              rgba(160,198,255,.92) 0%,
                              rgba(184,152,255,.94) 28%,
                              rgba(206,170,252,.90) 62%,
                              rgba(244,186,226,.86) 100%);""",
     """                            opacity:.50;
                            /* a shade deeper than the fill, so the speckles
                               still show against a surface this pale */
                            background:linear-gradient(118deg,
                              rgba(198,180,246,.92) 0%,
                              rgba(206,218,250,.88) 46%,
                              rgba(247,212,194,.88) 100%);"""),

    # white type cannot live on this
    ("""    .rec-foot-cta h2 { margin:0 0 10px; color:#FFFFFF;""",
     """    .rec-foot-cta h2 { margin:0 0 10px; color:#1A1430;"""),
    ("""    .rec-foot-cta p { margin:0; color:#E2DDF4; font-size:14.5px;""",
     """    .rec-foot-cta p { margin:0; color:#4B4270; font-size:14.5px;"""),

    # the solid button inverts; the outlined one takes an ink edge
    ("""    .rec-foot-cta .rec-foot-cta-go { background:#FFFFFF; color:#1A1430; }
    .rec-foot-cta .rec-foot-cta-go:hover { background:#EDE9FC; }
    .rec-foot-cta .rec-foot-cta-alt { color:#E4DFF6;
      box-shadow:inset 0 0 0 1px rgba(201,184,255,.3); }""",
     """    .rec-foot-cta .rec-foot-cta-go { background:#1A1430; color:#FFFFFF; }
    .rec-foot-cta .rec-foot-cta-go:hover { background:#2E2650; color:#FFFFFF; }
    .rec-foot-cta .rec-foot-cta-alt { color:#2C2545;
      box-shadow:inset 0 0 0 1px rgba(26,20,48,.24); }"""),
    ("""    .rec-foot-cta .rec-foot-cta-alt:hover { background:rgba(255,255,255,.09);
      color:#FFFFFF; }""",
     """    .rec-foot-cta .rec-foot-cta-alt:hover { background:rgba(26,20,48,.07);
      color:#1A1430; }"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:44], s.count(old))
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
