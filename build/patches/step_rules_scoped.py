# -*- coding: utf-8 -*-
"""The rail's rules were written for the rail's own row, so say so.

`.rec-step i` was the numbered circle and `.rec-step b` the step's name,
back when the row was all a step contained. A step now also holds a chip,
and the chip's second line is an `<i>` -- which the circle rule turned
into a 20px disc and clipped to "wis". The chip's name was quietly
losing its weight to `.rec-step b` for the same reason.

Each of these now names `.rec-step-row`, which is what they were always
describing.
"""
import io
import sys

EDITS = [
    (".rec-step i { font-style:normal;", ".rec-step-row i { font-style:normal;"),
    (".rec-step b { font-weight:500; }", ".rec-step-row b { font-weight:500; }"),
    (".rec-step.is-on i {", ".rec-step.is-on .rec-step-row i {"),
    (".rec-step.is-on b {", ".rec-step.is-on .rec-step-row b {"),
    (".rec-step.is-busy i {", ".rec-step.is-busy .rec-step-row i {"),
    # the rule and its reduced-motion twin
    (".rec-step.is-busy i::after {", ".rec-step.is-busy .rec-step-row i::after {", 2),
    (".rec-step.is-done i {", ".rec-step.is-done .rec-step-row i {"),
    ("      .rec-step b { display:none; }", "      .rec-step-row b { display:none; }"),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for edit in EDITS:
        old, new = edit[0], edit[1]
        want = edit[2] if len(edit) > 2 else 1
        assert s.count(old) == want, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new)
    css = s[:s.rindex('<script>')]
    import re
    left = re.findall(r'\.rec-step[a-z.-]*\s+[ib]\b', css)
    assert not [x for x in left if 'row' not in x], (path, left)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
