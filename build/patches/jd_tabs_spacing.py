# -*- coding: utf-8 -*-
"""The tabs lose their rule and gain some room.

The underline sat a pixel above the summary's own first rule, so the
two read as one thick line and the tabs looked welded to the table. The
selected tab's own mark is all that is needed to say which one is on;
the rule under the whole row was saying nothing the mark was not.

And the card starts lower, so the tabs are a thing above the summary
rather than its first row.
"""
import io
import sys

EDITS = [
    ("""    .rec-tabs { display:flex; gap:4px; margin:18px 0 0;
                border-bottom:1px solid #EDE9F8; }""",
     """    .rec-tabs { display:flex; gap:4px; margin:18px 0 10px; }"""),

    ("""    .rec-tab.is-on::after { content:""; position:absolute; left:10px;
                            right:10px; bottom:-1px; height:2px;
                            border-radius:2px; background:#7C5CF6; }""",
     """    .rec-tab.is-on::after { content:""; position:absolute; left:10px;
                            right:10px; bottom:2px; height:2px;
                            border-radius:2px; background:#7C5CF6; }"""),

    # and the card below them keeps its distance
    ("""    .rec-found-card { padding:0; border-radius:18px;""",
     """    .rec-tabs + .rec-found-card { margin-top:14px; }
    .rec-found-card { padding:0; border-radius:18px;"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert '.rec-tabs + .rec-found-card' not in s, path + ': already spaced'
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
