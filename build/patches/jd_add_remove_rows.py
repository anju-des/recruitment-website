# -*- coding: utf-8 -*-
"""Three questions and three rounds were a suggestion, not a limit.

A plus beside each heading adds one, and a cross on a row takes it
away. The cross stays out of sight until the row is pointed at or
focused, because it is destructive and there are six of them on the
screen; the plus is always there, because adding is the thing someone
is likely to want and a control you have to go looking for is not an
offer.

A new row is empty and takes focus, so the next thing typed goes into
it. Both redraw the whole screen from the same state everything else
reads, which keeps the rail's counts honest without telling them
anything.
"""
import io
import sys

EDITS = [
    # the headings gain a plus
    ("""            '<h3 class="rec-part-head">Screening questions</h3>' +""",
     """            '<h3 class="rec-part-head">Screening questions' +
              '<button type="button" class="rec-part-add" data-add="qs" ' +
                'aria-label="Add a question">+</button></h3>' +"""),

    ("""            '<h3 class="rec-part-head">Interview rounds</h3>' +""",
     """            '<h3 class="rec-part-head">Interview rounds' +
              '<button type="button" class="rec-part-add" data-add="rounds" ' +
                'aria-label="Add a round">+</button></h3>' +"""),

    # and every row a way out
    ("""                  '<textarea class="rec-q-in" rows="1" data-q="' + i + '">' +
                  esc(q) + '</textarea></li>';""",
     """                  '<textarea class="rec-q-in" rows="1" data-q="' + i + '">' +
                  esc(q) + '</textarea>' + row_x('qs', i) + '</li>';"""),

    ("""                    '<input class="rec-r-min" data-m="' + i + '" value="' +
                      esc(r.mins) + '" inputmode="numeric">min</span></li>';""",
     """                    '<input class="rec-r-min" data-m="' + i + '" value="' +
                      esc(r.mins) + '" inputmode="numeric">min</span>' +
                  row_x('rounds', i) + '</li>';"""),
]

ROW_X_JS = """    // the way out of a row, kept quiet until the row is pointed at
    function row_x(key, i) {
      return '<button type="button" class="rec-row-x" data-drop="' + key +
        '" data-i="' + i + '" aria-label="Remove this one">\\u00d7</button>';
    }

"""

ROW_X_ANCHOR = "    function role_row(r) {"

WIRE_JS = """
      // adding and removing redraw the screen from the same state the
      // rest of it reads, so nothing has to be told what changed
      function again(focus_k) {
        root.innerHTML = role_html();
        wire_role(root);
        kept[2] = role_html();
        rail_draw();
        remember();
        if (focus_k) {
          var box = root.querySelector(focus_k);
          if (box) box.focus();
        }
      }

      root.querySelectorAll('[data-add]').forEach(function (b) {
        b.addEventListener('click', function () {
          if (b.getAttribute('data-add') === 'qs') {
            role.questions.push('');
            again('.rec-q-in[data-q="' + (role.questions.length - 1) + '"]');
          } else {
            role.rounds.push({ say: '', mins: '30' });
            again('.rec-r-in[data-r="' + (role.rounds.length - 1) + '"]');
          }
        });
      });

      root.querySelectorAll('[data-drop]').forEach(function (b) {
        b.addEventListener('click', function () {
          var at = Number(b.getAttribute('data-i'));
          var list = b.getAttribute('data-drop') === 'qs'
            ? role.questions : role.rounds;
          list.splice(at, 1);
          again('');
        });
      });
"""

WIRE_ANCHOR = """      var see = root.querySelector('.rec-jd-see');"""

CSS = """    .rec-part-add { margin-left:auto; flex:none; width:24px; height:24px;
                    display:grid; place-items:center; border-radius:7px;
                    border:1px solid #ECE7F9; background:#FFFFFF;
                    color:#6B4BE8; font:inherit; font-size:16px;
                    line-height:1; cursor:pointer;
                    transition:background .14s, border-color .14s; }
    .rec-part-add:hover { background:#F7F5FE; border-color:#BCAEF0; }
    .rec-part-add:focus-visible { outline:2px solid #7C5CF6;
                                  outline-offset:2px; }
    /* destructive, and there are six of them: not until it is wanted */
    .rec-row-x { flex:none; width:22px; height:22px; margin:0 8px 0 0;
                 display:grid; place-items:center; border:0; border-radius:50%;
                 background:none; color:#A49CC0; font:inherit; font-size:15px;
                 line-height:1; cursor:pointer; opacity:0;
                 transition:opacity .14s, background .14s, color .14s; }
    .rec-qs .rec-row-x { margin-top:7px; }
    .rec-qs li:hover .rec-row-x, .rec-qs li:focus-within .rec-row-x,
    .rec-rounds li:hover .rec-row-x,
    .rec-rounds li:focus-within .rec-row-x { opacity:1; }
    .rec-row-x:hover { background:#FFF1F0; color:#B4443C; }
    .rec-row-x:focus-visible { opacity:1; outline:2px solid #7C5CF6;
                               outline-offset:1px; }
    @media (hover: none) {
      .rec-row-x { opacity:1; }
    }
"""

CSS_ANCHOR = """    .rec-part-say { margin:10px 0 0; font-size:12.5px; color:#9A93B8; }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-part-add' not in s, path + ': already addable'

    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    assert s.count(ROW_X_ANCHOR) == 1, (path, 'row_x', s.count(ROW_X_ANCHOR))
    s = s.replace(ROW_X_ANCHOR, ROW_X_JS + ROW_X_ANCHOR, 1)

    assert s.count(WIRE_ANCHOR) == 1, (path, 'wire', s.count(WIRE_ANCHOR))
    s = s.replace(WIRE_ANCHOR, WIRE_JS + '\n' + WIRE_ANCHOR, 1)

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS_ANCHOR + '\n' + CSS, 1)

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
