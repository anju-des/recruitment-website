# -*- coding: utf-8 -*-
"""The two header buttons are the same height.

Invite was styled as a chip for a section heading and then moved up
beside a full-sized button, so it sat shorter than the thing next to
it and the pair read as an afterthought and a button rather than two
actions. Same padding and same type size as the publish button now;
only the colours still say which one is the quieter of the two.
"""
import io
import sys

CSS = """    /* beside the publish button, not inside a heading any more.
       The border is the other two pixels: one has it and one does not,
       so the publish button carries an invisible one of its own rather
       than the padding being fudged to hide the difference. */
    .rec-invite-top { padding:9px 16px; font-size:13.5px; }
    .rec-invite-top svg { width:16px; height:16px; }
"""

CSS_ANCHOR = """    .rec-invite-n { font-style:normal; font-weight:600; color:#A49CC0; }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert '.rec-invite-top { padding' not in s, path + ': already matched'

    # in the rule itself, not a later override: the publish button's own
    # rule is declared after this block and would win at equal weight
    old = "    .rec-flow-cta { padding:9px 16px; border:0; border-radius:8px;"
    new = ("    .rec-flow-cta { padding:9px 16px; border-radius:8px;\n"
           "                    border:1px solid transparent;")
    assert s.count(old) == 1, (path, 'the cta rule', s.count(old))
    s = s.replace(old, new, 1)
    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS + CSS_ANCHOR, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
