# -*- coding: utf-8 -*-
"""Clicking the other chip switches to it instead of closing.

The toggle asked one question -- "is anything tucked away?" -- which was
enough when there was one chip and wrong as soon as there were two. With
the board open, pressing the company chip read the flow as "not tucked"
and closed it, so the other chip's screen never appeared and the press
looked broken.

It tracks which chip is open now. Pressing the open one closes it;
pressing the other switches straight to it.
"""
import io
import sys

EDITS = [
    ("""    // the screens the chips put back, one per step
    var kept = {};

    function show_details(i, on) {""",
     """    // the screens the chips put back, one per step
    var kept = {};
    var open_i = null;        // which chip is showing, if any

    function show_details(i, on) {"""),

    ("""      var face = flow.querySelector('.rec-flow-card');
      flow.classList.toggle('is-found', !on);
      face.innerHTML = on ? kept[i] : '';""",
     """      var face = flow.querySelector('.rec-flow-card');
      open_i = on ? i : null;
      flow.classList.toggle('is-found', !on);
      face.innerHTML = on ? kept[i] : '';"""),

    ("""      slot.querySelector('.rec-done-card').addEventListener('click',
        function () {
          show_details(i, flow.classList.contains('is-found'));
        });""",
     """      slot.querySelector('.rec-done-card').addEventListener('click',
        function () {
          // the open one closes; any other one takes its place
          show_details(i, open_i !== i);
        });"""),

    # tucking a step away is also "nothing is open"
    ("""            flow.classList.add('is-found');
            put_mini(0, who, logo, card.innerHTML);""",
     """            flow.classList.add('is-found');
            open_i = null;
            put_mini(0, who, logo, card.innerHTML);"""),

    ("""            flow.classList.add('is-found');
            put_mini(1, 'Job board', found.logo, card.innerHTML);""",
     """            flow.classList.add('is-found');
            open_i = null;
            put_mini(1, 'Job board', found.logo, card.innerHTML);"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'open_i' not in s, path + ': already switches'
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
