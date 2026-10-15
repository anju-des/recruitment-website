# -*- coding: utf-8 -*-
"""Step two: the job board, built from what step one found.

It starts itself once the company has tucked away, runs in the middle
with the same working panel, and settles into its own chip under its own
step.

What it builds is real, which is the only reason it can be shown: the
board's header is the logo and name fetched in step one, its location
line is the company's own, and the listing is the role that was typed
into the composer on the way in. Nothing is invented and nothing is
published -- it is a preview of a board, and the address under it is
shown as plain text rather than a link for that reason.

Two structural changes carry it:

* chips move inside their step's <li>, so each step owns the thing it
  produced and the rail keeps its order. The connector still bridges
  li to li, which is a fixed 28px whatever a step contains.
* the kept screens become a map keyed by step, and the toggle takes an
  index. One chip reopening one screen does not generalise to two.
"""
import io
import sys

EDITS = [
    # two steps again
    ("""          ['Company details']""",
     """          ['Company details', 'Job board']"""),

    # the row, so a chip can sit under the label inside the same step
    ("""                return '<li class="rec-step"><i>' + (i + 1) + '</i>' +
                  '<b>' + s + '</b></li>';""",
     """                return '<li class="rec-step">' +
                  '<span class="rec-step-row"><i>' + (i + 1) + '</i>' +
                  '<b>' + s + '</b></span></li>';"""),

    # screens are kept per step now
    ("""    // the screen the chip puts back
    var kept_html = '';

    function show_details(on) {
      // an older record can name a company without carrying its screen
      if (on && !kept_html) return;
      var face = flow.querySelector('.rec-flow-card');
      var chip = flow.querySelector('.rec-done-card');
      flow.classList.toggle('is-found', !on);
      face.innerHTML = on ? kept_html : '';
      if (chip) chip.setAttribute('aria-expanded', on ? 'true' : 'false');
    }""",
     """    // the screens the chips put back, one per step
    var kept = {};

    function show_details(i, on) {
      if (on && !kept[i]) return;
      var face = flow.querySelector('.rec-flow-card');
      flow.classList.toggle('is-found', !on);
      face.innerHTML = on ? kept[i] : '';
      var chips = flow.querySelectorAll('.rec-done-card');
      for (var k = 0; k < chips.length; k++) {
        chips[k].setAttribute('aria-expanded',
          (on && Number(chips[k].getAttribute('data-for')) === i)
            ? 'true' : 'false');
      }
    }"""),

    # one chip builder for both steps
    ("""    // what a finished lookup leaves behind in the rail
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
            '<path d="M9 6l6 6-6 6"/></svg>' +
        '</button>';
      slot.querySelector('.rec-done-card').addEventListener('click',
        function () {
          show_details(flow.classList.contains('is-found'));
        });
    }""",
     """    // what a finished step leaves behind, under that step
    function put_mini(i, label, logo, html) {
      kept[i] = html;
      var step = flow.querySelectorAll('.rec-step')[i];
      if (!step) return;
      var slot = step.querySelector('.rec-done-slot');
      if (!slot) {
        slot = document.createElement('span');
        slot.className = 'rec-done-slot';
        step.appendChild(slot);
      }
      slot.innerHTML =
        '<button type="button" class="rec-done-card" data-for="' + i +
          '" aria-expanded="false">' +
          '<span class="rec-done-mark">' +
            (logo ? '<img src="' + esc(logo) + '" alt="">'
                  : esc(String(label || '?').charAt(0))) +
          '</span><b>' + esc(label) + '</b>' +
          '<svg class="rec-done-go" viewBox="0 0 24 24" fill="none" ' +
            'stroke="currentColor" stroke-width="2.2" stroke-linecap="round" ' +
            'stroke-linejoin="round" aria-hidden="true">' +
            '<path d="M9 6l6 6-6 6"/></svg>' +
        '</button>';
      slot.querySelector('.rec-done-card').addEventListener('click',
        function () {
          show_details(i, flow.classList.contains('is-found'));
        });
    }"""),

    # step one tucks away, then step two starts itself
    ("""            kept_html = card.innerHTML;
            flow.classList.add('is-found');
            put_mini(who, logo);
            card.innerHTML = '';""",
     """            found = { who: who, logo: logo, based: vals.Based || '' };
            flow.classList.add('is-found');
            put_mini(0, who, logo, card.innerHTML);
            card.innerHTML = '';
            window.setTimeout(board, 700);"""),

    # the restore puts the company chip back the same way
    ("""      flow.querySelector('.rec-flow-card').innerHTML = '';
      kept_html = was.html || '';
      put_mini(was.who, was.logo);""",
     """      flow.querySelector('.rec-flow-card').innerHTML = '';
      put_mini(0, was.who, was.logo, was.html || '');"""),
]

BOARD_JS = """      // Step two. It builds a board out of step one's company and the
      // role that was typed on the way in -- nothing invented, nothing
      // published, which is why the address below it is text and not a
      // link.
      function board() {
        if (!found.who) return;
        step_busy(1);

        var title = (brief.role || '').split(',')[0].trim() ||
                    'Your first role';
        var jobs = [
          'taking the Wisemonk logo and name',
          'writing up ' + title,
          'laying out the board'
        ];
        jobs[0] = 'taking the ' + found.who + ' logo and name';

        var ran = [];
        var now = 0;

        function panel() {
          card.innerHTML =
            '<h2 class="rec-flow-q is-alone">Building your job board</h2>' +
            '<div class="rec-work" role="status" aria-live="polite">' +
              '<p class="rec-work-head"><span class="rec-work-dot"></span>' +
                'Mira is working on step ' + Math.min(now + 1, jobs.length) +
                ' of ' + jobs.length + '</p>' +
              ran.map(function (r) {
                return '<p class="rec-work-line is-done"><i>\\u2713</i>' +
                  '<span>' + esc(r) + '</span></p>';
              }).join('') +
              (now < jobs.length
                ? '<p class="rec-work-line is-now"><i>\\u203a</i><span>' +
                  esc(jobs[now]) + '\\u2026</span><b></b></p>'
                : '') +
            '</div>';
        }

        function step(then) {
          ran.push(jobs[now]);
          now++;
          panel();
          window.setTimeout(then, 620);
        }

        function made() {
          card.innerHTML =
            '<div class="rec-found-col">' +
              '<h2 class="rec-flow-q is-alone">Your job board</h2>' +
              '<div class="rec-found-card">' +
                '<div class="rec-board-head">' +
                  '<span class="rec-flow-found-mark">' +
                    (found.logo ? '<img src="' + esc(found.logo) + '" alt="">'
                                : esc(found.who.charAt(0))) +
                  '</span>' +
                  '<span class="rec-flow-found-say">' +
                    '<b>' + esc(found.who) + ' careers</b>' +
                    '<i>' + esc(found.who.toLowerCase().replace(/[^a-z0-9]/g,
                      '')) + '.mira.jobs</i></span>' +
                '</div>' +
                '<div class="rec-board-role">' +
                  '<b>' + esc(title) + '</b>' +
                  (found.based ? '<i>' + esc(found.based) + '</i>' : '') +
                '</div>' +
                '<p class="rec-board-note">A preview. The board goes live ' +
                  'with your account.</p>' +
              '</div>' +
            '</div>';
          window.setTimeout(function () {
            if (!flow || flow.hidden) return;
            at_step(1, true);
            flow.classList.add('is-found');
            put_mini(1, 'Job board', '', card.innerHTML);
            card.innerHTML = '';
          }, 2000);
        }

        panel();
        window.setTimeout(function () {
          step(function () { step(function () { step(made); }); });
        }, 500);
      }

"""

CSS = """    .rec-step { flex-direction:column; align-items:flex-start; }
    .rec-step-row { display:flex; align-items:center; gap:10px; }
    .rec-done-slot { display:block; max-width:100%; }

    /* step two's board, built from step one */
    .rec-board-head { display:flex; align-items:center; gap:13px; }
    .rec-board-role { margin-top:18px; padding:14px 16px; border-radius:12px;
                      background:#F6F4FD; display:flex;
                      flex-direction:column; gap:3px; }
    .rec-board-role b { font-size:14.5px; font-weight:600; color:#1A1430; }
    .rec-board-role i { font-style:normal; font-size:12.5px;
                        color:#8A82A8; }
    .rec-board-note { margin:14px 0 0; font-size:12.5px; color:#8A82A8; }
"""

CSS_ANCHOR = "    .rec-done-card { display:flex;"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-board-role' not in s, path + ': step two already there'

    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    # found carries step one's result into step two
    mark = "      function onward() { at++; draw(); }\n"
    assert s.count(mark) == 1, (path, 'onward', s.count(mark))
    s = s.replace(mark, mark + "\n      var found = {};\n" + BOARD_JS, 1)

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS + CSS_ANCHOR, 1)

    js = s[s.rindex('<script>'):]
    assert 'kept_html' not in js, path + ': the single kept screen survives'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
