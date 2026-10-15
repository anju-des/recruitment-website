# -*- coding: utf-8 -*-
"""The steps sit on the gradient, not on a white band.

The sand gradient started below the steps, so the row was a white strip
with the colour beginning underneath it -- a hard edge across the screen
for no reason. The gradient now starts above the row and the steps sit
on it.

Two things that had to move with it: the rule under the row, which only
existed to separate white from colour and now separates nothing; and the
stacking. The sand is a positioned element and the row was not, so the
gradient would have painted over the text; the row takes position and a
z-index of its own to stay on top.
"""
import io
import sys

OLD_MARKUP = """        '<ol class="rec-steps">' +
          ['Company details', 'Job board', 'Account']
            .map(function (s, i) {
              return '<li class="rec-step"><i>' + (i + 1) + '</i>' +
                '<b>' + s + '</b></li>';
            }).join('') +
        '</ol>' +
        '<div class="rec-flow-sand" aria-hidden="true"></div>' +"""

NEW_MARKUP = """        '<div class="rec-flow-sand" aria-hidden="true"></div>' +
        '<ol class="rec-steps">' +
          ['Company details', 'Job board', 'Account']
            .map(function (s, i) {
              return '<li class="rec-step"><i>' + (i + 1) + '</i>' +
                '<b>' + s + '</b></li>';
            }).join('') +
        '</ol>' +"""

OLD_CSS = """                 padding:15px clamp(18px, 3vw, 40px);
                 border-bottom:1px solid #F2EEFB; }"""
NEW_CSS = """                 padding:15px clamp(18px, 3vw, 40px);
                 /* the sand is positioned and this row was not, so without
                    a layer of its own the gradient paints over the text */
                 position:relative; z-index:1; }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in ((OLD_MARKUP, NEW_MARKUP), (OLD_CSS, NEW_CSS)):
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    js = s[s.rindex('<script>'):]
    assert js.index('rec-flow-sand') < js.index('rec-steps'), \
        path + ': the gradient still starts below the steps'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
