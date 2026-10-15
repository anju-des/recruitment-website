# -*- coding: utf-8 -*-
"""No role typed, no listing invented.

"Your first role" was a placeholder standing where a real listing goes,
on a board that is otherwise entirely made of true things -- their logo,
their name, their location. A row that looks like a posting and is not
one is the only thing on the screen pretending.

With nothing typed the row is simply absent, and the working line says
what it is actually doing instead of naming a role that does not exist.
"""
import io
import sys

EDITS = [
    ("""        var title = (brief.role || '').split(',')[0].trim() ||
                    'Your first role';""",
     """        var title = (brief.role || '').split(',')[0].trim();"""),

    ("""          'writing up ' + title,""",
     """          title ? 'writing up ' + title : 'setting it up for your roles',"""),

    ("""                '<div class="rec-board-role">' +
                  '<b>' + esc(title) + '</b>' +
                  (found.based ? '<i>' + esc(found.based) + '</i>' : '') +
                '</div>' +""",
     """                (title
                  ? '<div class="rec-board-role">' +
                      '<b>' + esc(title) + '</b>' +
                      (found.based ? '<i>' + esc(found.based) + '</i>' : '') +
                    '</div>'
                  : '') +"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    js = s[s.rindex('<script>'):]
    assert 'Your first role' not in js, path + ': the placeholder survives'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
