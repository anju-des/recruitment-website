# -*- coding: utf-8 -*-
"""The two sign-in controls stop going anywhere.

They were anchors to talent.wisemonk.io/login, on the reasoning that a page
with no auth behind it should hand people to the one that has. Asked to take
the links off, so: Google becomes a button rather than a disguised link, and
the form keeps its preventDefault and does nothing after it.

The "Sign up" line underneath still points at the product -- it was not one
of the two named, and it is a link by its nature rather than a button that
looks like it does something.
"""
import io
import sys

EDITS = [
    # Google: an anchor pretending to be a button becomes a button
    ("""              '<a class="login-google-btn" href="' + APP + '">' + '<svg""",
     """              '<button type="button" class="login-google-btn">' + '<svg"""),

    ("""                'Continue with Google</a>' +""",
     """                'Continue with Google</button>' +"""),

    # Sign in: submit, and then nothing
    ("""      panel.querySelector('.login-form').addEventListener('submit', function (e) {
        e.preventDefault();
        window.location.href = APP;
      });""",
     """      // nothing behind it to sign anyone in, and nowhere it is meant to
      // send them: the submit is swallowed
      panel.querySelector('.login-form').addEventListener('submit', function (e) {
        e.preventDefault();
      });"""),

    # a <button> brings its own padding
    ("""      border:1.5px solid var(--border-strong); border-radius:10px;
      background:var(--neutral-0); font-family:inherit; font-size:15px;""",
     """      border:1.5px solid var(--border-strong); border-radius:10px; padding:0;
      background:var(--neutral-0); font-family:inherit; font-size:15px;"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:50], s.count(old))
        s = s.replace(old, new, 1)
    # the only destination left is the Sign up link
    assert s.count("' + APP + '") == 1, path + ': APP still used elsewhere'
    assert 'window.location.href = APP' not in s, path + ': sign in still goes'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
