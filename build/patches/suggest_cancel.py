# -*- coding: utf-8 -*-
"""Hiding the list also cancels whatever is still in flight.

The sequence guard only dropped a reply when a newer search had started.
Clearing the field, or typing a dot, called shut() without starting
one -- so a request already on its way came back afterwards and filled
the list again. Clearing "stri" and typing "wisemonk" showed Australia
and Stribro in 164ms: the old answer landing on a new word.

shut() takes a turn of the sequence now, so anything in flight is
already stale by the time it returns.
"""
import io
import sys

OLD = """        function shut() { sug.hidden = true; sug.innerHTML = ''; }"""
NEW = """        // taking a turn invalidates anything already on its way back
        function shut() { seq++; sug.hidden = true; sug.innerHTML = ''; }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, s.count(OLD))
    io.open(path, 'w', encoding='utf-8').write(s.replace(OLD, NEW, 1))
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
