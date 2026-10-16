# -*- coding: utf-8 -*-
"""A shorter header, so the screen under it starts sooner.

It was padded like a page header on a page that scrolls. This one is
fixed above a column that already has more in it than fits, and every
row it takes is a row the work does not get. The side padding stays --
it lines the logo up with the rail beneath it -- and only the height
comes down, to a band the button sets rather than the padding.
"""
import io
import sys

OLD = """    .rec-flow-head { flex:none; display:flex; align-items:center;
                     justify-content:space-between; gap:16px;
                     padding:clamp(16px, 2.2vw, 26px) clamp(18px, 3vw, 40px); }
    .rec-flow-head img { display:block; width:92px; height:auto; }"""

NEW = """    .rec-flow-head { flex:none; display:flex; align-items:center;
                     justify-content:space-between; gap:16px;
                     padding:10px clamp(18px, 3vw, 40px); }
    .rec-flow-head img { display:block; width:78px; height:auto; }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, 'header', s.count(OLD))
    s = s.replace(OLD, NEW, 1)

    # the button sets the height now, so it carries its own breathing room
    old = "    .rec-flow-cta { padding:10px 18px; border:0; border-radius:8px;"
    new = "    .rec-flow-cta { padding:9px 16px; border:0; border-radius:8px;"
    assert s.count(old) == 1, (path, 'cta', s.count(old))
    s = s.replace(old, new, 1)

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
