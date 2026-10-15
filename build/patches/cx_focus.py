# -*- coding: utf-8 -*-
"""Open on the card, not on Close.

Focus was landing on the dismiss button, so the first thing a keyboard --
and the focus ring -- pointed at was the way out of a panel nobody had read
yet. The card takes focus instead, which still puts the screen reader at the
top of the dialog and leaves Close one Tab away.
"""
import io
import sys

EDITS = [
    ("""        '<div class="rec-cxp-card">' +""",
     """        '<div class="rec-cxp-card" tabindex="-1">' +"""),

    ("""      panel.querySelector('.rec-cxp-x').focus();""",
     """      panel.querySelector('.rec-cxp-card').focus();"""),

    ("""    .rec-cxp-top { display:flex; align-items:center; gap:10px;""",
     """    .rec-cxp-card:focus { outline:none; }
    .rec-cxp-top { display:flex; align-items:center; gap:10px;"""),
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
