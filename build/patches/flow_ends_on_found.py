# -*- coding: utf-8 -*-
"""The flow ends on what it found.

"The role is live." goes, and nothing replaces it: the profile is the
payoff, so it stays on screen until it is dismissed rather than sliding
away on a timer to a screen that no longer exists. The bar fills when the
details land, and the close in the header is the way out.

The two remaining done() calls become close(). Only the skip can reach
them now -- no website means nothing to show -- so skipping shuts the
flow instead of ending on a tick for work nobody did.
"""
import io
import sys

EDITS = [
    # the details are the end: fill the bar, drop the hand-off
    ("""          window.setTimeout(function () {
            if (flow && !flow.hidden) onward();
          }, facts.length ? 3200 : 2200);""",
     """          flow.querySelector('.rec-flow-bar span')
              .style.setProperty('--at', '100%');"""),

    ("""      if (at >= STEPS.length) { done(); return; }
      card.innerHTML = ask(STEPS[at]);""",
     """      if (at >= STEPS.length) { close(); return; }
      card.innerHTML = ask(STEPS[at]);"""),

    ("""        if (at >= STEPS.length) { done(); return; }""",
     """        if (at >= STEPS.length) { close(); return; }"""),
]

CUT = ("    function done() {", "    function wire(")


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    a = s.index(CUT[0])
    b = s.index(CUT[1], a)
    s = s[:a] + s[b:]

    js = s[s.rindex('<script>'):]
    for gone in ('function done(', 'The role is live', 'rec-flow-tick',
                 'walk-through of the flow'):
        assert gone not in js, path + ': ' + gone + ' survives in the script'
    assert 'function close(' in js, path + ': close went with it'
    assert 'function look(' in js, path + ': the lookup went with it'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
