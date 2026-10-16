# -*- coding: utf-8 -*-
"""The column sits beside the panel instead of floating in the middle.

Centred in the space left over, it drifted further from the panel the
wider the window got -- on a large display the rail was on one side,
the work was somewhere out in the middle, and the two stopped reading
as one screen. Against the panel they are a document with a contents
list beside it.

The column keeps its own width, so the lines of text do not get any
longer; only the space to its right does.
"""
import io
import sys

OLD = """    /* auto across, nothing down: centred in the column, top of the
       window, and still scrollable when it is taller than one */
    .rec-flow-card { width:min(680px, 100%); margin:0 auto; }"""

NEW = """    /* no margin either way: beside the panel, at the top of the window,
       and still scrollable when it is taller than one */
    .rec-flow-card { width:min(680px, 100%); margin:0; }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, 'card', s.count(OLD))
    s = s.replace(OLD, NEW, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
