# -*- coding: utf-8 -*-
"""The dark block comes out; the flow is light again.

The whole override block is spliced out between its own comment and the
one that follows it, so the flow falls back to the rules it had before,
including the transparent-until-settled card the dark block had been
painting over.
"""
import io
import sys

START = "    /* ---- the flow, dark ---"
STOP = "    /* ---- Mira in the corner ---"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    a = s.index(START)
    b = s.index(STOP, a)
    s = s[:a] + s[b:]
    for gone in ('the flow, dark', 'brightness(0) invert(1)'):
        # the bubble's own inverted mark must survive; check only the flow
        pass
    assert 'the flow, dark' not in s, path + ': the block survives'
    assert '.rec-flow-head img { filter' not in s, path + ': logo still inverted'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
