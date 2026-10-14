# -*- coding: utf-8 -*-
"""Take the mark out of the footer, and everything that was there for it.

The room reserved under the words, the deepened floor it hung into and the
rule that hid it on narrow screens all existed only to hold it, so they go
with it. The footer's floor goes back to what it was before, which also
brings the block back up to where it sat.
"""
import io
import sys

MARKUP = """          <span class="rec-foot-mark" aria-hidden="true">
            <svg viewBox="0 0 412 300">
              <rect width="412" height="300" fill="url(#rec-metal)"
                    mask="url(#rec-logo)"/>
            </svg>
          </span>
"""

CSS_HEAD = """    /* The mark in the corner, borrowing the metal and the logo mask the"""
CSS_TAIL = """    .rec-foot-base { width:100%;"""

PAD_OLD = """                      /* the room the mark stands in, and the only thing
                         holding the block off the rule -- so trimming it is
                         what moves the words down. Sized off the width like
                         the mark is, so the two cannot drift apart at some
                         screen and leave it sitting on the socials */
                      padding-bottom:clamp(100px, 11vw, 200px); }"""
PAD_NEW = """                      padding-bottom:clamp(44px, 7vh, 84px); }"""

FLOOR_OLD = """                /* the deeper floor is what the mark hangs into: without it
                   there is only the rule, a line of text and 34px under here,
                   and the drop below runs out of page */
                padding:clamp(48px, 7vh, 96px) clamp(22px, 4.5vw, 110px)
                        clamp(34px, 8vh, 110px);"""
FLOOR_NEW = """                padding:clamp(48px, 7vh, 96px) clamp(22px, 4.5vw, 110px)
                        clamp(26px, 4vh, 48px);"""

INNER_OLD = """    /* `auto` on the top margin only: with it on both, the spare height split
       above and below and left a gap between this block and the rule, which
       the mark was then pinned to the wrong side of */
    .rec-foot-inner { position:relative; width:100%; margin:auto 0 0;"""
INNER_NEW = """    /* `auto` on the top margin only, so the block sits on the rule rather
       than floating in the middle of whatever height is spare */
    .rec-foot-inner { width:100%; margin:auto 0 0;"""

MQ_OLD = """      .rec-foot-inner { grid-template-columns:1fr;
                        /* no mark down here, so no room to keep for it */
                        padding-bottom:clamp(36px, 6vh, 64px); }
      .rec-foot-mark { display:none; }"""
MQ_NEW = """      .rec-foot-inner { grid-template-columns:1fr; }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()

    assert s.count(MARKUP) == 1, path + ': mark markup changed'
    s = s.replace(MARKUP, '', 1)

    a = s.index(CSS_HEAD)
    b = s.index(CSS_TAIL, a)
    assert 'rec-foot-mark' in s[a:b], path + ': not the mark CSS'
    s = s[:a] + s[b:]

    for old, new in ((PAD_OLD, PAD_NEW), (FLOOR_OLD, FLOOR_NEW),
                     (INNER_OLD, INNER_NEW), (MQ_OLD, MQ_NEW)):
        assert s.count(old) == 1, (path, old.strip()[:40], s.count(old))
        s = s.replace(old, new, 1)

    assert 'rec-foot-mark' not in s, path + ': a reference is left'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
