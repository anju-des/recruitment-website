# -*- coding: utf-8 -*-
"""Step two plays in the middle, and the recovery reads as a button.

Step one tucks away by adding is-found, and nothing took it off again,
so step two inherited the tucked layout: its working panel and its
finished board both rendered into the corner column that exists for
things already put away. Step two clears it on the way in and sets it
again when it tucks, exactly as step one does.

And "Try another website" was styled as the secondary half of a pair of
buttons, which it was until it became the only thing on the screen.
Alone, with no background and no border, it reads as a heading. It takes
a border and a surface so it reads as the control it is.
"""
import io
import sys

EDITS = [
    ("""      function board() {
        if (!found.who) return;
        step_busy(1);""",
     """      function board() {
        if (!found.who) return;
        // step one tucked itself away; step two gets the middle back
        flow.classList.remove('is-found');
        open_i = null;
        step_busy(1);"""),

    ("""                '<div class="rec-flow-act">' +
                  '<button type="button" class="rec-flow-back">Try another ' +
                    'website</button>' +
                '</div>'""",
     """                '<div class="rec-flow-act">' +
                  '<button type="button" class="rec-flow-back rec-flow-again">' +
                    'Try another website</button>' +
                '</div>'"""),
]

CSS = """    /* alone on the miss screen it is the only control, so it looks like one */
    .rec-flow-again { border:1.5px solid #DCD6EE; background:#FFFFFF;
                      color:#4B4270; padding-inline:22px;
                      transition:background .15s, border-color .15s,
                                 color .15s; }
    .rec-flow-again:hover { border-color:#BCAEF0; background:#F7F5FE;
                            color:#1A1430; }
"""

CSS_ANCHOR = "    .rec-flow-back:hover { color:#1A1430; }\n"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-flow-again' not in s, path + ': already done'
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS_ANCHOR + CSS, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
