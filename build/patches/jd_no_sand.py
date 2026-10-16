# -*- coding: utf-8 -*-
"""The wash under the header comes off.

It was there to give one short screen some weather. The screen is long
now and carries a panel, a card and four lists, and a purple-into-blue
gradient behind all of that is one more thing to read past. White lets
the panel's edge do the dividing.

The element goes with the style -- a zero-height div painting nothing
is just a thing to wonder about later -- and the z-index that lifted
the card above it goes too, since there is nothing left to be above.
"""
import io
import sys

HEAD = """    /* Sand under the header, purple into blue."""
TAIL = """    /* the questions sit over it */
    .rec-flow-card { position:relative; z-index:1; text-align:center; }"""

NEW_TAIL = """    .rec-flow-card { text-align:center; }"""

MARKUP = """        '<div class="rec-flow-sand" aria-hidden="true"></div>' +\n"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()

    at = s.index(HEAD)
    end = s.index(TAIL, at)
    s = s[:at] + NEW_TAIL + s[end + len(TAIL):]

    assert s.count(MARKUP) == 1, (path, 'the element', s.count(MARKUP))
    s = s.replace(MARKUP, '', 1)

    # the rail's own note about painting over it no longer applies
    old = """                 /* the sand is positioned and this was not, so without a
                    layer of its own the gradient paints over the text */
                 position:relative; z-index:1;
"""
    new = """                 position:relative;
"""
    assert s.count(old) == 1, (path, 'rail layer', s.count(old))
    s = s.replace(old, new, 1)

    assert 'rec-flow-sand' not in s, path + ': the sand survives'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
