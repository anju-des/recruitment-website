# -*- coding: utf-8 -*-
"""A saved flow does not outlive the version that wrote it.

The record keeps each finished screen as HTML, so a visitor who had the
flow open before a deploy comes back to screens the old build wrote:
yesterday's button, yesterday's copy, and -- where the new CSS has
dropped a class the old markup still carries -- an unstyled control. It
looks exactly like a change that did not ship.

So the record is stamped with the build that wrote it, and a record from
any other build is dropped rather than replayed. The stamp is a hash of
this script's own text, taken once at load: change anything about how
these screens are built and the stamp changes by itself, which a number
someone has to remember to raise would not.

Over-eager by design. An unrelated edit to this script also clears the
record, and the cost of that is a visitor retyping their company -- far
cheaper than being shown a screen that no longer exists.
"""
import io
import sys

STAMP = """  // the build that wrote a record, so a record from another one can be
  // recognised and dropped. Taken from this script's own text: anything
  // that changes how a screen is built changes this with it.
  var FLOW_V = (function () {
    var el = document.currentScript ||
             document.scripts[document.scripts.length - 1];
    var s = (el && el.textContent) || '';
    var h = 5381;
    var i = s.length;
    while (i) { h = (h * 33 ^ s.charCodeAt(--i)) >>> 0; }
    return h.toString(36);
  }());

"""

ANCHOR = """  // Send opens the brief: the role in a sentence is the start of it, and the
  // three things Mira still needs come one screen at a time.
  (function () {"""

EDITS = [
    ("""        window.sessionStorage.setItem('wm-flow', JSON.stringify({
          role: brief.role, website: brief.website,""",
     """        window.sessionStorage.setItem('wm-flow', JSON.stringify({
          v: FLOW_V,
          role: brief.role, website: brief.website,"""),

    ("""      var screens = (was && was.screens) || {};
      if (!was || !was.who || !screens[0]) {""",
     """      var screens = (was && was.screens) || {};
      // a record from another build holds that build's markup
      if (!was || was.v !== FLOW_V || !was.who || !screens[0]) {"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'FLOW_V' not in s, path + ': already stamped'
    assert s.count(ANCHOR) == 1, (path, 'anchor', s.count(ANCHOR))
    s = s.replace(ANCHOR, STAMP + ANCHOR, 1)
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
