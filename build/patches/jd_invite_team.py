# -*- coding: utf-8 -*-
"""Whoever is going to interview can be asked along.

An invite button on the last screen, and beside it the company's
headcount where the open register publishes one -- P1128, which the
lookup already reads for the facts on the company card, so the figure
is the same one shown two steps earlier and comes from the same place.
No headcount on the record, no number: there is nothing to put there
and a guess would be worse than the gap.

Nothing is sent. The emails sit on the role until there is an account
to attach them to, and the line under the button says so rather than
implying that three people have just been mailed.
"""
import io
import sys

EDITS = [
    # the lookup already has the number: keep it
    ("""            found = { who: who, logo: logo, based: vals.Based || '' };""",
     """            found = { who: who, logo: logo, based: vals.Based || '',
                      people: vals.People || '' };"""),

    # it travels with the rest of the record
    ("""          who: company.who, logo: company.logo, based: company.based || '',
          rounds: role.rounds,""",
     """          who: company.who, logo: company.logo, based: company.based || '',
          people: company.people || '', rounds: role.rounds,"""),

    ("""      company = { who: was.who, logo: was.logo, based: was.based || '' };""",
     """      company = { who: was.who, logo: was.logo, based: was.based || '',
                  people: was.people || '' };"""),

    # the state the section keeps
    ("""    var role = { title: '', place: '', mode: '', years: '',
                 skills: '', pay: '', pay_from: '', pay_for: '',
                 pay_refs: [], questions: [], rounds: [] };""",
     """    var role = { title: '', place: '', mode: '', years: '',
                 skills: '', pay: '', pay_from: '', pay_for: '',
                 pay_refs: [], questions: [], rounds: [], team: [] };"""),

    # the section itself, after pay and before the way out
    ("""          (at >= 3
            ? '<button type="button" class="rec-flow-next rec-ready-go" ' +""",
     """          (at >= 3 ?
          '<div class="rec-part">' +
            '<h3 class="rec-part-head">Hiring team' +
              '<button type="button" class="rec-invite" data-invite="1">' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
                  'stroke-width="1.9" stroke-linecap="round" ' +
                  'stroke-linejoin="round" aria-hidden="true">' +
                  '<circle cx="9" cy="8" r="3.2"/>' +
                  '<path d="M3.5 19a5.5 5.5 0 0 1 11 0"/>' +
                  '<path d="M18 8.5v5M20.5 11h-5"/></svg>Invite</button>' +
            '</h3>' +
            (role.team.length
              ? '<ul class="rec-team">' +
                  role.team.map(function (who, i) {
                    return '<li><input class="rec-team-in" type="email" ' +
                      'data-t="' + i + '" value="' + esc(who) + '" ' +
                      'placeholder="name@' +
                      esc(board_addr((company && company.who) || '')
                            .replace('.mira.jobs', '.com')) + '">' +
                      row_x('team', i) + '</li>';
                  }).join('') +
                '</ul>' +
                '<p class="rec-part-say">They get access when you open the ' +
                  'account. Nothing is sent from this page.</p>'
              : '<p class="rec-part-say">Whoever is interviewing can read ' +
                'every application as it lands' +
                ((company && company.people)
                  ? ' \\u2014 ' + esc(company.people) + ' people at ' +
                    esc(company.who)
                  : '') + '.</p>') +
          '</div>' : '') +

          (at >= 3
            ? '<button type="button" class="rec-flow-next rec-ready-go" ' +"""),

    # one more list for the row remover to know about
    ("""          var list = b.getAttribute('data-drop') === 'qs'
            ? role.questions : role.rounds;""",
     """          var which = b.getAttribute('data-drop');
          var list = which === 'qs' ? role.questions
            : which === 'team' ? role.team : role.rounds;"""),
]

WIRE_JS = """
      root.querySelectorAll('[data-invite]').forEach(function (b) {
        b.addEventListener('click', function () {
          role.team.push('');
          again('.rec-team-in[data-t="' + (role.team.length - 1) + '"]');
        });
      });
      root.querySelectorAll('.rec-team-in').forEach(function (box) {
        box.addEventListener('input', function () {
          role.team[Number(box.getAttribute('data-t'))] = box.value;
          kept_again();
        });
      });
"""

WIRE_ANCHOR = """      var see = root.querySelector('.rec-jd-see');"""

CSS = """    .rec-invite { margin-left:auto; flex:none; display:inline-flex;
                  align-items:center; gap:6px; padding:6px 12px;
                  border-radius:8px; border:1px solid #E7E2F6;
                  background:#F7F5FE; color:#6B4BE8; font:inherit;
                  font-size:12.5px; font-weight:600; cursor:pointer;
                  transition:background .14s, border-color .14s; }
    .rec-invite svg { width:15px; height:15px; }
    .rec-invite:hover { background:#EFEAFF; border-color:#BCAEF0; }
    .rec-invite:focus-visible { outline:2px solid #7C5CF6;
                                outline-offset:2px; }
    .rec-team { margin:0; padding:0; list-style:none; display:flex;
                flex-direction:column; gap:3px; }
    .rec-team li { display:flex; align-items:center; gap:8px;
                   border-radius:10px; transition:background .14s; }
    .rec-team li:hover, .rec-team li:focus-within { background:#FAF9FE; }
    .rec-team-in { flex:1; min-width:0; border:1px solid transparent;
                   border-radius:9px; padding:9px 10px 9px 0; background:none;
                   font:inherit; font-size:14px; color:#2A2440; outline:none; }
    .rec-team-in::placeholder { color:#B4AECB; }
    .rec-team-in:focus { border-color:#D8CFF8; background:#FFFFFF;
                         padding-left:10px; }
"""

CSS_ANCHOR = """    .rec-part-add { margin-left:auto; flex:none; width:24px; height:24px;"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-invite' not in s, path + ': already invites'

    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    assert s.count(WIRE_ANCHOR) == 1, (path, 'wire', s.count(WIRE_ANCHOR))
    s = s.replace(WIRE_ANCHOR, WIRE_JS + '\n' + WIRE_ANCHOR, 1)

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS + CSS_ANCHOR, 1)

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
