# -*- coding: utf-8 -*-
"""The details play out in the middle, then become the card.

The card was forming at the start of the reveal, so the company, the
paragraph and the tiles all arrived in a small box in the corner. They
now arrive centre screen at full size, where there is room to read them,
and only once the last fact has landed does the card draw itself and
take its place under the step.

The chrome fades rather than appearing: padding, border, background and
shadow all transition, so the thing that was content becomes an object
instead of blinking into one. The move itself is a snap -- flex
alignment does not animate -- which is why the chrome is what carries
the change.

A restore from refresh skips the wait and opens already settled. The
reveal is a first impression and there is no sense replaying it for
someone who has just seen it.
"""
import io
import sys

EDITS = [
    # it no longer starts in the corner
    ("""        function stage() {
          flow.classList.add('is-found');
          screen();""",
     """        function stage() {
          screen();"""),

    # it settles once everything has landed
    ("""        function rest() {
          busy = '';
          finished = true;
          at_step(0, true);""",
     """        function rest() {
          busy = '';
          finished = true;
          at_step(0, true);
          // let it be read at full size before it becomes a card
          window.setTimeout(function () {
            if (flow && !flow.hidden) flow.classList.add('is-found');
          }, 1600);"""),
]

OLD_CSS = """    .rec-found-card { padding:20px 22px 22px; border-radius:18px;
                      border:1px solid #ECE7F9; background:#FFFFFF;
                      box-shadow:0 2px 18px rgba(18,22,32,.05); }"""

NEW_CSS = """    /* content first; the card draws itself once the facts have landed */
    .rec-found-card { padding:0; border-radius:18px;
                      border:1px solid transparent; background:transparent;
                      box-shadow:0 2px 18px rgba(18,22,32,0);
                      transition:padding .34s ease, background .34s ease,
                                 border-color .34s ease, box-shadow .34s ease; }
    .rec-flow.is-found .rec-found-card { padding:20px 22px 22px;
                                         border-color:#ECE7F9;
                                         background:#FFFFFF;
                                         box-shadow:0 2px 18px
                                                    rgba(18,22,32,.05); }
    .rec-flow.is-found .rec-found-col { width:100%; }
    @media (prefers-reduced-motion: reduce) {
      .rec-found-card { transition:none; }
    }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert s.count(OLD_CSS) == 1, (path, 'card css', s.count(OLD_CSS))
    s = s.replace(OLD_CSS, NEW_CSS, 1)
    js = s[s.rindex('<script>'):]
    # the restore still opens settled
    assert js.count("flow.classList.add('is-found')") == 2, \
        path + ': the settle or the restore is missing'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
