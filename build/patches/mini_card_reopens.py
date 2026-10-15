# -*- coding: utf-8 -*-
"""The chip opens the details again.

It becomes a button rather than a label, and toggles: the details come
back centre screen exactly as they were read the first time, and go away
again on a second press.

Nothing is fetched to do it. The rendered screen is kept when the chip
is made and put straight back, so what reopens is the thing that was
seen, not a second attempt at it.

Which means the refresh record carries the rendered screen again. It did
before, was dropped when the chip replaced it, and comes back now for a
different reason: not to land on, but to have something to reopen. A
restore lands on the chip and can open it just the same.

The open state is readable in three ways, which is right for a toggle
with no label: aria-expanded, a brighter border, and the details
themselves.
"""
import io
import sys

EDITS = [
    # keep what the chip will reopen
    ("""    // what a finished lookup leaves behind in the rail
    function put_mini(who, logo) {
      var rail = flow.querySelector('.rec-steps');
      var mini = rail.querySelector('.rec-done-card');
      if (!mini) {
        mini = document.createElement('li');
        mini.className = 'rec-done-card';
        rail.appendChild(mini);
      }
      mini.innerHTML =
        '<span class="rec-done-mark">' +
          (logo ? '<img src="' + esc(logo) + '" alt="">'
                : esc(String(who || '?').charAt(0))) +
        '</span><b>' + esc(who) + '</b>';
    }""",
     """    // the screen the chip puts back
    var kept_html = '';

    function show_details(on) {
      var face = flow.querySelector('.rec-flow-card');
      var chip = flow.querySelector('.rec-done-card');
      flow.classList.toggle('is-found', !on);
      face.innerHTML = on ? kept_html : '';
      if (chip) chip.setAttribute('aria-expanded', on ? 'true' : 'false');
    }

    // what a finished lookup leaves behind in the rail
    function put_mini(who, logo) {
      var rail = flow.querySelector('.rec-steps');
      var slot = rail.querySelector('.rec-done-slot');
      if (!slot) {
        slot = document.createElement('li');
        slot.className = 'rec-done-slot';
        rail.appendChild(slot);
      }
      slot.innerHTML =
        '<button type="button" class="rec-done-card" aria-expanded="false">' +
          '<span class="rec-done-mark">' +
            (logo ? '<img src="' + esc(logo) + '" alt="">'
                  : esc(String(who || '?').charAt(0))) +
          '</span><b>' + esc(who) + '</b>' +
          '<svg class="rec-done-go" viewBox="0 0 24 24" fill="none" ' +
            'stroke="currentColor" stroke-width="2.2" stroke-linecap="round" ' +
            'stroke-linejoin="round" aria-hidden="true">' +
            '<path d="M6 9.5l6 6 6-6"/></svg>' +
        '</button>';
      slot.querySelector('.rec-done-card').addEventListener('click',
        function () {
          show_details(flow.classList.contains('is-found'));
        });
    }"""),

    # the record carries the screen again, to reopen rather than to land on
    ("""              window.sessionStorage.setItem('wm-flow', JSON.stringify({
                role: brief.role, website: brief.website,
                who: who, logo: logo
              }));""",
     """              window.sessionStorage.setItem('wm-flow', JSON.stringify({
                role: brief.role, website: brief.website,
                who: who, logo: logo, html: card.innerHTML
              }));"""),

    ("""            flow.classList.add('is-found');
            put_mini(who, logo);
            card.innerHTML = '';""",
     """            kept_html = card.innerHTML;
            flow.classList.add('is-found');
            put_mini(who, logo);
            card.innerHTML = '';"""),

    ("""      flow.querySelector('.rec-flow-card').innerHTML = '';
      put_mini(was.who, was.logo);""",
     """      flow.querySelector('.rec-flow-card').innerHTML = '';
      kept_html = was.html || '';
      put_mini(was.who, was.logo);"""),
]

OLD_CSS = """    .rec-done-card { display:flex; align-items:center; gap:9px;
                     margin:2px 0 0 30px; padding:9px 12px; max-width:100%;
                     box-sizing:border-box; border-radius:12px;
                     border:1px solid #ECE7F9; background:#FFFFFF;
                     box-shadow:0 1px 8px rgba(18,22,32,.05);
                     animation:rec-mini-in .32s ease both; }"""

NEW_CSS = """    .rec-done-slot { list-style:none; max-width:100%; }
    .rec-done-card { display:flex; align-items:center; gap:9px; font:inherit;
                     margin:2px 0 0 30px; padding:9px 12px; max-width:100%;
                     box-sizing:border-box; border-radius:12px; cursor:pointer;
                     border:1px solid #ECE7F9; background:#FFFFFF;
                     text-align:left;
                     box-shadow:0 1px 8px rgba(18,22,32,.05);
                     transition:border-color .15s, box-shadow .15s;
                     animation:rec-mini-in .32s ease both; }
    .rec-done-card:hover { border-color:#BCAEF0;
                           box-shadow:0 2px 12px rgba(18,22,32,.08); }
    .rec-done-card:focus-visible { outline:2px solid #7C5CF6;
                                   outline-offset:2px; }
    /* the details are open: the chip is the thing holding them there */
    .rec-flow:not(.is-found) .rec-done-card { border-color:#BCAEF0; }
    .rec-done-go { flex:none; width:14px; height:14px; margin-left:auto;
                   color:#A49CC0; transition:transform .2s ease; }
    .rec-flow:not(.is-found) .rec-done-go { transform:rotate(180deg);
                                            color:#6B4BE8; }
    @media (prefers-reduced-motion: reduce) {
      .rec-done-go { transition:none; }
    }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-done-slot' not in s, path + ': already a button'
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert s.count(OLD_CSS) == 1, (path, 'chip css', s.count(OLD_CSS))
    s = s.replace(OLD_CSS, NEW_CSS, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
