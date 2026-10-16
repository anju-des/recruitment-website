# -*- coding: utf-8 -*-
"""The ticks come off the step headings.

A numbered circle that becomes a tick was the only thing saying how far
along the flow was, back when the rail was three words. Three things
say it now -- the bar across the top, the card under each heading, and
the lists under that -- so the circles were repeating what the panel
already showed, and a column of purple ticks down the left was the
loudest thing in it.

The spinner went with them. A step being worked on is already the one
segment sweeping in the bar, which is a better place for it: the panel
is a record of what was made, and the bar is where progress lives.

at_step still decides which steps are done, because the bar and the
chips both read that; it simply has no circle to write into any more.
"""
import io
import sys

EDITS = [
    ("""                return '<li class="rec-step">' +
                  '<span class="rec-step-row"><i>' + (i + 1) + '</i>' +
                  '<b>' + s + '</b></span></li>';""",
     """                return '<li class="rec-step">' +
                  '<span class="rec-step-row"><b>' + s + '</b></span></li>';"""),

    # the mark it used to write into is gone; the rest of at_step is not
    ("""        var mark = all[k].querySelector('i');
        mark.textContent = over ? '\\u2713' : String(k + 1);""",
     """        // no mark to write into: the bar carries the progress now"""),

    ("""    .rec-step-row i { font-style:normal; display:grid; place-items:center;
                  width:20px; height:20px; flex:none; border-radius:50%;
                  background:#F1EEFA; color:#9A93B8; font-size:11px;
                  font-weight:700; }
    .rec-step-row b { font-weight:500; }
    .rec-step.is-on { color:#1A1430; }
    .rec-step.is-on .rec-step-row i { background:#7C5CF6; color:#FFFFFF; }
    .rec-step.is-on .rec-step-row b { font-weight:600; }
    .rec-step.is-busy .rec-step-row i { background:#7C5CF6; color:transparent;
                          position:relative; }
    .rec-step.is-busy .rec-step-row i::after { content:""; position:absolute; inset:3px;
                                 border-radius:50%;
                                 border:2px solid rgba(255,255,255,.4);
                                 border-top-color:#FFFFFF;
                                 animation:rec-flow-turn .7s linear infinite; }
    @media (prefers-reduced-motion: reduce) {
      .rec-step.is-busy .rec-step-row i::after { animation:none; }
    }
    .rec-step.is-done { color:#6B6392; }
    .rec-step.is-done .rec-step-row i { background:#EDE8FD; color:#5A4BD8; }""",

     """    .rec-step-row b { font-weight:500; }
    .rec-step.is-on { color:#1A1430; }
    .rec-step.is-on .rec-step-row b { font-weight:600; }
    .rec-step.is-done { color:#6B6392; }"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert '.rec-step-row i' not in s, path + ': a circle survives'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
