# -*- coding: utf-8 -*-
"""The one destination left is written where you read it.

`APP` held the product's login URL for three places; two no longer go
anywhere, so a variable for the third buys nothing -- and an href built by
concatenation is invisible to anything reading the page as text, publish.py's
asset scan included, which is what noticed.
"""
import io
import sys

EDITS = [
    ("""                '<a class="login-switch-link" href="' + APP + '">Sign up</a></p>' +""",
     """                '<a class="login-switch-link" ' +
                  'href="https://talent.wisemonk.io/login">Sign up</a></p>' +"""),

    ("""    var APP = 'https://talent.wisemonk.io/login';
""",
     """"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:50], s.count(old))
        s = s.replace(old, new, 1)
    assert "' + APP + '" not in s, path + ': a built href is left'
    assert 'var APP' not in s, path + ': the variable is left'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
