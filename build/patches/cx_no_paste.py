# -*- coding: utf-8 -*-
"""The paste box goes.

Connect opens Claude with the question, and that is all it does now.

This removes the only route the reply had back into the page, so the
profile card can no longer be filled from here. The card, its parser and
its storage stay: a profile already saved still renders, and whatever
fills it next -- a clipboard read, a lookup, the brief itself -- hands it
the same object. Removing that too would be throwing away the part that
was not in question.

build() is spliced out between anchors rather than matched whole: the file
carries a real em-dash where the patch that wrote it used an escape, so an
exact match of that block is not dependable.
"""
import io
import sys

NEW_BUILD = """    function build() {
      card = document.createElement('div');
      card.className = 'rec-co';
      card.hidden = true;
      row.appendChild(card);
    }

"""

EDITS = [
    ("""    ask.addEventListener('click', function () {
      window.open('https://claude.ai/new?q=' + encodeURIComponent(PROMPT),
                  '_blank', 'noopener');
      ask.hidden = true;
      take.hidden = false;
      take.querySelector('textarea').focus();
    });""",
     """    ask.addEventListener('click', function () {
      window.open('https://claude.ai/new?q=' + encodeURIComponent(PROMPT),
                  '_blank', 'noopener');
    });"""),

    ("""    var take, card;""", """    var card;"""),

    ("""      ask.hidden = true;
      take.hidden = true;
      card.hidden = false;""",
     """      ask.hidden = true;
      card.hidden = false;"""),

    ("""        card.hidden = true;
        take.hidden = true;
        ask.hidden = false;""",
     """        card.hidden = true;
        ask.hidden = false;"""),
]

CSS_FROM = "    .rec-cx[hidden], .rec-cx-take[hidden], .rec-co[hidden]"
CSS_TO = "\n    .rec-co { display:flex;"


def patch(path):
    s = io.open(path, encoding='utf-8').read()

    # the Connect build(), by anchor rather than by text
    k = s.index("      take = document.createElement('div');")
    a = s.rindex("    function build() {", 0, k)
    b = s.index("    build();", k)
    s = s[:a] + NEW_BUILD + s[b:]

    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    # the stylesheet block for the box, up to where the card's rules begin
    ca = s.index(CSS_FROM)
    cb = s.index(CSS_TO, ca)
    s = s[:ca] + "    .rec-cx[hidden], .rec-co[hidden] { display:none; }" + s[cb:]

    for gone in ('rec-cx-take', 'rec-cx-tip', 'rec-cx-drop', 'take.', 'take)'):
        assert gone not in s, path + ': ' + gone + ' survives'
    assert 'rec-co-mark' in s, path + ': the card went with it'
    assert s.count('.rec-co {') == 1, path + ': the card rules were cut'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
