# -*- coding: utf-8 -*-
"""Step one spins while it is working.

The three states it can be in now say themselves: 1 before it starts,
a spinner while the lookup runs, a tick when the details land.

The spinner is drawn over the number rather than replacing it, so the
circle never changes size and the row never shifts. at_step clears the
busy state on every call, which means the tick and the number both put
it away without having to know about it.

It reuses the rotation the old inline spinner left behind in the
stylesheet, and stands still under prefers-reduced-motion -- the filled
circle still reads as "this one is live".
"""
import io
import sys

EDITS = [
    ("""      var all = flow.querySelectorAll('.rec-step');
      for (var k = 0; k < all.length; k++) {
        var over = k < i || (k === i && done);""",
     """      var all = flow.querySelectorAll('.rec-step');
      for (var k = 0; k < all.length; k++) {
        var over = k < i || (k === i && done);
        all[k].classList.remove('is-busy');"""),

    ("""    function open() {
      brief.role = field.value.trim();""",
     """    // the step is working, not merely current
    function step_busy(i) {
      at_step(i, false);
      var one = flow.querySelectorAll('.rec-step')[i];
      if (one) one.classList.add('is-busy');
    }

    function open() {
      brief.role = field.value.trim();"""),

    ("""      function look() {
        var site = brief.website;""",
     """      function look() {
        step_busy(0);
        var site = brief.website;"""),
]

CSS = """    .rec-step.is-busy i { background:#7C5CF6; color:transparent;
                          position:relative; }
    .rec-step.is-busy i::after { content:""; position:absolute; inset:3px;
                                 border-radius:50%;
                                 border:2px solid rgba(255,255,255,.4);
                                 border-top-color:#FFFFFF;
                                 animation:rec-flow-turn .7s linear infinite; }
    @media (prefers-reduced-motion: reduce) {
      .rec-step.is-busy i::after { animation:none; }
    }
"""

CSS_ANCHOR = "    .rec-step.is-done { color:#6B6392; }"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'is-busy' not in s, path + ': already spins'
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS + CSS_ANCHOR, 1)
    # the rotation it borrows has to still be there
    assert '@keyframes rec-flow-turn' in s, path + ': no rotation to use'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
