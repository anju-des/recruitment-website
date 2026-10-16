# -*- coding: utf-8 -*-
"""The rail gets an edge, so it reads as a panel rather than a margin.

Everything in it already belonged together; nothing said so. One line
down its right-hand side is enough -- the same hairline the cards and
the rows use, so it joins them rather than competing.

Where the rail lies down across the top, the line lies down with it:
a right-hand edge on a horizontal strip separates nothing.
"""
import io
import sys

OLD = """                 /* the sand is positioned and this was not, so without a
                    layer of its own the gradient paints over the text */
                 position:relative; z-index:1; }"""

NEW = """                 /* the sand is positioned and this was not, so without a
                    layer of its own the gradient paints over the text */
                 position:relative; z-index:1;
                 border-right:1px solid #E7E2F6; }"""

NARROW_OLD = """      .rec-rail-set { display:none; }"""

NARROW_NEW = """      .rec-rail-set { display:none; }
      /* lying down, the edge lies down with it */
      .rec-steps { border-right:0; border-bottom:1px solid #E7E2F6; }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'border-right:1px solid #E7E2F6' not in s, path + ': already edged'

    assert s.count(OLD) == 1, (path, 'rail', s.count(OLD))
    s = s.replace(OLD, NEW, 1)

    assert s.count(NARROW_OLD) == 1, (path, 'narrow', s.count(NARROW_OLD))
    s = s.replace(NARROW_OLD, NARROW_NEW, 1)

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
