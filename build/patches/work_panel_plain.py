# -*- coding: utf-8 -*-
"""The working panel loses its container, and its green.

The tinted box was a second surface inside a screen that is already one
surface. Without it the lines sit on the page, which is what the
reference does too.

Green was the only green on the page -- it read as a system status
colour borrowed from somewhere else. The dot and the ticks take the
violet everything else here uses.
"""
import io
import sys

EDITS = [
    ("""    .rec-work { display:inline-block; margin-top:26px; padding:16px 22px;
                border-radius:14px; background:#F6F5FC; text-align:left;""",
     """    .rec-work { display:inline-block; margin-top:26px; text-align:left;"""),

    ("""                    background:#12B76A;
                    animation:rec-work-pulse 1.5s ease-in-out infinite; }""",
     """                    background:#7C5CF6;
                    animation:rec-work-pulse 1.5s ease-in-out infinite; }"""),

    ("""    .rec-work-line.is-done i { color:#12B76A; }""",
     """    .rec-work-line.is-done i { color:#7C5CF6; }"""),

    ("""    @media (max-width:600px) {
      .rec-work { font-size:12px; padding:14px 16px; }""",
     """    @media (max-width:600px) {
      .rec-work { font-size:12px; }"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert '#12B76A' not in s[s.index('.rec-work'):s.index('.rec-found-about')], \
        path + ': green is left in the panel'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
