# -*- coding: utf-8 -*-
"""The bar comes off, and the header gets an edge instead.

With the step ticks gone, the bar was the last thing still narrating
progress in the chrome -- and the panel does that better: three
headings, each with the card it produced underneath. A purple rule
across the top of every screen was weather, not information.

What the top of the screen does need is a line between the header and
the work, which the bar was incidentally providing. Now it is an actual
border, the same hairline as the panel's edge, so the two meet in the
corner as one frame.

at_step keeps deciding which steps are done -- the chips and the
headings read that -- it simply has no segments to colour in.
"""
import io
import sys

EDITS = [
    # the element
    ("""        '<div class="rec-flow-bar" aria-hidden="true">' +
          '<i></i><i></i><i></i></div>' +""", ""),

    # the segments at_step used to colour
    ("""      // the bar is the same answer, drawn along the top
      var segs = flow.querySelectorAll('.rec-flow-bar i');
      for (var n = 0; n < segs.length; n++) {
        segs[n].classList.toggle('is-done', n < i || (n === i && done));
        segs[n].classList.toggle('is-now', n === i && !done);
      }
""", ""),

    # and the line it was standing in for
    ("""    .rec-flow-head { flex:none; display:flex; align-items:center;
                     justify-content:space-between; gap:16px;
                     padding:10px clamp(18px, 3vw, 40px); }""",
     """    .rec-flow-head { flex:none; display:flex; align-items:center;
                     justify-content:space-between; gap:16px;
                     padding:10px clamp(18px, 3vw, 40px);
                     border-bottom:1px solid #E7E2F6; }"""),
]

DEAD_CSS_HEAD = "    /* the rail fills as the brief does */"
DEAD_CSS_TAIL = "    .rec-flow-card { text-align:center; }"

DEAD_MOTION = """      .rec-flow-bar i { transition:none; }
      .rec-flow-bar i.is-now::after { animation:none; opacity:.55; }
"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()

    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    assert s.count(DEAD_MOTION) == 1, (path, 'motion', s.count(DEAD_MOTION))
    s = s.replace(DEAD_MOTION, '', 1)

    at = s.index(DEAD_CSS_HEAD)
    end = s.index(DEAD_CSS_TAIL, at)
    s = s[:at] + s[end:]

    for gone in ['rec-flow-bar', 'rec-bar-sweep']:
        assert gone not in s, (path, gone + ' survives')

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
