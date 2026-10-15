# -*- coding: utf-8 -*-
"""The heading is "Your company".

"Found your company" announced the lookup; the badge on the card
already does that, and by the time anyone reads the heading the finding
is over. What the screen holds is the company.
"""
import io
import sys

OLD = "(blank ? 'Nothing on that domain' : 'Found your company')"
NEW = "(blank ? 'Nothing on that domain' : 'Your company')"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, s.count(OLD))
    s = s.replace(OLD, NEW, 1)
    assert 'Found your company' not in s, path + ': the old heading survives'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
