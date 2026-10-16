# -*- coding: utf-8 -*-
"""Headings say what the section is, and work mode shows the answer.

The grey half-sentences beside each heading explained what was already
obvious from the thing underneath them. The one on Pay was carrying
something real -- where the figure came from -- but the note under the
figure says that in full, so nothing is lost by dropping all three.

And work mode was three buttons where the other rows show one value.
It shows the chosen one, and the other two appear when it is pressed:
the answer at rest, the choice when you want it. With nothing chosen
yet there is nothing to collapse to, so all three stay out.
"""
import io
import sys

EDITS = [
    ("""            '<h3 class="rec-part-head">Screening questions' +
              '<span>asked before anyone reaches you</span></h3>' +""",
     """            '<h3 class="rec-part-head">Screening questions</h3>' +"""),

    ("""            '<h3 class="rec-part-head">Interview rounds' +
              '<span>' + esc(family(role.title) === 'any'
                ? 'a standard three' : 'typical for this kind of role') +
              '</span></h3>' +""",
     """            '<h3 class="rec-part-head">Interview rounds</h3>' +"""),

    ("""            '<h3 class="rec-part-head">Pay' +
              '<span>' + (role.pay_from === 'said'
                ? 'as the job description states it'
                : role.pay_from === 'market'
                  ? 'the job description does not say, so: the market'
                  : 'the job description does not say') + '</span></h3>' +""",
     """            '<h3 class="rec-part-head">Pay</h3>' +"""),

    # one chip at rest, three when it is pressed
    ("""            '<div class="rec-role-row"><i>Work mode</i>' +
              '<span class="rec-role-pick">' +
                MODES.map(function (m) {
                  return '<button type="button" data-mode="' + esc(m) + '"' +
                    (role.mode === m ? ' class="is-on"' : '') + '>' +
                    esc(m) + '</button>';
                }).join('') +
              '</span></div>' +""",
     """            '<div class="rec-role-row"><i>Work mode</i>' +
              '<span class="rec-role-pick' +
                (role.mode ? ' is-picked' : '') + '">' +
                MODES.map(function (m) {
                  return '<button type="button" data-mode="' + esc(m) + '"' +
                    (role.mode === m ? ' class="is-on"' : '') + '>' +
                    esc(m) + '</button>';
                }).join('') +
              '</span></div>' +"""),

    # pressing the chosen one offers the others; choosing puts them away
    ("""      root.querySelectorAll('[data-mode]').forEach(function (b) {
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
      });""",
     """      var pick = root.querySelector('.rec-role-pick');
      root.querySelectorAll('[data-mode]').forEach(function (b) {
        b.addEventListener('click', function () {
          var mine = b.getAttribute('data-mode');
          // the chosen one, pressed while alone: show the others
          if (pick && role.mode === mine &&
              !pick.classList.contains('is-open')) {
            pick.classList.add('is-open');
            return;
          }
          role.mode = mine;
          if (pick) {
            pick.classList.remove('is-open');
            pick.classList.add('is-picked');
          }
          root.querySelectorAll('[data-mode]').forEach(function (o) {
            o.classList.toggle('is-on',
              o.getAttribute('data-mode') === role.mode);
          });
          kept_again();
        });
      });"""),
]

CSS = """    /* the answer at rest; the choice when it is asked for */
    .rec-role-pick.is-picked button { display:none; }
    .rec-role-pick.is-picked button.is-on,
    .rec-role-pick.is-picked.is-open button { display:inline-block; }
    .rec-role-pick.is-picked:not(.is-open) button.is-on::after {
      content:""; display:inline-block; width:5px; height:5px;
      margin:0 0 1px 7px; border-right:1.5px solid currentColor;
      border-bottom:1.5px solid currentColor; transform:rotate(45deg);
      opacity:.65; }
"""

CSS_ANCHOR = """    .rec-role-pick button:focus-visible { outline:2px solid #7C5CF6;
                                          outline-offset:2px; }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'is-picked' not in s, path + ': already quiet'

    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS_ANCHOR + '\n' + CSS, 1)

    assert '.rec-part-head span' in s, (path, 'the span style can go too')
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
