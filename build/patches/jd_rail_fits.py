# -*- coding: utf-8 -*-
"""The lists stay inside the panel they belong to.

Each set was width:100% with a 30px left margin, inside a step that
shrinks to its contents -- so the margin pushed it 30px past the rail's
edge, and the ellipsis that should have trimmed a long question never
fired, because nothing was constraining the row.

The step stretches to the rail's width now, and the set fills what is
left beside the margin instead of asking for all of it.
"""
import io
import sys

EDITS = [
    # the step is as wide as the panel, so its children can be measured
    ("""    .rec-step { flex-direction:column; align-items:flex-start; }""",
     """    .rec-step { flex-direction:column; align-items:flex-start;
                align-self:stretch; width:100%; box-sizing:border-box; }"""),

    # and the set takes what is left, not all of it
    ("""    .rec-rail-set { width:100%; margin:8px 0 0 30px; padding-right:8px;
                    box-sizing:border-box;""",
     """    .rec-rail-set { align-self:stretch; margin:8px 0 0 30px;
                    padding-right:8px; min-width:0; box-sizing:border-box;"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
