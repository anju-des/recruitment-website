# -*- coding: utf-8 -*-
"""Step three: preparing the account, and the flow ends there.

It follows the same shape as the other two -- work in the middle, named
lines, a result -- but it does not tuck away. It is the end, and the end
is the only screen with something to ask for, so it stays.

Its lines name the three things actually assembled by the steps before
it: the workspace takes the company's name, the board its address, the
listing the role that was typed. Nothing new is fetched because nothing
new is needed; this step is the summary made actionable.

The button opens the sign-in screen the page already has rather than
inventing a second one. Nothing is created -- the subcopy says the
account is ready to open, not opened -- which is the honest shape for a
walkthrough whose last screen is a door.
"""
import io
import sys

EDITS = [
    ("""          ['Company details', 'Job board']""",
     """          ['Company details', 'Job board', 'Account']"""),

    # the board keeps its address for the summary
    ("""            found = { who: who, logo: logo, based: vals.Based || '' };""",
     """            found = { who: who, logo: logo, based: vals.Based || '' };"""),

    ("""            flow.classList.add('is-found');
            open_i = null;
            put_mini(1, 'Job board', found.logo, card.innerHTML);
            card.innerHTML = '';""",
     """            flow.classList.add('is-found');
            open_i = null;
            put_mini(1, 'Job board', found.logo, card.innerHTML);
            card.innerHTML = '';
            step_busy(2);
            window.setTimeout(account, 700);"""),
]

ACCOUNT_JS = """      // Step three. Nothing is fetched: it names what the first two steps
      // already made, and ends on the one screen with something to ask.
      function account() {
        if (!found.who) return;
        flow.classList.remove('is-found');
        open_i = null;
        step_busy(2);

        var title = (brief.role || '').split(',')[0].trim();
        var addr = found.who.toLowerCase().replace(/[^a-z0-9]/g, '') +
                   '.mira.jobs';
        var jobs = [
          'naming your workspace ' + found.who,
          'attaching ' + addr,
          title ? 'adding ' + title : 'leaving room for your first role'
        ];
        var ran = [];
        var now = 0;

        function panel() {
          card.innerHTML =
            '<h2 class="rec-flow-q is-alone">Preparing your account</h2>' +
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

        function ready() {
          at_step(2, true);
          flow.querySelector('.rec-flow-bar span')
              .style.setProperty('--at', '100%');
          card.innerHTML =
            '<div class="rec-found-col">' +
              '<h2 class="rec-flow-q">Your account is ready to open</h2>' +
              '<p class="rec-flow-hint">Everything above is set up and ' +
                'waiting. Open the account and Mira starts reading ' +
                'applications the day they land.</p>' +
              '<div class="rec-found-card">' +
                '<ul class="rec-ready">' +
                  '<li><i>Workspace</i><b>' + esc(found.who) + '</b></li>' +
                  '<li><i>Job board</i><b>' + esc(addr) + '</b></li>' +
                  (title
                    ? '<li><i>First role</i><b>' + esc(title) + '</b></li>'
                    : '') +
                '</ul>' +
                '<button type="button" class="rec-flow-next rec-ready-go">' +
                  'Open your account</button>' +
              '</div>' +
            '</div>';
          var go = card.querySelector('.rec-ready-go');
          if (go) go.addEventListener('click', function () {
            close();
            var login = document.querySelector('.rec-head .rec-login');
            if (login) window.setTimeout(function () { login.click(); }, 200);
          });
        }

        panel();
        window.setTimeout(function () {
          step(function () { step(function () { step(ready); }); });
        }, 500);
      }

"""

CSS = """    /* step three: what the first two steps made, as a list */
    .rec-ready { margin:0; padding:0; list-style:none; }
    .rec-ready li { display:flex; align-items:baseline; gap:12px;
                    padding:11px 0; border-top:1px solid #F1EDFA; }
    .rec-ready li:first-child { border-top:0; padding-top:0; }
    .rec-ready i { font-style:normal; flex:none; width:86px; font-size:11px;
                   letter-spacing:.09em; text-transform:uppercase;
                   color:#8A82A8; }
    .rec-ready b { min-width:0; font-size:14.5px; font-weight:600;
                   color:#1A1430; }
    .rec-ready-go { width:100%; margin-top:18px; }
"""

CSS_ANCHOR = "    .rec-board-head { display:flex;"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-ready-go' not in s, path + ': step three already there'
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    mark = "      // Step two. It builds a board out of step one's company and the\n"
    assert s.count(mark) == 1, (path, 'board anchor', s.count(mark))
    s = s.replace(mark, ACCOUNT_JS + mark, 1)

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS + CSS_ANCHOR, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
