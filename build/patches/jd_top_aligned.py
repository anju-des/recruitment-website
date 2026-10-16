# -*- coding: utf-8 -*-
"""The screen starts at the top, not in the middle of the window.

Vertical centring suited a screen that was one question and a button.
Now the first thing in the column is a heading and the last is a
sign-in, and centring a column that nearly fills the window only moves
where it begins -- high on a tall display, low on a short one, never
the same place twice.

The auto margin stays on the horizontal axis, where it does the
centring that is wanted. On the vertical it becomes nothing, which with
align-items:flex-start is a column that starts at the top and scrolls
all of itself.
"""
import io
import sys

OLD = "    .rec-flow-card { width:min(680px, 100%); margin:auto; }"
NEW = ("    /* auto across, nothing down: centred in the column, top of the\n"
       "       window, and still scrollable when it is taller than one */\n"
       "    .rec-flow-card { width:min(680px, 100%); margin:0 auto; }")


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, 'card', s.count(OLD))
    s = s.replace(OLD, NEW, 1)
    assert 'align-items:flex-start;\n                     justify-content' in s, \
        path + ': the body no longer starts its items at the top'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
