# -*- coding: utf-8 -*-
"""Drop "Where will they work from?".

The step, the field it wrote to, its reset and its line on the review all
go together -- a key left on the brief that nothing ever sets would show
as "Not given" on every role.

What is left: website, budget, skills, then the review.
"""
import io
import sys

EDITS = [
    ("""      { key: 'location',
        q: 'Where will they work from?',
        chipsOnly: true,
        chips: ['Remote', 'Hybrid', 'On-site'] },
""", ""),

    ("""    var brief = { role: '', website: '', location: '', salary: '',
                  skills: [] };""",
     """    var brief = { role: '', website: '', salary: '', skills: [] };"""),

    ("""      brief.website = '';
      brief.location = '';""",
     """      brief.website = '';"""),

    ("""        ['Where', brief.location],
""", ""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert 'brief.location' not in s, path + ': a reference survives'
    assert 'work from?' not in s, path + ': the question survives'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
