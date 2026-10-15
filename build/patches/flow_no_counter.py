# -*- coding: utf-8 -*-
"""No "Step 1 of 4".

The bar across the top already says how far along this is, and it says it
without making anyone do arithmetic about how much is left.

The header is display:flex with justify-content:space-between over three
children, so removing the middle one leaves the logo at one end and the
close button at the other -- which is where they both belong anyway.
"""
import io
import sys

EDITS = [
    ("""          '<span class="rec-flow-step"></span>' +\n""", ""),

    ("""      // the gate is not one of the questions, so it takes no number
      flow.querySelector('.rec-flow-step').textContent =
        at > STEPS.length ? '' : 'Step ' + (at + 1) + ' of ' + total;
""", ""),

    ("""    .rec-flow-step { font-size:12.5px; color:#8A82A8; letter-spacing:.01em; }\n""",
     ""),

    # the confirmation screen cleared it as well
    ("""      flow.querySelector('.rec-flow-step').textContent = '';\n""", ""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert 'rec-flow-step' not in s, path + ': the counter survives'
    # the bar is what reports progress now, so it had better still be wired
    assert "rec-flow-bar span').style.setProperty" in s, path + ': bar lost'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
