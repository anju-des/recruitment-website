# -*- coding: utf-8 -*-
"""The workspace row carries the company's mark, not just its name.

"Wise" on its own is a word. "Wise" next to the logo that was fetched
two steps ago is this company's workspace, and it ties the last screen
back to the first.

Same mark the chip in the rail uses -- the fetched logo, or the first
letter on the gradient when there was none -- so the page has one way of
drawing a company and not two.
"""
import io
import sys

EDITS = [
    ("""                  '<li><i>Workspace</i><b>' + esc(found.who) + '</b></li>' +""",
     """                  '<li><i>Workspace</i><span class="rec-ready-who">' +
                    '<span class="rec-done-mark">' +
                      (found.logo
                        ? '<img src="' + esc(found.logo) + '" alt="">'
                        : esc(String(found.who || '?').charAt(0))) +
                    '</span><b>' + esc(found.who) + '</b></span></li>' +"""),
]

CSS = """    .rec-ready-who { display:inline-flex; align-items:center; gap:9px;
                     min-width:0; }
"""

CSS_ANCHOR = "    .rec-ready-go { width:100%; margin-top:18px; }"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-ready-who' not in s, path + ': already has the mark'
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS_ANCHOR + '\n' + CSS, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
