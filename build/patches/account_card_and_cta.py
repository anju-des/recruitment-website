# -*- coding: utf-8 -*-
"""The Account step gets a card too, and the button says what it does.

Two steps left a card behind and the third left a clickable row, which
is a second way of saying the same thing and looks like neither. All
three steps file a card now, and the rail is one list of three.

Its card is filed with the screen still open, so the card says so from
the moment it appears -- which it could not while "which card is open"
was read off the flow's own class. Every card lit up whenever any one of
them was. The card's own aria-expanded already carried the answer, step
by step, so the active look reads from that instead.

make_step_open existed for a step with no card. There is no such step
now, so it goes, with the row-link styling it brought.

And the button: "Open your account" was the wrong half of what this
screen does, which is why a sign-in line had to be bolted under it. It
says "Sign in to your account", and the screen it opens -- "Sign in or
create your account" -- is the one that handles both. The bolted-on
line and its styling go with it.
"""
import io
import sys

EDITS = [
    # the button, and the line that existed because the button was wrong
    ("""                '<button type="button" class="rec-flow-next rec-ready-go" ' +
                  'data-login="1">Open your account</button>' +
                '<p class="rec-ready-in">Already with Mira? ' +
                  '<button type="button" class="rec-ready-signin" ' +
                    'data-login="1">Sign in</button></p>' +""",
     """                '<button type="button" class="rec-flow-next rec-ready-go" ' +
                  'data-login="1">Sign in to your account</button>' +"""),

    # the third card, filed with its screen still showing
    ("""          kept[2] = card.innerHTML;
          remember();""",
     """          put_mini(2, 'Account', 'ready to open', found.logo,
                   card.innerHTML);
          // it is filed open: the screen it holds is the one on screen
          open_i = 2;
          var mine = flow.querySelector('.rec-done-card[data-for="2"]');
          if (mine) mine.setAttribute('aria-expanded', 'true');
          remember();"""),

    ("""        function ready() {
          at_step(2, true);
          make_step_open(2);""",
     """        function ready() {
          at_step(2, true);"""),

    ("""      if (screens[2]) { kept[2] = screens[2]; make_step_open(2); last = 2; }""",
     """      if (screens[2]) { put_mini(2, 'Account', 'ready to open',
                                 was.logo, screens[2]);
                        last = 2; }"""),

    # a step with no card of its own: there is no longer one
    ("""    // a step with a screen behind it and no chip of its own
    function make_step_open(i) {
      var step = flow.querySelectorAll('.rec-step')[i];
      if (!step) return;
      var row = step.querySelector('.rec-step-row');
      if (!row || row.getAttribute('data-open') === '1') return;
      row.setAttribute('data-open', '1');
      step.classList.add('is-link');
      row.addEventListener('click', function () {
        show_details(i, open_i !== i);
      });
    }

""", ""),
]

CSS_EDITS = [
    # the open card, not every card while one is open
    ("""    /* the details are open: the chip is the thing holding them there */
    .rec-flow:not(.is-found) .rec-done-card { border-color:#BCAEF0; }""",
     """    /* this card is the one holding the details open */
    .rec-done-card[aria-expanded="true"] { border-color:#BCAEF0; }"""),

    ("""    .rec-flow:not(.is-found) .rec-done-go { transform:rotate(90deg);
                                            color:#6B4BE8; }""",
     """    .rec-done-card[aria-expanded="true"] .rec-done-go {
      transform:rotate(90deg); color:#6B4BE8; }"""),

    ("""    .rec-step.is-link .rec-step-row { cursor:pointer; }
    .rec-step.is-link .rec-step-row:hover b { color:#1A1430;
                                              text-decoration:underline;
                                              text-underline-offset:3px; }
""", ""),

    ("""    .rec-ready-in { margin:14px 0 0; text-align:center; font-size:13.5px;
                    color:#8A82A8; }
    .rec-ready-signin { border:0; padding:0 2px; background:none;
                        font:inherit; font-size:13.5px; font-weight:600;
                        color:#6B4BE8; cursor:pointer;
                        text-decoration:underline;
                        text-underline-offset:3px; }
    .rec-ready-signin:hover { color:#4A32C0; }
""", ""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS + CSS_EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    for gone in ('make_step_open', 'is-link', 'rec-ready-in',
                 'rec-ready-signin', 'kept[2]'):
        assert gone not in s, (path, gone + ' survives')
    js = s[s.rindex('<script>'):]
    # the definition and six places that call it: three steps, three
    # the restore puts back
    assert js.count('put_mini(') == 7, (path, 'call sites',
                                        js.count('put_mini('))
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
