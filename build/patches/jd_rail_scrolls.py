# -*- coding: utf-8 -*-
"""The panel scrolls, now that it has more in it than fits.

It held three words and a card when it was written, so nothing ever
asked what happens when it is taller than the window. Four sections
later it is, and a flex item with no overflow of its own simply gets
clipped: the job description sat below the fold with no way to reach
it.

It scrolls itself now, independently of the screen beside it, which is
what a panel does. min-height:0 is the part that makes that work -- a
flex item refuses to shrink below its content without it, so the
overflow would never have anything to scroll.

Lying down across the top it goes back to overflowing sideways, where
the lists are hidden anyway.
"""
import io
import sys

OLD = """                 position:relative;
                 border-right:1px solid #E7E2F6; }"""

NEW = """                 position:relative;
                 border-right:1px solid #E7E2F6;
                 /* taller than the window: scroll it, not the page */
                 min-height:0; overflow-y:auto; overscroll-behavior:contain;
                 scrollbar-width:thin;
                 scrollbar-color:#DED8F2 transparent; }
    .rec-steps::-webkit-scrollbar { width:9px; }
    .rec-steps::-webkit-scrollbar-thumb { border-radius:9px;
                                          border:3px solid transparent;
                                          background-clip:content-box;
                                          background-color:#DED8F2; }
    .rec-steps::-webkit-scrollbar-track { background:transparent; }"""

NARROW_OLD = """      .rec-steps { border-right:0; border-bottom:1px solid #E7E2F6; }"""

NARROW_NEW = """      .rec-steps { border-right:0; border-bottom:1px solid #E7E2F6;
                   overflow-y:visible; overflow-x:auto; }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'overscroll-behavior:contain' not in s, path + ': already scrolls'

    assert s.count(OLD) == 1, (path, 'rail', s.count(OLD))
    s = s.replace(OLD, NEW, 1)

    assert s.count(NARROW_OLD) == 1, (path, 'narrow', s.count(NARROW_OLD))
    s = s.replace(NARROW_OLD, NARROW_NEW, 1)

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
