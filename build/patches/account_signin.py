# -*- coding: utf-8 -*-
"""A way in for people who already have an account.

The last screen only offered to open a new one, which is the wrong
question for anyone who has been here before. A quiet line under the
button offers to sign in instead.

Both go to the same place, because the screen they open is the one that
already does both -- "Sign in or create your account to hire with Mira
AI". Two doors onto one room is honest here; two different rooms would
be a promise this page cannot keep.

The listeners are hung off a data attribute rather than a class, so the
re-wire that runs when a screen is reopened picks up both buttons
without knowing their names.
"""
import io
import sys

EDITS = [
    ("""                '<button type="button" class="rec-flow-next rec-ready-go">' +
                  'Open your account</button>' +""",
     """                '<button type="button" class="rec-flow-next rec-ready-go" ' +
                  'data-login="1">Open your account</button>' +
                '<p class="rec-ready-in">Already with Mira? ' +
                  '<button type="button" class="rec-ready-signin" ' +
                    'data-login="1">Sign in</button></p>' +"""),

    ("""          kept[2] = card.innerHTML;
          remember();
          var go = card.querySelector('.rec-ready-go');
          if (go) go.addEventListener('click', open_account);""",
     """          kept[2] = card.innerHTML;
          remember();
          card.querySelectorAll('[data-login]').forEach(function (b) {
            b.addEventListener('click', open_account);
          });"""),

    ("""      // re-injected HTML has no listeners of its own
      var back = face.querySelector('.rec-ready-go');
      if (back) back.addEventListener('click', open_account);""",
     """      // re-injected HTML has no listeners of its own
      face.querySelectorAll('[data-login]').forEach(function (b) {
        b.addEventListener('click', open_account);
      });"""),
]

CSS = """    .rec-ready-in { margin:14px 0 0; text-align:center; font-size:13.5px;
                    color:#8A82A8; }
    .rec-ready-signin { border:0; padding:0 2px; background:none;
                        font:inherit; font-size:13.5px; font-weight:600;
                        color:#6B4BE8; cursor:pointer;
                        text-decoration:underline;
                        text-underline-offset:3px; }
    .rec-ready-signin:hover { color:#4A32C0; }
"""

CSS_ANCHOR = "    .rec-ready-go { width:100%; margin-top:18px; }"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-ready-signin' not in s, path + ': already offers it'
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS_ANCHOR + '\n' + CSS, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
