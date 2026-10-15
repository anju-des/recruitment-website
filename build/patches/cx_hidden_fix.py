# -*- coding: utf-8 -*-
"""Make `hidden` actually hide the Connect button.

`.rec-cx { display:inline-flex }` is an author rule and the browser's
`[hidden] { display:none }` is a user-agent rule, so the button kept its
box and sat above the profile card it had just been replaced by. The two
siblings already carry the same guard; the button was the one that
needed it most and did not have it.
"""
import io
import sys

OLD = """    .rec-cx-take[hidden], .rec-co[hidden] { display:none; }"""
NEW = """    .rec-cx[hidden], .rec-cx-take[hidden], .rec-co[hidden] { display:none; }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, s.count(OLD))
    io.open(path, 'w', encoding='utf-8').write(s.replace(OLD, NEW, 1))
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
