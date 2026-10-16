# -*- coding: utf-8 -*-
"""The rail shows what each step made, not just that it finished.

A card saying "Job board" is a receipt. The address it was given, and
the role standing on it, are the thing itself -- and once they are in
the rail the whole run can be read down the left without opening
anything.

So each step keeps its card and gains a short list under it: the board
with its address and its roles, the role with its rounds and how long
each one is. A count sits beside the label, because the count is the
part that changes as someone edits.

Every row opens the screen it came from, the same as the card above it.
Nothing here is a second way to edit -- it is the same thing seen from
outside, so it re-renders from the same state whenever that state
changes.

The rail is wider for it, and below 860px, where the rail lies down
across the top, the lists are hidden rather than wrapped: a horizontal
strip is no place to read a list.
"""
import io
import sys

RAIL_JS = r"""    // ---- what a step made, under that step --------------------------

    // rows: [{ n, say, end }]. `n` is the small leading mark, `end` the
    // figure on the right, both optional.
    function rail_set(i, label, count, rows) {
      var step = flow.querySelectorAll('.rec-step')[i];
      if (!step) return;
      var set = step.querySelector('.rec-rail-set');
      if (!rows || !rows.length) { if (set) set.remove(); return; }
      if (!set) {
        set = document.createElement('div');
        set.className = 'rec-rail-set';
        step.appendChild(set);
      }
      set.innerHTML =
        '<p class="rec-rail-head">' + esc(label) +
          (count ? '<b>' + esc(String(count)) + '</b>' : '') + '</p>' +
        '<ul class="rec-rail-rows">' +
          rows.map(function (r) {
            return '<li><button type="button" class="rec-rail-row">' +
              (r.n ? '<i>' + esc(r.n) + '</i>' : '') +
              '<span>' + esc(r.say) + '</span>' +
              (r.end ? '<em>' + esc(r.end) + '</em>' : '') +
              '</button></li>';
          }).join('') +
        '</ul>';
      set.querySelectorAll('.rec-rail-row').forEach(function (b) {
        b.addEventListener('click', function () {
          show_details(i, open_i !== i);
        });
      });
    }

    // the rail reads off the same state the screens do
    function rail_draw() {
      if (!flow) return;
      if (kept[1]) {
        var said = (role.title || (brief.role || '').split(',')[0] || '')
          .trim();
        rail_set(1, 'Board', said ? '1 role' : '', [
          { say: board_addr(company.who || found_who()), end: 'live' }
        ].concat(said ? [{ say: said }] : []));
      }
      if (kept[2] && role.rounds && role.rounds.length) {
        rail_set(2, 'Rounds', role.rounds.length,
          role.rounds.map(function (r, n) {
            return { n: String(n + 1), say: r.say,
                     end: r.mins ? r.mins + 'm' : '' };
          }));
      }
    }

    // the company's name, wherever this run keeps it
    function found_who() {
      return (company && company.who) || '';
    }

"""

RAIL_CSS = """    /* what a step made, listed under it */
    .rec-rail-set { width:100%; margin:8px 0 0 30px; padding-right:8px;
                    box-sizing:border-box;
                    animation:rec-mini-in .3s ease both; }
    .rec-rail-head { display:flex; align-items:center; gap:7px; margin:0 0 5px;
                     font-size:10px; font-weight:700; letter-spacing:.09em;
                     text-transform:uppercase; color:#A49CC0; }
    .rec-rail-head b { font-weight:700; color:#6B4BE8; }
    .rec-rail-rows { margin:0; padding:0; list-style:none;
                     display:flex; flex-direction:column; gap:3px; }
    .rec-rail-row { display:flex; align-items:center; gap:8px; width:100%;
                    padding:6px 9px; border:1px solid transparent;
                    border-radius:9px; background:none; font:inherit;
                    text-align:left; cursor:pointer;
                    transition:background .14s, border-color .14s; }
    .rec-rail-row:hover { background:#FFFFFF; border-color:#ECE7F9; }
    .rec-rail-row:focus-visible { outline:2px solid #7C5CF6;
                                  outline-offset:1px; }
    .rec-rail-row i { flex:none; width:15px; height:15px; border-radius:4px;
                      display:grid; place-items:center; background:#EFEBFC;
                      color:#7C5CF6; font-style:normal; font-size:9.5px;
                      font-weight:700; }
    .rec-rail-row span { flex:1; min-width:0; font-size:12px;
                         color:#4E4766; white-space:nowrap;
                         overflow:hidden; text-overflow:ellipsis; }
    .rec-rail-row em { flex:none; font-style:normal; font-size:11px;
                       color:#A49CC0; }
    @media (prefers-reduced-motion: reduce) {
      .rec-rail-set { animation:none; }
    }
"""

CSS_ANCHOR = """    .rec-done-slot { display:block; max-width:100%; }"""

# the rail has more to hold now
WIDTH_OLD = "list-style:none; width:clamp(200px, 22vw, 250px);"
WIDTH_NEW = "list-style:none; width:clamp(230px, 24vw, 292px);"

# lying down across the top, it is no place for a list
NARROW_OLD = """      .rec-done-card { margin:0 0 0 10px; }"""
NARROW_NEW = """      .rec-done-card { margin:0 0 0 10px; }
      .rec-rail-set { display:none; }"""

# --- where it gets drawn ---------------------------------------------

DRAW_AT = [
    # when the board's card is filed
    ("""            put_mini(1, 'Job board', board_addr(found.who),
                     found.logo, card.innerHTML);
            remember();""",
     """            put_mini(1, 'Job board', board_addr(found.who),
                     found.logo, card.innerHTML);
            rail_draw();
            remember();"""),

    # when the role screen is finished
    ("""          put_mini(2, 'Role details', role.title || 'as read', found.logo,
                   role_html());""",
     """          put_mini(2, 'Role details', role.title || 'as read', found.logo,
                   role_html());
          rail_draw();"""),

    # and whenever anything on it is edited
    ("""      function kept_again() { kept[2] = role_html(); remember(); }""",
     """      function kept_again() {
        kept[2] = role_html();
        rail_draw();
        remember();
      }"""),

    ("""            retitle_board(said || 'Your first role');""",
     """            retitle_board(said || 'Your first role');
            rail_draw();"""),

    # a refresh brings back the rail with everything else
    ("""      at_step(last, true);""",
     """      if (was.rounds) role.rounds = was.rounds;
      if (was.role) role.title = String(was.role).split(',')[0].trim();
      rail_draw();
      at_step(last, true);"""),
]

# the record carries what the rail needs to come back
REMEMBER = ("""          who: company.who, logo: company.logo, based: company.based || '',""",
            """          who: company.who, logo: company.logo, based: company.based || '',
          rounds: role.rounds,""")


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-rail-set' not in s, path + ': already listed'

    mark = "    // what a finished step leaves behind, under that step\n"
    assert s.count(mark) == 1, (path, 'rail anchor', s.count(mark))
    s = s.replace(mark, RAIL_JS + mark, 1)

    for old, new in DRAW_AT + [REMEMBER]:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    assert s.count(WIDTH_OLD) == 1, (path, 'width', s.count(WIDTH_OLD))
    s = s.replace(WIDTH_OLD, WIDTH_NEW, 1)

    assert s.count(NARROW_OLD) == 1, (path, 'narrow', s.count(NARROW_OLD))
    s = s.replace(NARROW_OLD, NARROW_NEW, 1)

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS_ANCHOR + '\n' + RAIL_CSS, 1)

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
