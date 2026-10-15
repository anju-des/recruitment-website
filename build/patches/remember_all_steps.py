# -*- coding: utf-8 -*-
"""A refresh brings back all three steps, not just the first.

The record was written once, by step one, back when step one was the
whole flow. Two steps were added after it and nothing taught it about
them -- so a reload restored the company chip and left the rail
stranded: one step done, two plain, and no way to reach either, because
the thing that starts them is finishing the step before.

It now keeps every screen a step has produced, written at each of the
three moments a step finishes, and the restore puts them all back: both
chips, the Account row made clickable again, and every step ticked.

A record from the older build has an html field and no screens, so the
guard rejects it and clears it rather than restoring half a flow.
"""
import io
import sys

EDITS = [
    # the company survives outside wire() so the record can be written anywhere
    ("""    // the screens the chips put back, one per step
    var kept = {};""",
     """    // the screens the chips put back, one per step
    var kept = {};
    var company = {};         // step one's result, for the record"""),

    ("""    // the account screen's one action, defined where a reopen can find it""",
     """    // written at each of the three moments a step finishes
    function remember() {
      try {
        window.sessionStorage.setItem('wm-flow', JSON.stringify({
          role: brief.role, website: brief.website,
          who: company.who, logo: company.logo, based: company.based || '',
          screens: kept
        }));
      } catch (e) {}
    }

    // the account screen's one action, defined where a reopen can find it"""),

    # step one: one record write, after the chip exists
    ("""            found = { who: who, logo: logo, based: vals.Based || '' };
            flow.classList.add('is-found');
            open_i = null;
            put_mini(0, who, logo, card.innerHTML);
            card.innerHTML = '';
            step_busy(1);          // no dead "2" in the gap
            window.setTimeout(board, 700);""",
     """            found = { who: who, logo: logo, based: vals.Based || '' };
            company = found;
            flow.classList.add('is-found');
            open_i = null;
            put_mini(0, who, logo, card.innerHTML);
            remember();
            card.innerHTML = '';
            step_busy(1);          // no dead "2" in the gap
            window.setTimeout(board, 700);"""),

    ("""          window.setTimeout(function () {
            try {
              window.sessionStorage.setItem('wm-flow', JSON.stringify({
                role: brief.role, website: brief.website,
                who: who, logo: logo, html: card.innerHTML
              }));
            } catch (e) {}
          }, 0);
""", ""),

    # step two
    ("""            put_mini(1, 'Job board', found.logo, card.innerHTML);
            card.innerHTML = '';""",
     """            put_mini(1, 'Job board', found.logo, card.innerHTML);
            remember();
            card.innerHTML = '';"""),

    # step three
    ("""          kept[2] = card.innerHTML;
          var go = card.querySelector('.rec-ready-go');""",
     """          kept[2] = card.innerHTML;
          remember();
          var go = card.querySelector('.rec-ready-go');"""),

    # and the restore rebuilds whatever was finished
    ("""      // a record from a build that did not keep the screen cannot be
      // reopened, so it is not worth restoring
      if (!was || !was.who || !was.html) {
        try { window.sessionStorage.removeItem('wm-flow'); } catch (e) {}
        return;
      }""",
     """      // a record without the screens is from an older build and would
      // restore half a flow, so it goes rather than confuses
      var screens = (was && was.screens) || {};
      if (!was || !was.who || !screens[0]) {
        try { window.sessionStorage.removeItem('wm-flow'); } catch (e) {}
        return;
      }"""),

    ("""      flow.querySelector('.rec-flow-card').innerHTML = '';
      put_mini(0, was.who, was.logo, was.html || '');""",
     """      flow.querySelector('.rec-flow-card').innerHTML = '';
      company = { who: was.who, logo: was.logo, based: was.based || '' };
      put_mini(0, was.who, was.logo, screens[0]);
      var last = 0;
      if (screens[1]) { put_mini(1, 'Job board', was.logo, screens[1]);
                        last = 1; }
      if (screens[2]) { kept[2] = screens[2]; make_step_open(2); last = 2; }
      at_step(last, true);"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'function remember' not in s, path + ': already remembers'
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    js = s[s.rindex('<script>'):]
    assert js.count('remember();') == 3, path + ': not three writes'
    assert 'was.html' not in js, path + ': the old field survives'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
