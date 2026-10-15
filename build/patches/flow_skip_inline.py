# -*- coding: utf-8 -*-
"""Continue and the skip on one line.

The action row was already a centred flex with a 12px gap, so the link
only had to move inside it and give up the block display and auto margins
that were stacking it underneath.
"""
import io
import sys

OLD_MARKUP = """          (step.chipsOnly && !step.multi ? '' :
            '<button type="button" class="rec-flow-next">Continue</button>') +
        '</div>' +
        (step.skip ? '<button type="button" class="rec-flow-skip">' +
          esc(step.skip) + '</button>' : '');"""

NEW_MARKUP = """          (step.chipsOnly && !step.multi ? '' :
            '<button type="button" class="rec-flow-next">Continue</button>') +
          (step.skip ? '<button type="button" class="rec-flow-skip">' +
            esc(step.skip) + '</button>' : '') +
        '</div>';"""

OLD_CSS = """    .rec-flow-skip { display:block; margin:18px auto 0; border:0; padding:2px;"""
NEW_CSS = """    .rec-flow-skip { margin:0; border:0; padding:2px 4px;"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in ((OLD_MARKUP, NEW_MARKUP), (OLD_CSS, NEW_CSS)):
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
