# -*- coding: utf-8 -*-
"""Footer: the mark grown down onto the rule, the nav in one row, the
copyright moved over to the right.

The mark moves inside the block above the rule and is pinned to its bottom.
An absolutely positioned child is laid out against its ancestor's padding
box, and that block's padding box ends exactly where the rule's border
begins -- so `bottom: 0` puts the mark on the rule without anyone having to
know how tall the line beneath it happens to be.

Platform goes, and with three columns left they fit on one line, which is
what frees the height the mark now takes.
"""
import io
import sys

MARK_OLD = """      <footer class="rec-foot">
        <span class="rec-foot-mark" aria-hidden="true">
          <svg viewBox="0 0 412 300">
            <rect width="412" height="300" fill="url(#rec-metal)"
                  mask="url(#rec-logo)"/>
          </svg>
        </span>
        <div class="rec-foot-inner">
"""
MARK_NEW = """      <footer class="rec-foot">
        <div class="rec-foot-inner">
          <span class="rec-foot-mark" aria-hidden="true">
            <svg viewBox="0 0 412 300">
              <rect width="412" height="300" fill="url(#rec-metal)"
                    mask="url(#rec-logo)"/>
            </svg>
          </span>
"""

PLATFORM = """            <div class="rec-foot-col">
              <h3>Platform</h3>
              <ul>
                <li><a href="#screening">Screening</a></li>
                <li><a href="#interviews">Interviews</a></li>
                <li><a href="#scorecards">Scorecards</a></li>
                <li><a href="#offers">Offers</a></li>
              </ul>
            </div>
"""

POS_OLD = """    .rec-foot-mark { position:absolute; z-index:0; pointer-events:none;
                     left:clamp(22px, 4.5vw, 110px);
                     bottom:clamp(76px, 11vh, 132px);
                     width:clamp(104px, 11vw, 188px); aspect-ratio:412 / 300;"""
POS_NEW = """    /* `bottom: 0` of the block above the rule puts it on the rule: an
       absolutely positioned child is laid out against its ancestor's padding
       box, and that box ends exactly where the rule's border begins -- so
       nothing here has to know how tall the line beneath it is */
    .rec-foot-mark { position:absolute; z-index:0; pointer-events:none;
                     left:0; bottom:0;
                     width:clamp(170px, 21vw, 360px); aspect-ratio:412 / 300;"""

INNER_OLD = """    .rec-foot-inner { position:relative; width:100%; margin:auto 0;"""
INNER_OLD_ALT = """    .rec-foot-inner { width:100%; margin:auto 0;"""
INNER_NEW = """    .rec-foot-inner { position:relative; width:100%; margin:auto 0;"""

COLS_OLD = """    .rec-foot-cols { display:grid;
                     grid-template-columns:repeat(2, minmax(150px, 240px));
                     gap:clamp(28px, 4vh, 48px) clamp(24px, 3vw, 72px); }"""
COLS_NEW = """    /* three of them now, so they fit on one line */
    .rec-foot-cols { display:grid;
                     grid-template-columns:repeat(3, minmax(126px, 200px));
                     gap:clamp(28px, 4vh, 48px) clamp(22px, 2.6vw, 56px); }"""

BASE_OLD = """                     display:flex; flex-wrap:wrap; gap:14px 28px;
                     align-items:center; justify-content:space-between; }"""
BASE_NEW = """                     display:flex; flex-wrap:wrap; gap:14px 32px;
                     align-items:center; justify-content:flex-end; }"""

# the nav is narrower now, and on a middling screen three columns want room
MQ_OLD = """    @media (max-width:860px) {
      .rec-foot-inner { grid-template-columns:1fr; }
    }"""
MQ_NEW = """    @media (max-width:1100px) {
      .rec-foot-inner { grid-template-columns:1fr; }
      .rec-foot-mark { display:none; }
    }
    @media (max-width:560px) {
      .rec-foot-cols { grid-template-columns:repeat(2, minmax(0, 1fr)); }
    }"""

MARK_MQ_OLD = """    /* once the footer stacks there is no spare corner to put it in */
    @media (max-width:860px) { .rec-foot-mark { display:none; } }
"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()

    assert s.count(MARK_OLD) == 1, path + ': footer head changed'
    s = s.replace(MARK_OLD, MARK_NEW, 1)

    assert s.count(PLATFORM) == 1, path + ': platform column changed'
    s = s.replace(PLATFORM, '', 1)

    assert s.count(POS_OLD) == 1, path + ': mark rule changed'
    s = s.replace(POS_OLD, POS_NEW, 1)

    if INNER_OLD not in s:
        assert s.count(INNER_OLD_ALT) == 1, path + ': inner rule changed'
        s = s.replace(INNER_OLD_ALT, INNER_NEW, 1)

    for old, new in ((COLS_OLD, COLS_NEW), (BASE_OLD, BASE_NEW),
                     (MQ_OLD, MQ_NEW), (MARK_MQ_OLD, '')):
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    assert 'Screening' not in s.split('<footer')[1], path + ': platform left'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
