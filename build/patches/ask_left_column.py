# -*- coding: utf-8 -*-
"""The question reads down one edge, with its actions at the ends.

The question screen was centred while every screen after it reads down
a left edge, so the flow changed axis the moment it got an answer. It
now uses the same column: 520px, left aligned, which also gives the
action row two ends to work with.

Continue sits at the start of that row and "I don't have a website" at
the far end, so the thing most people want is where the eye already is
and the way out is somewhere deliberate rather than beside it.
"""
import io
import sys

EDITS = [
    ("""      return '<h2 class="rec-flow-q' + (step.hint ? '' : ' is-alone') +""",
     """      return '<div class="rec-ask-col">' +
        '<h2 class="rec-flow-q' + (step.hint ? '' : ' is-alone') +"""),

    ("""          (step.skip ? '<button type="button" class="rec-flow-skip">' +
            esc(step.skip) + '</button>' : '') +
        '</div>';
    }""",
     """          (step.skip ? '<button type="button" class="rec-flow-skip">' +
            esc(step.skip) + '</button>' : '') +
        '</div>' +
        '</div>';
    }"""),
]

CSS = """    /* the question reads down the same edge every later screen does */
    .rec-ask-col { width:min(520px, 100%); margin-inline:auto;
                   text-align:left; }
    .rec-ask-col .rec-flow-act { justify-content:space-between; }
"""

CSS_ANCHOR = "    /* the found screen shares one left edge */"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-ask-col' not in s, path + ': already columned'
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS + CSS_ANCHOR, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
