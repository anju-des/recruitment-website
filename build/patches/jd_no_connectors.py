# -*- coding: utf-8 -*-
"""The threads between the steps come out.

They joined one circle to the next when a step was a circle and a word.
A step is a heading over a card over a list now, and a 28px thread
reaching across that gap joins nothing -- it reads as a stray mark
beside the content it is supposed to connect. The headings and the
panel's own edge do that work.

The horizontal rule for the narrow layout goes with it: it was the same
thread lying down.
"""
import io
import sys

EDITS = [
    ("""    /* a line from the circle above to this one, at the circle's centre */
    .rec-step + .rec-step::before { content:""; position:absolute;
                                    left:9.5px; top:-14px; width:1px;
                                    height:28px; background:#E2DCF4; }
""", ""),

    ("""      .rec-step + .rec-step { flex:1; }
      .rec-step + .rec-step::before { position:static; flex:1; width:auto;
                                      min-width:14px; height:1px;
                                      margin-right:8px; }
""", """      .rec-step + .rec-step { flex:1; }
"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert '.rec-step + .rec-step::before' not in s, \
        path + ': a thread survives'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
