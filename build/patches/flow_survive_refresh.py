# -*- coding: utf-8 -*-
"""A refresh keeps the company it found.

Reloading threw the whole flow away and put the reader back on the
marketing page, losing a lookup they had just waited through. The found
screen now survives: it is kept in sessionStorage when the details land
and put back on the next load.

Closing is still closing. The record is cleared by close(), so the x,
Escape and the skip all mean the same thing they did, and a new tab
starts clean because sessionStorage does not travel.

What gets kept is the rendered screen rather than the data, so the
restore cannot drift from what was on screen and nothing is fetched
again -- the reader has already seen these words and should not wait for
them twice. Everything in it was escaped when it was built.
"""
import io
import sys

KEY = "'wm-flow'"

EDITS = [
    # remember the finished screen
    ("""        function rest() {
          busy = '';
          finished = true;
          at_step(0, true);""",
     """        function rest() {
          busy = '';
          finished = true;
          at_step(0, true);
          window.setTimeout(function () {
            try {
              window.sessionStorage.setItem(@KEY@, JSON.stringify({
                role: brief.role, website: brief.website,
                html: card.innerHTML
              }));
            } catch (e) {}
          }, 0);""".replace('@KEY@', KEY)),

    # closing means closing
    ("""    function close() {
      if (!flow || flow.hidden) return;""",
     """    function close() {
      try { window.sessionStorage.removeItem(@KEY@); } catch (e) {}
      if (!flow || flow.hidden) return;""".replace('@KEY@', KEY)),

    # and put it back on the next load
    ("""    form.addEventListener('submit', function (e) {
      e.preventDefault();
      open();
    });""",
     """    form.addEventListener('submit', function (e) {
      e.preventDefault();
      open();
    });

    // a reload should not cost someone the lookup they just waited for
    (function () {
      var kept;
      try { kept = window.sessionStorage.getItem(@KEY@); } catch (e) { return; }
      if (!kept) return;
      var was;
      try { was = JSON.parse(kept); } catch (e) { return; }
      if (!was || !was.html) return;

      brief.role = was.role || '';
      brief.website = was.website || '';
      at = 0;
      if (!flow) build();
      flow.classList.remove('is-out');
      flow.hidden = false;
      at_step(0, true);
      flow.querySelector('.rec-flow-bar span')
          .style.setProperty('--at', '100%');
      var card = flow.querySelector('.rec-flow-card');
      card.innerHTML = was.html;
      // the only control the found screen can carry
      var again = card.querySelector('.rec-flow-back');
      if (again) again.addEventListener('click', function () { draw(); });
    }());""".replace('@KEY@', KEY)),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'wm-flow' not in s, path + ': already survives'
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    js = s[s.rindex('<script>'):]
    assert js.count("sessionStorage.setItem('wm-flow'") == 1, path + ': no save'
    assert js.count("sessionStorage.removeItem('wm-flow'") == 1, path + ': no clear'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
