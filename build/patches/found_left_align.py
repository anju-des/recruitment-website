# -*- coding: utf-8 -*-
"""The found screen reads down one left edge.

Everything was centred independently -- heading, paragraph, tiles, links
-- so each block had its own axis and the eye started in a different
place four times. A column the width of the company card, left aligned,
gives them one edge to share.

The column is the card's width rather than something wider, so the card
is no longer an island floating inside a looser layout: its left and
right edges are the edges of everything below it.
"""
import io
import sys

OPEN_OLD = """          card.innerHTML =
            '<h2 class="rec-flow-q is-alone">' +"""
OPEN_NEW = """          card.innerHTML =
            '<div class="rec-found-col">' +
            '<h2 class="rec-flow-q is-alone">' +"""

SHUT_OLD = """              : '');

          var again = card.querySelector('.rec-flow-back');"""
SHUT_NEW = """              : '') +
            '</div>';

          var again = card.querySelector('.rec-flow-back');"""

CSS = """    /* the found screen shares one left edge */
    .rec-found-col { width:min(420px, 100%); margin-inline:auto;
                     text-align:left; }
    .rec-found-col .rec-flow-q { text-align:left; }
    .rec-found-col .rec-flow-found { width:100%; margin-left:0;
                                     margin-right:0; }
    .rec-found-col .rec-found-about { max-width:none; margin-left:0;
                                      margin-right:0; }
    .rec-found-col .rec-found-facts,
    .rec-found-col .rec-found-links,
    .rec-found-col .rec-tell { justify-content:flex-start; }
    .rec-found-col .rec-flow-act { justify-content:flex-start; }
"""

CSS_ANCHOR = "    .rec-found-links { display:flex;"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-found-col' not in s, path + ': already in a column'
    for old, new in ((OPEN_OLD, OPEN_NEW), (SHUT_OLD, SHUT_NEW)):
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS + CSS_ANCHOR, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
