# -*- coding: utf-8 -*-
"""board() builds the address itself, so give it the shared function.

The chip's new second line was handed `addr`, a name that belongs to the
account step. board() writes the same address inline in its own markup
and never named it, so the chip threw -- and because the throw happened
inside the timeout that tucks the board away, the flow stopped there:
step two ticked, the screen stayed put, step three never started.

Both uses now go through board_addr, which is where that formula was
supposed to end up.
"""
import io
import sys

EDITS = [
    ("""                    '<i>' + esc(found.who.toLowerCase().replace(/[^a-z0-9]/g,
                      '')) + '.mira.jobs</i></span>' +""",
     """                    '<i>' + esc(board_addr(found.who)) + '</i></span>' +"""),

    ("""            put_mini(1, 'Job board', addr, found.logo, card.innerHTML);""",
     """            put_mini(1, 'Job board', board_addr(found.who),
                     found.logo, card.innerHTML);"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    js = s[s.rindex('<script>'):]
    assert js.count("'.mira.jobs'") == 1, (path, 'the formula is not alone')
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
