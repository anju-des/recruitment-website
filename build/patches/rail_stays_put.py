# -*- coding: utf-8 -*-
"""The rail stops vanishing, and the card gets room to breathe.

The rail was shown by either is-working or is-found. In a live session
both are set once the lookup has run, so opening the details -- which
drops is-found -- left is-working holding it up. A restored session
never ran the lookup, so it only had is-found, and opening the chip took
the step and the chip off the screen with it.

is-working is really "the lookup has happened", so the restore sets it
too. The rail then depends on one fact that never stops being true
rather than on two that happen to overlap.

And the blocks inside the details sat too close for four different kinds
of thing: the paragraph, the tiles and the links all take more space
above them.
"""
import io
import sys

EDITS = [
    ("""      at_step(0, true);
      flow.classList.add('is-found');""",
     """      at_step(0, true);
      // the lookup has happened, even though this session did not run it:
      // without this the rail leaves with the details
      flow.classList.add('is-working');
      flow.classList.add('is-found');"""),

    ("""    .rec-found-card .rec-found-about { margin-top:14px; }
    .rec-found-card .rec-found-facts { margin-top:16px; }""",
     """    .rec-found-card .rec-found-about { margin-top:18px; }
    .rec-found-card .rec-found-facts { margin-top:22px; }
    .rec-found-card .rec-found-links { margin-top:20px; }"""),

    ("""    .rec-found-about { max-width:34ch; margin:16px auto 0; font-size:14px;""",
     """    .rec-found-about { max-width:34ch; margin:18px auto 0; font-size:14px;"""),

    ("""    .rec-found-facts { display:flex; flex-wrap:wrap; justify-content:center;
                       gap:10px; margin-top:18px; }""",
     """    .rec-found-facts { display:flex; flex-wrap:wrap; justify-content:center;
                       gap:10px; margin-top:22px; }"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    js = s[s.rindex('<script>'):]
    assert js.count("classList.add('is-working')") == 2, \
        path + ': the restore or the lookup is missing it'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
