# -*- coding: utf-8 -*-
"""Sand across the foot of the page, in dark purple and blue.

The same build as the hero's: the wash is what gets painted and the noise is
a mask over it, so the speckles carry the colour instead of draining it the
way grey grain on `overlay` did. A second mask layer fades the whole thing
out going up and the two intersect.

Darker and more saturated than the hero's, because down here it is lifting a
near-black rather than tinting a white.

The mask needs its noise in the alpha channel: `mask-mode: luminance` is too
new to lean on, while an alpha mask is the default everywhere. So the colour
matrix writes white into RGB and the turbulence into A, offset so the mean
lands near the middle instead of near opaque.
"""
import io
import sys

NOISE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
         "width='180' height='180'%3E%3Cfilter id='f'%3E%3CfeTurbulence "
         "type='fractalNoise' baseFrequency='0.62' numOctaves='3' "
         "stitchTiles='stitch'/%3E%3CfeColorMatrix type='matrix' "
         "values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 "
         "0.33 0.33 0.33 0 -0.28'/%3E%3C/filter%3E%3Crect "
         "width='180' height='180' filter='url(%23f)'/%3E%3C/svg%3E\")")

FADE = ("linear-gradient(to top, transparent 0%, rgba(0,0,0,.95) 14%, "
        "rgba(0,0,0,.72) 52%, transparent 100%)")

CSS = """    /* Sand across the foot of the page. The wash is what is painted and the
       noise is a mask over it, so the speckles carry the colour rather than
       draining it; a second mask layer fades it out going up and the two
       intersect. Darker than the hero's, since here it lifts a near-black
       instead of tinting a white. */
    .rec-foot::after { content:""; position:absolute; inset:auto 0 0 0;
                       height:78%%; z-index:0; pointer-events:none;
                       opacity:calc(var(--fin, 0) * .82);
                       background:linear-gradient(162deg,
                         rgba(128,86,232,.86) 0%%, rgba(96,78,228,.80) 48%%,
                         rgba(62,88,226,.74) 100%%);
                       -webkit-mask-image:%s, %s;
                       mask-image:%s, %s;
                       -webkit-mask-size:150px 150px, auto;
                       mask-size:150px 150px, auto;
                       -webkit-mask-composite:source-in;
                       mask-composite:intersect; }
    /* the footer's own content stays above the grain */
    .rec-foot-inner, .rec-foot-base { position:relative; z-index:1; }
""" % (NOISE, FADE, NOISE, FADE)

ANCHOR = """    .rec-foot-inner { width:100%; margin:auto 0 0;"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert '.rec-foot::after' not in s, path + ': already has sand'
    assert s.count(ANCHOR) == 1, path + ': inner rule changed'
    s = s.replace(ANCHOR, CSS + ANCHOR, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
