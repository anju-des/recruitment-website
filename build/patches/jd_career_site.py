# -*- coding: utf-8 -*-
"""The job board is a career site.

Everywhere a person reads it: the step, the card, the panel's heading,
and the two lines on the screen that builds it. The address it is given
does not change -- that is what the thing is called on the internet --
and board_addr keeps its name, because renaming a function nobody sees
only makes the next diff harder to read.

The one line left saying "job board" is the parser's, about how a job
board writes a location, which is about job boards in general and not
about this one.
"""
import io
import sys

EDITS = [
    ("""            ['Company details', 'Job board', 'Role details']""",
     """            ['Company details', 'Career site', 'Role details']"""),

    ("""        rail_set(1, 'board', 'Board', said ? '1 role' : '', [""",
     """        rail_set(1, 'board', 'Career site', said ? '1 role' : '', ["""),

    ("""            '<h2 class="rec-flow-q is-alone">Building your job board</h2>' +""",
     """            '<h2 class="rec-flow-q is-alone">Building your career ' +
              'site</h2>' +"""),

    ("""              '<h2 class="rec-flow-q">Your custom job board is ready' +""",
     """              '<h2 class="rec-flow-q">Your career site is ready' +"""),

    ("""            put_mini(1, 'Job board', board_addr(found.who),""",
     """            put_mini(1, 'Career site', board_addr(found.who),"""),

    ("""      if (screens[1]) { put_mini(1, 'Job board', board_addr(was.who),""",
     """      if (screens[1]) { put_mini(1, 'Career site', board_addr(was.who),"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    # what a person reads, gone; the parser's own comment, left alone
    left = [l for l in s.split('\n') if 'job board' in l.lower()]
    assert len(left) == 1 and 'how a job board writes one' in left[0], \
        (path, left)

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
