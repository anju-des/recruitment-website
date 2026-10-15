# -*- coding: utf-8 -*-
"""The budget band in dollars.

Thousands a year, from 20 to 300 in fives, which is a range that holds both
an early engineer and a principal one. The top of the scale carries a plus,
because a band that stops dead at its maximum reads as a cap the person
chose rather than the end of the slider.
"""
import io
import sys

EDITS = [
    ("        range: { min: 4, max: 80, step: 1 } },",
     "        range: { min: 20, max: 300, step: 5 } },"),

    ("    var band = { from: 18, to: 24 };",
     "    var band = { from: 90, to: 120 };   // thousands a year"),

    ("      return n >= top ? n + '+' : String(n);",
     "      return '$' + n + 'k' + (n >= top ? '+' : '');"),

    ("""      return money(band.from, r.max) + '\\u2013' + money(band.to, r.max) + ' LPA';""",
     """      return money(band.from, r.max) + '\\u2013' + money(band.to, r.max);"""),

    ("""        '<div class="rec-flow-ends"><span>' + r.min + ' LPA</span><span>' +
          r.max + '+ LPA</span></div>' +""",
     """        '<div class="rec-flow-ends"><span>$' + r.min + 'k</span><span>$' +
          r.max + 'k+</span></div>' +"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert 'LPA' not in s, path + ': an LPA is left'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
