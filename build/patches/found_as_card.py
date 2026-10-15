# -*- coding: utf-8 -*-
"""The details become one card, under the step that found them.

Three things, which are really one:

* everything the lookup produced goes inside a single card, so it reads
  as the result of step one rather than as four loose blocks;
* the card moves to the top left, under "Company details", instead of
  floating in the middle of the screen with no relationship to the step
  that produced it;
* and step one takes a tick, because it is finished.

The company row loses its own border and background on the way in. A
card inside a card said "two objects" when the whole point of this
change is that it is one.

Only the found screen moves: the question screens keep their centred
layout, so the flow still opens on a centred field and only settles to
the corner once there is something to settle around.
"""
import io
import sys

EDITS = [
    # one card around everything the lookup produced
    ("""            '<h2 class="rec-flow-q is-alone">' +
              (blank ? 'Nothing on that domain' : 'Found your company') +
            '</h2>' +
            '<div class="rec-flow-found">' +""",
     """            '<h2 class="rec-flow-q is-alone">' +
              (blank ? 'Nothing on that domain' : 'Found your company') +
            '</h2>' +
            '<div class="rec-found-card">' +
            '<div class="rec-flow-found">' +"""),

    ("""              : '') +
            '</div>';

          var again = card.querySelector('.rec-flow-back');""",
     """              : '') +
            '</div>' +
            '</div>';

          var again = card.querySelector('.rec-flow-back');"""),

    # the found screen sits in the corner; the questions stay centred
    ("""        function stage() {
          screen();""",
     """        function stage() {
          flow.classList.add('is-found');
          screen();"""),

    ("""      if (at >= STEPS.length) { close(); return; }
      at_step(0, false);""",
     """      if (at >= STEPS.length) { close(); return; }
      flow.classList.remove('is-found');
      at_step(0, false);"""),

    # a finished step says so
    ("""      var all = flow.querySelectorAll('.rec-step');
      for (var k = 0; k < all.length; k++) {
        all[k].classList.toggle('is-on', k === i && !done);
        all[k].classList.toggle('is-done', k < i || (k === i && done));
      }""",
     """      var all = flow.querySelectorAll('.rec-step');
      for (var k = 0; k < all.length; k++) {
        var over = k < i || (k === i && done);
        all[k].classList.toggle('is-on', k === i && !done);
        all[k].classList.toggle('is-done', over);
        var mark = all[k].querySelector('i');
        mark.textContent = over ? '\\u2713' : String(k + 1);
      }"""),

    # and the restored screen is a found screen too
    ("""      at_step(0, true);
      flow.querySelector('.rec-flow-bar span')
          .style.setProperty('--at', '100%');
      var card = flow.querySelector('.rec-flow-card');""",
     """      at_step(0, true);
      flow.classList.add('is-found');
      flow.querySelector('.rec-flow-bar span')
          .style.setProperty('--at', '100%');
      var card = flow.querySelector('.rec-flow-card');"""),
]

CSS = """    /* the lookup's result, as one card in the corner */
    .rec-flow.is-found .rec-flow-body { align-items:flex-start;
                                        justify-content:flex-start; }
    .rec-flow.is-found .rec-flow-card { width:min(470px, 100%); }
    .rec-found-card { padding:20px 22px 22px; border-radius:18px;
                      border:1px solid #ECE7F9; background:#FFFFFF;
                      box-shadow:0 2px 18px rgba(18,22,32,.05); }
    /* flattened: a card inside a card reads as two objects */
    .rec-found-card .rec-flow-found { width:100%; margin:0; padding:0;
                                      border:0; background:none; }
    .rec-found-card .rec-found-about { margin-top:14px; }
    .rec-found-card .rec-found-facts { margin-top:16px; }
"""

CSS_ANCHOR = "    /* the found screen shares one left edge */"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-found-card' not in s, path + ': already a card'
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS + CSS_ANCHOR, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
