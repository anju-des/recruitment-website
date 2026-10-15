# -*- coding: utf-8 -*-
"""A wider question column, so the heading holds one line.

"Let's start with your company" is 29 characters, and at the top of the
heading's clamp that wants more room than 520 gives it. The column and
the card it sits in both go to 680; the field and the action row follow
the column, which is what keeps Continue and the skip at its two ends.

The found screens keep their 520. Their headings are shorter and their
tiles read better in a narrower measure.
"""
import io
import sys

EDITS = [
    ("""    .rec-ask-col { width:min(520px, 100%); margin-inline:auto;""",
     """    .rec-ask-col { width:min(680px, 100%); margin-inline:auto;"""),

    ("""    .rec-flow-card { width:min(620px, 100%); }""",
     """    .rec-flow-card { width:min(680px, 100%); }"""),
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
