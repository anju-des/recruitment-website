# -*- coding: utf-8 -*-
"""Industry or a company directory, and one row per domain.

Legal form, founder and chief executive let a Czech town through --
places have founders, and some carry a legal form. Industry (P452) and
an entry in a company directory (Crunchbase, LinkedIn) are the two that
only an organisation has.

And "Infosys limited" and "Infosys Consulting" both resolved to
infosys.com, which is two rows that do the same thing. The first one
for a domain wins.
"""
import io
import sys

EDITS = [
    ("""                    if (!(c.P452 || c.P2088 || c.P4264 || c.P1454 ||
                          c.P169 || c.P112)) return;""",
     """                    if (!(c.P452 || c.P2088 || c.P4264)) return;"""),

    ("""                    if (!host) return;
                    rows.push({""",
     """                    if (!host) return;
                    // two names for one domain is one suggestion
                    for (var k = 0; k < rows.length; k++) {
                      if (rows[k].host === host) return;
                    }
                    rows.push({"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
