# -*- coding: utf-8 -*-
"""The Account step opens its own screen again.

Steps one and two leave a chip behind, so their screens can always be
reopened. Step three does not -- it is the end and stays on screen --
which was fine until a chip was pressed: the account screen went away
and nothing could bring it back.

Its own row in the rail does that now. The row takes a pointer and a
hover once there is something behind it, and it toggles exactly as the
chips do: press it to open, press it again to put it away.

The button inside it had to move out of the closure that built it. A
reopened screen is re-injected HTML, so its listener is gone; the
handler now lives at the top of the flow and show_details re-attaches
it to whatever it has just put back.
"""
import io
import sys

EDITS = [
    # one handler, reachable from both the first render and every reopen
    ("""    function show_details(i, on) {
      if (on && !kept[i]) return;
      var face = flow.querySelector('.rec-flow-card');""",
     """    // the account screen's one action, defined where a reopen can find it
    function open_account() {
      close();
      var login = document.querySelector('.rec-head .rec-login');
      if (login) window.setTimeout(function () { login.click(); }, 200);
    }

    function show_details(i, on) {
      if (on && !kept[i]) return;
      var face = flow.querySelector('.rec-flow-card');"""),

    ("""      open_i = on ? i : null;
      flow.classList.toggle('is-found', !on);
      face.innerHTML = on ? kept[i] : '';""",
     """      open_i = on ? i : null;
      flow.classList.toggle('is-found', !on);
      face.innerHTML = on ? kept[i] : '';
      // re-injected HTML has no listeners of its own
      var back = face.querySelector('.rec-ready-go');
      if (back) back.addEventListener('click', open_account);"""),

    # the step row becomes the way back to a screen with no chip
    ("""        function ready() {
          at_step(2, true);""",
     """        function ready() {
          at_step(2, true);
          make_step_open(2);"""),

    ("""          var go = card.querySelector('.rec-ready-go');
          if (go) go.addEventListener('click', function () {
            close();
            var login = document.querySelector('.rec-head .rec-login');
            if (login) window.setTimeout(function () { login.click(); }, 200);
          });""",
     """          kept[2] = card.innerHTML;
          var go = card.querySelector('.rec-ready-go');
          if (go) go.addEventListener('click', open_account);"""),
]

HELPER_JS = """    // a step with a screen behind it and no chip of its own
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

"""

CSS = """    .rec-step.is-link .rec-step-row { cursor:pointer; }
    .rec-step.is-link .rec-step-row:hover b { color:#1A1430;
                                              text-decoration:underline;
                                              text-underline-offset:3px; }
"""

CSS_ANCHOR = "    .rec-done-slot { display:block; max-width:100%; }"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'make_step_open' not in s, path + ': already clickable'

    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    mark = "    // what a finished step leaves behind, under that step\n"
    assert s.count(mark) == 1, (path, 'helper anchor', s.count(mark))
    s = s.replace(mark, HELPER_JS + mark, 1)

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS_ANCHOR + '\n' + CSS, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
