# -*- coding: utf-8 -*-
"""The last step prepares the role to publish, a piece at a time.

Three things get drafted, each on its own line of the same panel the
other steps use: screening questions, interview rounds, and what the
job description says about pay.

The questions are built out of the job description and nothing else --
its skills, one of its own responsibility lines, and where it says the
work happens. A question assembled from the document can be checked
against the document. One invented from a job title cannot.

The rounds come from the role's family: a designer's first round is a
portfolio walkthrough, an engineer's is a technical screen. Three
rounds, named, editable, because a starting point that can be changed
is useful and a fixed process is not.

Pay is the one that cannot be drafted. There is no pay in this job
description and no market data on this page, so it reads what the
document says and asks when the document says nothing. A guessed salary
is the one field here that costs somebody real money when it is
believed.

And the job description itself stays one click away, because every one
of these is a reading of it.
"""
import io
import sys

# --- what the step drafts --------------------------------------------

DRAFT_JS = r"""    // ---- what gets drafted from the job description -------------------

    // the family decides the rounds, and a title is what names it
    var FAMILIES = [
      { is: /(design|ux|ui|brand|creative)/i, key: 'design' },
      { is: /(engineer|developer|programmer|architect|devops|sre|data scien)/i,
        key: 'engineering' },
      { is: /(sales|account exec|business development|partnership)/i,
        key: 'sales' },
      { is: /(market|growth|content|brand manager|seo)/i, key: 'marketing' },
      { is: /(support|success|operations|ops|recruit|hr|people)/i, key: 'ops' }
    ];

    var ROUNDS = {
      design: [
        { say: 'Portfolio walkthrough', mins: '45' },
        { say: 'Craft and product sense', mins: '60' },
        { say: 'Team and founders', mins: '30' }
      ],
      engineering: [
        { say: 'Technical screen', mins: '45' },
        { say: 'System design and pairing', mins: '60' },
        { say: 'Team and founders', mins: '30' }
      ],
      sales: [
        { say: 'Discovery conversation', mins: '30' },
        { say: 'Pitch exercise', mins: '60' },
        { say: 'Leadership', mins: '30' }
      ],
      marketing: [
        { say: 'Intro and past work', mins: '30' },
        { say: 'Campaign exercise', mins: '60' },
        { say: 'Team and founders', mins: '30' }
      ],
      ops: [
        { say: 'Intro and experience', mins: '30' },
        { say: 'Working session', mins: '45' },
        { say: 'Team and founders', mins: '30' }
      ],
      any: [
        { say: 'Intro conversation', mins: '30' },
        { say: 'Skills deep-dive', mins: '60' },
        { say: 'Team and founders', mins: '30' }
      ]
    };

    function family(said) {
      for (var i = 0; i < FAMILIES.length; i++) {
        if (FAMILIES[i].is.test(said || '')) return FAMILIES[i].key;
      }
      return 'any';
    }

    function draft_rounds() {
      return ROUNDS[family(role.title)].map(function (r) {
        return { say: r.say, mins: r.mins };
      });
    }

    // A bullet reads "Own the journey: from user flows to polished UI".
    // The verb phrase is the label; the gloss is what follows it.
    function as_duty(line) {
      var s = String(line || '').replace(/[.\s\u2013\u2014-]+$/, '').trim();
      if (!s) return null;
      // the advert talking about itself, not the work
      if (/^(?:we|our|this role|the role|as a|join)\b/i.test(s)) return null;
      var head = s;
      var tail = '';
      var cut = s.indexOf(':');
      if (cut > 0 && cut < 44) {
        head = s.slice(0, cut).trim();
        tail = s.slice(cut + 1).trim().split(/,|\u2014| and /)[0].trim();
      }
      head = head.replace(/^[A-Z]/, function (c) { return c.toLowerCase(); });
      tail = tail.replace(/^[A-Z]/, function (c) { return c.toLowerCase(); });
      if (head.length < 8 || head.length > 90) return null;
      return { head: head, tail: tail.length > 70 ? '' : tail };
    }

    // every question is assembled out of the document, so every question
    // can be checked against it
    function draft_questions() {
      var out = [];
      var skills = (role.skills || '').split(',').map(function (s) {
        return s.trim();
      }).filter(Boolean);

      if (skills.length >= 2) {
        out.push('Tell us about something you shipped with ' + skills[0] +
                 ' and ' + skills[1] + '. What was yours in it?');
      } else if (skills.length === 1) {
        out.push('Tell us about something you shipped with ' + skills[0] +
                 '. What was yours in it?');
      } else if (role.title) {
        out.push('Tell us about the piece of work you are proudest of as a ' +
                 role.title.toLowerCase() + '.');
      }

      var duties = (jd && jd.duties) || [];
      for (var i = 0; i < duties.length && out.length < 2; i++) {
        var d = as_duty(duties[i]);
        if (!d) continue;
        out.push('This role asks you to ' + d.head +
                 (d.tail ? ' \u2014 ' + d.tail : '') +
                 '. When have you done that, and how did it go?');
      }
      if (out.length < 2 && role.years) {
        out.push('You would be coming in at ' + role.years +
                 '. What does that experience look like day to day?');
      }

      if (role.mode && role.place) {
        out.push('This role is ' + role.mode.toLowerCase() + ' in ' +
                 role.place + '. Does that work for you?');
      } else if (role.place) {
        out.push('This role is based in ' + role.place +
                 '. Does that work for you?');
      } else {
        out.push('What are you looking for in your next role, and when ' +
                 'could you start?');
      }
      return out.slice(0, 3);
    }

    // what the job description says about pay, which is often nothing
    function draft_pay() {
      var text = (jd && jd.text) || '';
      var m = text.match(
        /(?:₹|INR|Rs\.?|\$|USD)\s?[\d,.]+\s?(?:[-–to]+\s?(?:₹|INR|Rs\.?|\$|USD)?\s?[\d,.]+)?\s*(?:LPA|lakh|lakhs|per annum|a year|\/year|k)?/i);
      if (m && /\d/.test(m[0])) return m[0].trim();
      return '';
    }

"""

# --- the screen -------------------------------------------------------

SCREEN_JS = r"""    function role_html() {
      return '<div class="rec-found-col">' +
        '<h2 class="rec-flow-q">Your role is ready to publish</h2>' +
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
          '</div>' +

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
          '</div>' +

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
          '</div>' +

          '<button type="button" class="rec-flow-next rec-ready-go" ' +
            'data-login="1">Sign in to your account</button>' +
        '</div>' +
      '</div>';
    }
"""

# --- what the panel says while it drafts ------------------------------

STEP_JS = r"""      function role_step() {
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

        var jobs = [
          'writing three screening questions',
          'laying out the interview rounds',
          'reading the job description for pay'
        ];
        var ran = [];
        var now = 0;

        function panel() {
          card.innerHTML =
            '<h2 class="rec-flow-q is-alone">Preparing your role to ' +
              'publish</h2>' +
            '<div class="rec-work" role="status" aria-live="polite">' +
              '<p class="rec-work-head"><span class="rec-work-dot"></span>' +
                'Mira is working on step ' + Math.min(now + 1, jobs.length) +
                ' of ' + jobs.length + '</p>' +
              ran.map(function (r) {
                return '<p class="rec-work-line is-done"><i>✓</i>' +
                  '<span>' + esc(r) + '</span></p>';
              }).join('') +
              (now < jobs.length
                ? '<p class="rec-work-line is-now"><i>›</i><span>' +
                  esc(jobs[now]) + '…</span><b></b></p>'
                : '') +
            '</div>';
        }

        // each line does the thing it says, then rests long enough to read
        function step(work, then) {
          var say = jobs[now];
          work();
          ran.push(say);
          now++;
          panel();
          window.setTimeout(then, 700);
        }

        panel();
        window.setTimeout(function () {
          if (!flow || flow.hidden) return;
          step(function () { role.questions = draft_questions(); }, function () {
            step(function () { role.rounds = draft_rounds(); }, function () {
              step(function () { role.pay = draft_pay(); }, ready);
            });
          });
        }, 520);

        function ready() {
          if (!flow || flow.hidden) return;
          at_step(2, true);
          flow.querySelector('.rec-flow-bar span')
              .style.setProperty('--at', '100%');
          card.innerHTML = role_html();
          put_mini(2, 'Role details', role.title || 'as read', found.logo,
                   role_html());
          // filed open: the screen it holds is the one on screen
          open_i = 2;
          var mine = flow.querySelector('.rec-done-card[data-for="2"]');
          if (mine) mine.setAttribute('aria-expanded', 'true');
          remember();
          wire_role(card);
        }
      }
"""

# --- the wiring, for a first render and every reopen -------------------

WIRE_JS = r"""    // re-injected HTML brings no listeners, so this runs on every render
    function wire_role(root) {
      if (!root) return;

      function kept_again() { kept[2] = role_html(); remember(); }

      root.querySelectorAll('.rec-role-in').forEach(function (box) {
        box.addEventListener('input', function () {
          var k = box.getAttribute('data-k');
          role[k] = box.value;
          if (k === 'title') {
            var said = box.value.split(',')[0].trim();
            brief.role = box.value;
            retitle_board(said || 'Your first role');
            put_mini(2, 'Role details', said || 'as read',
                     (company && company.logo) || '', role_html());
            remember();
          } else {
            kept_again();
          }
        });
      });
      root.querySelectorAll('[data-mode]').forEach(function (b) {
        b.addEventListener('click', function () {
          var was = role.mode;
          role.mode = (was === b.getAttribute('data-mode'))
            ? '' : b.getAttribute('data-mode');
          root.querySelectorAll('[data-mode]').forEach(function (o) {
            o.classList.toggle('is-on',
              !!role.mode && o.getAttribute('data-mode') === role.mode);
          });
          kept_again();
        });
      });
      root.querySelectorAll('.rec-q-in').forEach(function (box) {
        box.addEventListener('input', function () {
          role.questions[Number(box.getAttribute('data-q'))] = box.value;
          kept_again();
        });
      });
      root.querySelectorAll('.rec-r-in').forEach(function (box) {
        box.addEventListener('input', function () {
          role.rounds[Number(box.getAttribute('data-r'))].say = box.value;
          kept_again();
        });
      });
      root.querySelectorAll('.rec-r-min').forEach(function (box) {
        box.addEventListener('input', function () {
          role.rounds[Number(box.getAttribute('data-m'))].mins =
            box.value.replace(/[^0-9]/g, '');
          kept_again();
        });
      });
      var see = root.querySelector('.rec-jd-see');
      if (see) see.addEventListener('click', show_jd);
      root.querySelectorAll('[data-login]').forEach(function (b) {
        b.addEventListener('click', open_account);
      });
    }

    // the document all of this was read out of, kept one click away
    function show_jd() {
      if (!jd) return;
      var box = document.createElement('div');
      box.className = 'rec-jd-ov';
      box.innerHTML =
        '<div class="rec-jd-sheet" role="dialog" aria-modal="true" ' +
          'aria-label="The job description">' +
          '<div class="rec-jd-top"><b>' + esc(jd_name || 'The job ' +
            'description') + '</b>' +
            (jd_file ? '<a class="rec-jd-open" target="_blank" rel="noopener">' +
              'Open the original</a>' : '') +
            '<button type="button" class="rec-jd-x" aria-label="Close">' +
              '×</button></div>' +
          '<pre class="rec-jd-text">' + esc(jd.text || '') + '</pre>' +
        '</div>';
      document.body.appendChild(box);

      var url = '';
      var link = box.querySelector('.rec-jd-open');
      if (link && jd_file) {
        url = window.URL.createObjectURL(jd_file);
        link.href = url;
      }
      function shut() {
        if (url) window.URL.revokeObjectURL(url);
        box.remove();
        document.removeEventListener('keydown', esc_shut);
      }
      function esc_shut(e) { if (e.key === 'Escape') shut(); }
      box.querySelector('.rec-jd-x').addEventListener('click', shut);
      box.addEventListener('click', function (e) {
        if (e.target === box) shut();
      });
      document.addEventListener('keydown', esc_shut);
    }

"""

CSS = """    /* the parts of the last screen */
    .rec-part { margin-top:22px; padding-top:18px;
                border-top:1px solid #F0EDF7; }
    .rec-part-head { display:flex; align-items:baseline; gap:10px;
                     flex-wrap:wrap; margin:0 0 12px; font-size:14px;
                     font-weight:700; color:#1A1430; }
    .rec-part-head span { font-size:12px; font-weight:500; color:#9A93B8; }
    .rec-part-say { margin:10px 0 0; font-size:12.5px; color:#9A93B8; }
    .rec-qs, .rec-rounds { margin:0; padding:0; list-style:none;
                           display:flex; flex-direction:column; gap:10px; }
    .rec-qs li, .rec-rounds li { display:flex; align-items:flex-start;
                                 gap:11px; }
    .rec-qs b, .rec-rounds b { flex:none; width:22px; height:22px;
                               margin-top:5px; border-radius:50%;
                               display:grid; place-items:center;
                               background:#F1EEFA; color:#6B4BE8;
                               font-size:11px; font-weight:700; }
    .rec-q-in { flex:1; min-width:0; resize:vertical; overflow-x:hidden;
                border:1px solid #ECE7F9;
                border-radius:10px; padding:9px 12px; background:#FFFFFF;
                font:inherit; font-size:14px; line-height:1.45;
                color:#2A2440; outline:none; }
    .rec-q-in:focus { border-color:#7C5CF6; background:#FCFBFF; }
    .rec-rounds li { align-items:center; }
    .rec-rounds b { margin-top:0; }
    .rec-r-in { flex:1; min-width:0; border:1px solid #ECE7F9;
                border-radius:10px; padding:9px 12px; background:#FFFFFF;
                font:inherit; font-size:14px; font-weight:600; color:#1A1430;
                outline:none; }
    .rec-r-in:focus { border-color:#7C5CF6; background:#FCFBFF; }
    .rec-r-mins { flex:none; display:inline-flex; align-items:center; gap:4px;
                  font-size:12.5px; color:#9A93B8; }
    .rec-r-min { width:38px; border:1px solid #ECE7F9; border-radius:8px;
                 padding:7px 6px; background:#FFFFFF; font:inherit;
                 font-size:13px; font-weight:600; color:#1A1430;
                 text-align:center; outline:none; }
    .rec-r-min:focus { border-color:#7C5CF6; }
    .rec-jd-see { border:0; padding:0 0 1px; background:none; font:inherit;
                  font-size:inherit; color:#6B4BE8; cursor:pointer;
                  text-decoration:underline; text-underline-offset:3px; }
    .rec-jd-see:hover { color:#4A32C0; }

    /* the document itself */
    /* above the flow (300), which is what it is opened from */
    .rec-jd-ov { position:fixed; inset:0; z-index:320; display:flex;
                 align-items:center; justify-content:center; padding:24px;
                 background:rgba(18,16,34,.42); }
    .rec-jd-sheet { display:flex; flex-direction:column; width:min(680px,100%);
                    max-height:min(76vh,760px); border-radius:16px;
                    background:#FFFFFF; overflow:hidden;
                    box-shadow:0 24px 64px rgba(18,22,32,.24); }
    .rec-jd-top { display:flex; align-items:center; gap:12px;
                  padding:14px 18px; border-bottom:1px solid #F0EDF7; }
    .rec-jd-top b { flex:1; min-width:0; font-size:14px; color:#1A1430;
                    overflow:hidden; text-overflow:ellipsis;
                    white-space:nowrap; }
    .rec-jd-open { flex:none; font-size:12.5px; color:#6B4BE8;
                   text-decoration:underline; text-underline-offset:3px; }
    .rec-jd-x { flex:none; width:28px; height:28px; border:0; border-radius:50%;
                background:#F4F2FB; color:#6B6487; font-size:17px;
                line-height:1; cursor:pointer; }
    .rec-jd-x:hover { background:#EAE6F8; color:#1A1430; }
    .rec-jd-text { margin:0; padding:18px; overflow:auto; font:inherit;
                   font-size:13px; line-height:1.6; color:#3A3356;
                   white-space:pre-wrap; word-break:break-word; }
    @media (max-width:560px) {
      .rec-rounds li { flex-wrap:wrap; }
      .rec-r-in { flex-basis:100%; order:2; }
    }
"""

CSS_ANCHOR = "    .rec-role-pick button:focus-visible { outline:2px solid #7C5CF6;\n" \
             "                                          outline-offset:2px; }"


def cut(s, head, tail, what):
    at = s.index(head)
    end = s.index(tail, at)
    return s[:at], s[end:]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'draft_questions' not in s, path + ': already drafts'

    # the state this step keeps
    old = ("    var role = { title: '', place: '', mode: '', years: '', "
           "skills: '' };")
    new = ("    var role = { title: '', place: '', mode: '', years: '',\n"
           "                 skills: '', pay: '', questions: [], rounds: [] };\n"
           "    var jd_file = null;       // the file itself, to open the "
           "original\n    var jd_name = '';         // what it was called")
    assert s.count(old) == 1, (path, 'role state', s.count(old))
    s = s.replace(old, new, 1)

    # role_html, rebuilt
    head, rest = cut(s, '    function role_html() {',
                     '    function role_row(r) {', 'role_html')
    s = head + SCREEN_JS + '\n' + rest

    # wire_role and the drafting helpers
    head, rest = cut(s, '    // re-injected HTML brings no listeners,',
                     '    // what a finished step leaves behind', 'wire_role')
    s = head + DRAFT_JS + WIRE_JS + rest

    # the step itself
    head, rest = cut(s, '      function role_step() {',
                     '\n      function board() {', 'role_step')
    s = head + STEP_JS + rest

    # the reader keeps the file, so the original can be opened
    # not the line above it: that one carries an ellipsis the page stores
    # as the character, not the escape
    old = """      read_jd(file).then(function (text) {
        drop_busy(false);"""
    new = """      read_jd(file).then(function (text) {
        drop_busy(false);
        jd_file = file;
        jd_name = file.name || '';"""
    assert s.count(old) == 1, (path, 'keep the file', s.count(old))
    s = s.replace(old, new, 1)

    old = """        from_jd(field.value, 'the text you pasted');"""
    new = """        jd_file = null;
        jd_name = 'The job description you pasted';
        from_jd(field.value, 'the text you pasted');"""
    assert s.count(old) == 1, (path, 'paste name', s.count(old))
    s = s.replace(old, new, 1)

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS_ANCHOR + '\n' + CSS, 1)

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
