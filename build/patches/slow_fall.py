# -*- coding: utf-8 -*-
"""Let the tiles fall into the window more slowly.

The fall had the last fifth of the pinned stretch. The honest way to give it
more is to make the stretch longer rather than to start the fall earlier --
earlier would run it over the statement's own exit, and over the third line
still coming up to white.

So the section grows from 300vh to 420vh and every band before the fall is
divided by that same 1.4, which lands each of them on exactly the scroll
position it had before. The fall then takes everything that is left: 0.57 to
1 of a stretch 1.4 times longer, which is three times the scroll it had, over
the same distance. Nothing above it moves; only the fall slows.
"""
import io
import sys

EDITS = [
    ("    .rec-next { position:relative; min-height:300vh; }",
     """    /* 420vh rather than 300: the extra is all for the fall at the end of
       it, and every band before the fall is divided by the same 1.4 so it
       still happens where it used to */
    .rec-next { position:relative; min-height:420vh; }"""),

    ("""        root.style.setProperty('--l1', slice(0.08, 0.26));
        root.style.setProperty('--l2', slice(0.28, 0.46));
        root.style.setProperty('--l3', slice(0.48, 0.66));""",
     """        root.style.setProperty('--l1', slice(0.057, 0.186));
        root.style.setProperty('--l2', slice(0.200, 0.329));
        root.style.setProperty('--l3', slice(0.343, 0.471));"""),

    ("        root.style.setProperty('--say-out', slice(0.62, 0.80));",
     "        root.style.setProperty('--say-out', slice(0.443, 0.571));"),

    ("""          var f = parseFloat(slice(0.80, 1));""",
     """          // all the room the longer section bought: three times the
          // scroll the fall used to have, over the same distance
          var f = parseFloat(slice(0.571, 1));"""),
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
