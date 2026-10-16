# -*- coding: utf-8 -*-
"""The last step is the role, and it is the visitor's turn.

Step three used to be an account being prepared, which was three lines
of spinner over work nobody was doing: naming a workspace, attaching an
address, adding a role. All three were already decided.

It shows the role instead, as fields, because a rules parser is right
about most of a job description and wrong about some of it, and the
difference between useful and dishonest is whether the thing it got
wrong can be corrected before it is used. Nothing it was unsure of is
filled in -- those ask.

No panel and no spinner here: Mira is not working, the visitor is. The
step is ticked because the reading did happen; what follows it is a
button, not a wait.

An edit to the title reaches back into the board card above it, which
was built from the old one. A preview that disagrees with the field
that feeds it is worse than no preview.
"""
import io
import sys

# --- the rail says what the step is ----------------------------------

EDITS = [
    ("""            ['Company details', 'Job board', 'Account']""",
     """            ['Company details', 'Job board', 'Role details']"""),

    # the third step, rebuilt: no panel, no invented work
    ("""      function account() {""",
     """      function role_step() {"""),

    ("""            window.setTimeout(account, 700);""",
     """            window.setTimeout(role_step, 700);"""),

    # the restore puts back a role card, not an account one
    ("""      if (screens[2]) { put_mini(2, 'Account', 'ready to open',
                                 was.logo, screens[2]);
                        last = 2; }""",
     """      if (screens[2]) {
        var said = String(was.role || '').split(',')[0].trim();
        put_mini(2, 'Role details', said || 'as read', was.logo, screens[2]);
        last = 2;
      }"""),
]

# --- the screen itself ------------------------------------------------

ROLE_JS = r"""    // what the last step shows, and what a change to it touches
    var role = { title: '', place: '', mode: '', years: '', skills: '' };

    var ROLE_ROWS = [
      { k: 'title', say: 'Role', hint: 'What are you hiring for?' },
      { k: 'place', say: 'Location', hint: 'Add a location' },
      { k: 'years', say: 'Experience', hint: 'Add a range' },
      { k: 'skills', say: 'Skills', hint: 'Add a few' }
    ];
    var MODES = ['On-site', 'Hybrid', 'Remote'];

    function role_html() {
      return '<div class="rec-found-col">' +
        '<h2 class="rec-flow-q">' +
          (jd ? 'The role, as I read it' : 'The role you are hiring for') +
        '</h2>' +
        '<p class="rec-flow-hint">' +
          (jd ? 'Change anything I got wrong — this is what goes on ' +
                'your board.'
              : 'Fill in what you know. You can change all of it later.') +
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
          '<button type="button" class="rec-flow-next rec-ready-go" ' +
            'data-login="1">Sign in to your account</button>' +
        '</div>' +
      '</div>';
    }

    function role_row(r) {
      return '<label class="rec-role-row"><i>' + esc(r.say) + '</i>' +
        '<input class="rec-role-in" data-k="' + r.k + '" value="' +
          esc(role[r.k] || '') + '" placeholder="' + esc(r.hint) + '"></label>';
    }

    // the board card above was built from the title: keep them the same
    function retitle_board(said) {
      if (!kept[1]) return;
      var box = document.createElement('div');
      box.innerHTML = kept[1];
      var b = box.querySelector('.rec-board-role b');
      if (!b) return;
      b.textContent = said;
      kept[1] = box.innerHTML;
      if (open_i === 1) {
        var face = flow.querySelector('.rec-flow-card');
        if (face) face.innerHTML = kept[1];
      }
    }

    // re-injected HTML brings no listeners, so this runs on every render
    function wire_role(root) {
      if (!root) return;
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
          } else {
            kept[2] = role_html();
          }
          remember();
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
          kept[2] = role_html();
          remember();
        });
      });
    }

"""

# --- the body of the step --------------------------------------------

OLD_STEP_HEAD = """      function role_step() {
        if (!found.who) return;"""

NEW_STEP = r"""      function role_step() {
        if (!found.who) return;
        flow.classList.remove('is-found');
        open_i = null;

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
        card.querySelectorAll('[data-login]').forEach(function (b) {
          b.addEventListener('click', open_account);
        });
      }
"""

CSS = """    /* the last step: fields, because a reading can be wrong */
    .rec-role { display:flex; flex-direction:column; }
    .rec-role-row { display:flex; align-items:center; gap:12px;
                    padding:11px 0; border-top:1px solid #F0EDF7; }
    .rec-role-row:first-child { border-top:0; padding-top:0; }
    .rec-role-row i { flex:none; width:86px; font-style:normal; font-size:11px;
                      font-weight:600; letter-spacing:.07em;
                      text-transform:uppercase; color:#9A93B8; }
    .rec-role-in { flex:1; min-width:0; border:0; padding:4px 2px;
                   background:none; font:inherit; font-size:14.5px;
                   font-weight:600; color:#1A1430; border-radius:6px;
                   outline:none; }
    .rec-role-in::placeholder { font-weight:500; color:#B4AECB; }
    .rec-role-in:hover { background:#FAF8FE; }
    .rec-role-in:focus { background:#F6F3FF;
                         box-shadow:inset 0 -2px 0 #7C5CF6; }
    .rec-role-pick { display:flex; flex-wrap:wrap; gap:6px; }
    .rec-role-pick button { padding:5px 12px; border-radius:100px;
                            border:1px solid #E7E2F6; background:#FFFFFF;
                            font:inherit; font-size:13px; font-weight:600;
                            color:#6B6487; cursor:pointer;
                            transition:border-color .14s, color .14s,
                                       background .14s; }
    .rec-role-pick button:hover { border-color:#BCAEF0; color:#4B3BC8; }
    .rec-role-pick button.is-on { border-color:#7C5CF6; background:#F3EFFE;
                                  color:#4B3BC8; }
    .rec-role-pick button:focus-visible { outline:2px solid #7C5CF6;
                                          outline-offset:2px; }
    @media (max-width:560px) {
      .rec-role-row { align-items:flex-start; flex-direction:column; gap:4px; }
      .rec-role-row i { width:auto; }
      .rec-role-in { width:100%; }
    }
"""

CSS_ANCHOR = "    .rec-ready-go { width:100%; margin-top:18px; }"

# a reopened role screen gets its fields wired again
REWIRE = ("""      // re-injected HTML has no listeners of its own
      face.querySelectorAll('[data-login]').forEach(function (b) {
        b.addEventListener('click', open_account);
      });""",
          """      // re-injected HTML has no listeners of its own
      face.querySelectorAll('[data-login]').forEach(function (b) {
        b.addEventListener('click', open_account);
      });
      if (i === 2) wire_role(face);""")


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-role-in' not in s, path + ': already a role step'

    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    # the old third step, from its head to the line that closed it
    at = s.index(OLD_STEP_HEAD)
    end = s.index('\n      function board() {', at)
    s = s[:at] + NEW_STEP + s[end + 1:]

    old, new = REWIRE
    assert s.count(old) == 1, (path, 'rewire', s.count(old))
    s = s.replace(old, new, 1)

    mark = "    // what a finished step leaves behind, under that step\n"
    assert s.count(mark) == 1, (path, 'role anchor', s.count(mark))
    s = s.replace(mark, ROLE_JS + mark, 1)

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS_ANCHOR + '\n' + CSS, 1)

    for gone in ('naming your workspace', 'rec-ready-go">Open',
                 "put_mini(2, 'Account'"):
        assert gone not in s, (path, gone + ' survives')

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
