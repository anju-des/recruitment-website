# -*- coding: utf-8 -*-
"""A wider column, and the board screen says what it has made.

The column was 420px, which put "Nothing on that domain" across four
lines of a 24px heading. 520 gives the headings room without letting
the paragraph run past a comfortable measure, which its own max-width
still holds.

The board screen gets a heading and a subcopy instead of a two-word
label and a note tucked under the card. The subcopy names what the
board was built from -- the logo and name found in step one, the role
typed on the way in -- because that is the claim worth making: it is
theirs, not a template. And it carries the "goes live with your account"
line that was in the card, which is the honest half: nothing here is
published.
"""
import io
import sys

EDITS = [
    ("""    .rec-found-col { width:min(420px, 100%); margin-inline:auto;""",
     """    .rec-found-col { width:min(520px, 100%); margin-inline:auto;"""),

    ("""    .rec-flow.is-found .rec-flow-card { width:min(470px, 100%); }""",
     """    .rec-flow.is-found .rec-flow-card { width:min(520px, 100%); }"""),

    ("""              '<h2 class="rec-flow-q is-alone">Your job board</h2>' +""",
     """              '<h2 class="rec-flow-q">Your custom job board is ready' +
                '</h2>' +
              '<p class="rec-flow-hint">Built from your logo, your name and ' +
                'the role you described. It goes live with your account.</p>' +"""),

    ("""                '<p class="rec-board-note">A preview. The board goes live ' +
                  'with your account.</p>' +
""", ""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    js = s[s.rindex('<script>'):]
    assert 'rec-board-note' not in js, path + ': the old note survives'
    assert 'custom job board is ready' in js, path + ': no new heading'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
