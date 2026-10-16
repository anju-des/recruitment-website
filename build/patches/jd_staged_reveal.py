# -*- coding: utf-8 -*-
"""The last step builds itself in front of you, a section at a time.

It used to spend three lines in a work panel and then put the whole
finished screen up at once, which meant the panel described work whose
result you could not see and the screen arrived with no account of
where any of it came from.

Now the summary comes up first -- it is the one part that was already
read -- and each section that follows is preceded by the line saying
what is being written. The same thinking line the company lookup uses,
in the same place: under what exists, above what is coming.

The card it files is the finished screen, not whichever part was on
screen when it was filed, so reopening it shows all of it.
"""
import io
import sys

# --- the screen takes a part count -----------------------------------

OLD_HEAD = "    function role_html() {"
OLD_TAIL = "    function role_row(r) {"

NEW_SCREEN = r"""    // how much of the screen exists yet: 0 summary, 1 questions,
    // 2 rounds, 3 pay and the way out. `tell` is the line saying what is
    // being written next.
    function role_html(upto, tell) {
      var at = (upto === undefined) ? 3 : upto;
      return '<div class="rec-found-col">' +
        '<h2 class="rec-flow-q">' +
          (at < 3 ? 'Preparing your role to publish'
                  : 'Your role is ready to publish') + '</h2>' +
        '<p class="rec-flow-hint">' +
          (jd ? 'Drafted from your job description. Change anything — ' +
                'none of it is fixed.'
              : 'A starting point. Change anything — none of it is ' +
                'fixed.') +
          (jd ? ' <button type="button" class="rec-jd-see">View the job ' +
                'description</button>' : '') +
        '</p>' +
        '<div class="rec-found-card">' +
          '<div class="rec-role">' +
            ROLE_ROWS.slice(0, 2).map(role_row).join('') +
            '<div class="rec-role-row"><i>Work mode</i>' +
              '<span class="rec-role-pick">' +
                MODES.map(function (m) {
                  return '<button type="button" data-mode="' + esc(m) + '"' +
                    (role.mode === m ? ' class="is-on"' : '') + '>' +
                    esc(m) + '</button>';
                }).join('') +
              '</span></div>' +
            ROLE_ROWS.slice(2).map(role_row).join('') +
          '</div>' +

          (at >= 1 ?
          '<div class="rec-part">' +
            '<h3 class="rec-part-head">Screening questions' +
              '<span>asked before anyone reaches you</span></h3>' +
            '<ol class="rec-qs">' +
              role.questions.map(function (q, i) {
                return '<li><b>' + (i + 1) + '</b>' +
                  // a long question gets the line it needs, not a scrollbar
                  '<textarea class="rec-q-in" rows="' +
                    (q.length > 86 ? 3 : 2) + '" data-q="' + i + '">' +
                  esc(q) + '</textarea></li>';
              }).join('') +
            '</ol>' +
          '</div>' : '') +

          (at >= 2 ?
          '<div class="rec-part">' +
            '<h3 class="rec-part-head">Interview rounds' +
              '<span>' + esc(family(role.title) === 'any'
                ? 'a standard three' : 'typical for this kind of role') +
              '</span></h3>' +
            '<ol class="rec-rounds">' +
              role.rounds.map(function (r, i) {
                return '<li><b>' + (i + 1) + '</b>' +
                  '<input class="rec-r-in" data-r="' + i + '" value="' +
                    esc(r.say) + '">' +
                  '<span class="rec-r-mins">' +
                    '<input class="rec-r-min" data-m="' + i + '" value="' +
                      esc(r.mins) + '" inputmode="numeric">min</span></li>';
              }).join('') +
            '</ol>' +
          '</div>' : '') +

          (at >= 3 ?
          '<div class="rec-part">' +
            '<h3 class="rec-part-head">Pay' +
              '<span>' + (role.pay
                ? 'as the job description states it'
                : 'the job description does not say') + '</span></h3>' +
            '<div class="rec-role-row"><i>Salary</i>' +
              '<input class="rec-role-in" data-k="pay" value="' +
                esc(role.pay || '') + '" placeholder="' +
                'Add what you are paying"></div>' +
            (role.pay ? '' :
              '<p class="rec-part-say">Mira can estimate this once your own ' +
              'placement data is behind it. It will not guess one.</p>') +
          '</div>' : '') +

          (tell
            ? '<p class="rec-tell"><i>›</i><span>' + esc(tell) +
              '…</span><b></b></p>'
            : '') +

          (at >= 3
            ? '<button type="button" class="rec-flow-next rec-ready-go" ' +
              'data-login="1">Sign in to your account</button>'
            : '') +
        '</div>' +
      '</div>';
    }

"""

# --- the step, rebuilt as a reveal ------------------------------------

OLD_STEP_HEAD = "      function role_step() {"
OLD_STEP_TAIL = "\n      function board() {"

NEW_STEP = r"""      function role_step() {
        if (!found.who) return;
        flow.classList.remove('is-found');
        open_i = null;
        step_busy(2);

        // seeded from the job description, where there was one
        var said = (brief.role || '').split(',')[0].trim();
        role.title = role.title || said;
        if (jd) {
          role.place = role.place || jd.place || '';
          role.mode = role.mode || jd.mode || '';
          role.years = role.years || jd.years || '';
          role.skills = role.skills ||
            ((jd.skills && jd.skills.join(', ')) || '');
        }

        // what is written, in the order it is written, each announced
        // before it appears
        var parts = [
          { say: 'writing three screening questions',
            work: function () { role.questions = draft_questions(); } },
          { say: 'laying out the interview rounds',
            work: function () { role.rounds = draft_rounds(); } },
          { say: 'reading the job description for pay',
            work: function () { role.pay = draft_pay(); } }
        ];

        function show(at, tell) {
          card.innerHTML = role_html(at, tell);
          wire_role(card);
        }

        // the summary first: it is the part that was already read
        show(0, '');
        window.setTimeout(function () {
          if (!flow || flow.hidden) return;
          next(0);
        }, 620);

        function next(i) {
          if (!flow || flow.hidden) return;
          if (i >= parts.length) { ready(); return; }
          show(i, parts[i].say);          // the line, then the section
          window.setTimeout(function () {
            if (!flow || flow.hidden) return;
            parts[i].work();
            show(i + 1, '');
            window.setTimeout(function () { next(i + 1); }, 520);
          }, 900);
        }

        function ready() {
          if (!flow || flow.hidden) return;
          at_step(2, true);
          flow.querySelector('.rec-flow-bar span')
              .style.setProperty('--at', '100%');
          show(3, '');
          // the card keeps the finished screen, not the part on show
          put_mini(2, 'Role details', role.title || 'as read', found.logo,
                   role_html());
          // filed open: the screen it holds is the one on screen
          open_i = 2;
          var mine = flow.querySelector('.rec-done-card[data-for="2"]');
          if (mine) mine.setAttribute('aria-expanded', 'true');
          remember();
        }
      }
"""

# the sections arrive rather than appear
CSS = """    .rec-part { animation:rec-part-in .34s ease both; }
    @keyframes rec-part-in { from { opacity:0; transform:translateY(6px); }
                             to { opacity:1; transform:none; } }
    @media (prefers-reduced-motion: reduce) {
      .rec-part { animation:none; }
    }
"""

CSS_ANCHOR = """    .rec-part-say { margin:10px 0 0; font-size:12.5px; color:#9A93B8; }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-part-in' not in s, path + ': already staged'

    at = s.index(OLD_HEAD)
    end = s.index(OLD_TAIL, at)
    assert end > at, (path, 'the screen slice runs backwards')
    s = s[:at] + NEW_SCREEN + s[end:]

    at = s.index(OLD_STEP_HEAD)
    end = s.index(OLD_STEP_TAIL, at)
    assert end > at, (path, 'the step slice runs backwards')
    s = s[:at] + NEW_STEP + s[end:]

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS_ANCHOR + '\n' + CSS, 1)

    # the work panel this step used to put up has no place here any more
    assert 'Preparing your role to ' in s, (path, 'the heading went missing')
    assert s.count('function role_html') == 1, (path, 'two screens')
    assert s.count('function role_step') == 1, (path, 'two steps')

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
