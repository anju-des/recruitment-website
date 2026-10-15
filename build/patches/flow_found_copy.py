# -*- coding: utf-8 -*-
"""Tell them, do not ask them.

"Is this you?" made the lookup sound unsure of itself, and put the work of
confirming on someone who had just typed their own domain. "Found your
company" reports what happened; Change is still there for the times it is
wrong.

The button follows the heading: "Yes, continue" was answering a question
that is no longer asked.
"""
import io
import sys

EDITS = [
    ("""          '<h2 class="rec-flow-q is-alone">Is this you?</h2>' +""",
     """          '<h2 class="rec-flow-q is-alone">Found your company</h2>' +"""),

    ("""            '<button type="button" class="rec-flow-next">Yes, continue' +
              '</button>' +""",
     """            '<button type="button" class="rec-flow-next">Continue' +
              '</button>' +"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert 'Is this you' not in s, path + ': the question survives'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
