# -*- coding: utf-8 -*-
"""Invite moves to the header, and the plus loses its box.

Inviting is not part of reading a role, it is something you do to the
whole thing -- so it sits in the header beside the publish button,
where actions that apply to everything live. It appears when there is a
role to invite people to and not before, since an invitation to nothing
is not an offer.

Pressing it opens the role, adds a row in the hiring team and puts the
cursor in it, which is what the button in that section did. There is no
second button there now: two ways to do one thing in two places is how
they drift apart.

And the plus beside the question and round headings drops its border.
It is a small mark next to a heading, not a button on a form, and the
box around it was competing with the headings it belongs to.
"""
import io
import sys

EDITS = [
    # the header carries it
    ("""          '<button type="button" class="rec-flow-cta" data-login="1">' +
            'Publish role for free</button>' +""",
     """          '<span class="rec-flow-acts">' +
            '<button type="button" class="rec-invite rec-invite-top" ' +
              'data-invite-top="1" hidden>' +
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
                'stroke-width="1.9" stroke-linecap="round" ' +
                'stroke-linejoin="round" aria-hidden="true">' +
                '<circle cx="9" cy="8" r="3.2"/>' +
                '<path d="M3.5 19a5.5 5.5 0 0 1 11 0"/>' +
                '<path d="M18 8.5v5M20.5 11h-5"/></svg>Invite' +
              '<em class="rec-invite-n"></em></button>' +
            '<button type="button" class="rec-flow-cta" data-login="1">' +
              'Publish role for free</button>' +
          '</span>' +"""),

    # wired once, where the header is built
    ("""      flow.querySelector('.rec-flow-cta')
          .addEventListener('click', open_account);""",
     """      flow.querySelector('.rec-flow-cta')
          .addEventListener('click', open_account);
      flow.querySelector('[data-invite-top]')
          .addEventListener('click', invite_one);"""),

    # the section exists only once there are people in it: with the button
    # in the header, an empty one has nothing left to offer
    ("""          (at >= 3 && role.tab === 'role' ?
          '<div class="rec-part">' +
            '<h3 class="rec-part-head">Hiring team' +""",
     """          (at >= 3 && role.tab === 'role' && role.team.length ?
          '<div class="rec-part">' +
            '<h3 class="rec-part-head">Hiring team' +"""),

    # with the section conditional, the empty branch is unreachable
    ("""            (role.team.length
              ? '<ul class="rec-team">'""",
     """            ('<ul class="rec-team">'"""),

    # the section keeps its people and loses its button
    ("""            '<h3 class="rec-part-head">Hiring team' +
              '<button type="button" class="rec-invite" data-invite="1">' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
                  'stroke-width="1.9" stroke-linecap="round" ' +
                  'stroke-linejoin="round" aria-hidden="true">' +
                  '<circle cx="9" cy="8" r="3.2"/>' +
                  '<path d="M3.5 19a5.5 5.5 0 0 1 11 0"/>' +
                  '<path d="M18 8.5v5M20.5 11h-5"/></svg>Invite</button>' +
            '</h3>' +""",
     """            '<h3 class="rec-part-head">Hiring team</h3>' +"""),

    ("""      root.querySelectorAll('[data-invite]').forEach(function (b) {
        b.addEventListener('click', function () {
          role.team.push('');
          again('.rec-team-in[data-t="' + (role.team.length - 1) + '"]');
        });
      });
""", ""),

    # the plus is a mark, not a button
    ("""    .rec-part-add { margin-left:auto; flex:none; width:24px; height:24px;
                    display:grid; place-items:center; border-radius:7px;
                    border:1px solid #ECE7F9; background:#FFFFFF;
                    color:#6B4BE8; font:inherit; font-size:16px;
                    line-height:1; cursor:pointer;
                    transition:background .14s, border-color .14s; }
    .rec-part-add:hover { background:#F7F5FE; border-color:#BCAEF0; }""",
     """    .rec-part-add { margin-left:auto; flex:none; width:24px; height:24px;
                    display:grid; place-items:center; border-radius:7px;
                    border:0; background:none; color:#A49CC0; font:inherit;
                    font-size:17px; line-height:1; cursor:pointer;
                    transition:background .14s, color .14s; }
    .rec-part-add:hover { background:#F4F2FB; color:#6B4BE8; }"""),
]

INVITE_JS = """    // the header's invite: open the role, add a line, put the cursor in it
    function invite_one() {
      if (!kept[2]) return;
      role.tab = 'role';
      role.team.push('');
      kept[2] = role_html();
      show_details(2, true);
      var face = flow.querySelector('.rec-flow-card');
      var box = face && face.querySelector('.rec-team-in[data-t="' +
        (role.team.length - 1) + '"]');
      if (box) box.focus();
    }

    // it has somewhere to point once the role exists
    function invite_ready() {
      var b = flow && flow.querySelector('[data-invite-top]');
      if (!b) return;
      b.hidden = !kept[2];
      // the headcount from the open register, where there is one. It was
      // in the section's empty state, which no longer exists.
      var n = b.querySelector('.rec-invite-n');
      if (n) n.textContent = (company && company.people) || '';
    }

"""

INVITE_ANCHOR = "    // the account screen's one action, defined where a reopen can find it"

SHOW_AT = [
    ("""          put_mini(2, 'Role details', role.title || 'as read', found.logo,
                   role_html());
          rail_draw();""",
     """          put_mini(2, 'Role details', role.title || 'as read', found.logo,
                   role_html());
          rail_draw();
          invite_ready();"""),

    ("""      rail_draw();
      at_step(last, true);""",
     """      rail_draw();
      invite_ready();
      at_step(last, true);"""),
]

CSS = """    .rec-flow-acts { display:inline-flex; align-items:center; gap:10px; }
    .rec-invite-top[hidden] { display:none; }
    .rec-invite-n { font-style:normal; font-weight:600; color:#A49CC0; }
    .rec-invite-n:not(:empty)::before { content:"\00b7"; margin:0 5px 0 2px;
                                        color:#CFC7E8; }
"""

CSS_ANCHOR = """    .rec-flow-cta { padding:9px 16px; border:0; border-radius:8px;"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-invite-top' not in s, path + ': already in the header'

    for old, new in EDITS + SHOW_AT:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    assert s.count(INVITE_ANCHOR) == 1, (path, 'invite', s.count(INVITE_ANCHOR))
    s = s.replace(INVITE_ANCHOR, INVITE_JS + INVITE_ANCHOR, 1)

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS + CSS_ANCHOR, 1)

    # the else branch of that ternary is now unreachable, and it carries
    # an em-dash, so it comes out by position rather than by match
    head = "              : '<p class=\"rec-part-say\">Whoever is interviewing"
    tail = "'.</p>') +"
    at = s.index(head)
    end = s.index(tail, at) + len(tail)
    s = s[:at] + "            ) +" + s[end:]

    assert 'Whoever is interviewing' not in s, path + ': the empty state survives'
    assert 'data-invite="1"' not in s, path + ': the second button survives'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
