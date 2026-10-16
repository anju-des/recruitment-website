# -*- coding: utf-8 -*-
"""The header asks for the thing the page wants, not for the exit.

A close button in the corner is the one control on this screen that
undoes everything on it. In its place, the offer: publish the role, for
nothing. It opens the same sign-in the last screen does, because that
is what publishing needs.

Escape still closes the flow -- that binding was always there beside
the button -- so the way out exists, it just is not the brightest
thing on the screen any more.
"""
import io
import sys

EDITS = [
    ("""          '<button type="button" class="rec-flow-x" aria-label="Close">&#215;</button>' +""",
     """          '<button type="button" class="rec-flow-cta" data-login="1">' +
            'Publish role for free</button>' +"""),

    ("""      flow.querySelector('.rec-flow-x').addEventListener('click', close);""",
     """      flow.querySelector('.rec-flow-cta')
          .addEventListener('click', open_account);"""),
]

CSS = """    .rec-flow-cta { padding:10px 18px; border:0; border-radius:100px;
                    background:#1A1430; color:#FFFFFF; font:inherit;
                    font-size:13.5px; font-weight:600; cursor:pointer;
                    transition:background .15s, transform .15s; }
    .rec-flow-cta:hover { background:#2C2545; transform:translateY(-1px); }
    .rec-flow-cta:focus-visible { outline:2px solid #7C5CF6;
                                  outline-offset:3px; }
    @media (prefers-reduced-motion: reduce) {
      .rec-flow-cta { transition:none; }
    }
    @media (max-width:560px) {
      .rec-flow-cta { padding:9px 14px; font-size:12.5px; }
    }
"""

# the close button's own styles go with it
DEAD = """    .rec-flow-x { width:36px; height:36px; border-radius:50%; border:0;"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-flow-cta' not in s, path + ': already asks'

    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    at = s.index(DEAD)
    end = s.index('.rec-flow-x:hover', at)
    end = s.index('\n', end) + 1
    s = s[:at] + CSS + s[end:]
    assert 'rec-flow-x' not in s, path + ': the close button survives'

    # Escape is the way out now, and it was already bound
    assert "if (e.key === 'Escape' && flow && !flow.hidden) close();" in s, \
        path + ': nothing closes the flow any more'

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
