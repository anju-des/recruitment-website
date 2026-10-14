# -*- coding: utf-8 -*-
"""Sand under the brief screen's header, purple into blue.

It is a zero-height element sitting between the rail and the body, painting
downward out of itself. That is what puts it exactly at the top of the body
without anyone having to know how tall the header above it happens to be --
and it keeps the band out of the body, which scrolls, so the wash stays put
while the questions move under it.
"""
import io
import sys

NOISE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
         "width='180' height='180'%3E%3Cfilter id='b'%3E%3CfeTurbulence "
         "type='fractalNoise' baseFrequency='0.62' numOctaves='3' "
         "stitchTiles='stitch'/%3E%3CfeColorMatrix type='matrix' "
         "values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 "
         "0.33 0.33 0.33 0 -0.17'/%3E%3C/filter%3E%3Crect "
         "width='180' height='180' filter='url(%23b)'/%3E%3C/svg%3E\")")

FADE = ("linear-gradient(to bottom, #000 0%, rgba(0,0,0,.66) 42%, "
        "transparent 100%)")

CSS = """    /* Sand under the header, purple into blue. A zero-height element
       between the rail and the body, painting downward out of itself: that
       puts it at the top of the body without knowing how tall the header is,
       and keeps it out of the body, which scrolls. */
    .rec-flow-sand { position:relative; height:0; z-index:0; }
    .rec-flow-sand::before { content:""; position:absolute;
                             top:0; left:0; right:0;
                             height:clamp(190px, 34vh, 360px);
                             pointer-events:none;
                             background:linear-gradient(118deg,
                               rgba(168,138,255,.58) 0%,
                               rgba(134,148,255,.50) 52%,
                               rgba(118,178,255,.42) 100%);
                             -webkit-mask-image:@NOISE@, @FADE@;
                             mask-image:@NOISE@, @FADE@;
                             -webkit-mask-size:150px 150px, auto;
                             mask-size:150px 150px, auto;
                             -webkit-mask-composite:source-in;
                             mask-composite:intersect; }
    /* the questions sit over it */
    .rec-flow-card { position:relative; z-index:1; }
""".replace('@NOISE@', NOISE).replace('@FADE@', FADE)

CSS_ANCHOR = """    .rec-flow-body { flex:1; min-height:0; overflow:auto;"""

MARKUP_OLD = """        '<div class="rec-flow-bar"><span></span></div>' +
        '<div class="rec-flow-body">"""
MARKUP_NEW = """        '<div class="rec-flow-bar"><span></span></div>' +
        '<div class="rec-flow-sand" aria-hidden="true"></div>' +
        '<div class="rec-flow-body">"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-flow-sand' not in s, path + ': already has the sand'

    assert s.count(CSS_ANCHOR) == 1, path + ': flow body rule changed'
    s = s.replace(CSS_ANCHOR, CSS + CSS_ANCHOR, 1)

    assert s.count(MARKUP_OLD) == 1, path + ': flow markup changed'
    s = s.replace(MARKUP_OLD, MARKUP_NEW, 1)

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
