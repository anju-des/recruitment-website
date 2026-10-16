# -*- coding: utf-8 -*-
"""The job description is a tab, not a link in a sentence.

It was a link buried in the subcopy, which is the hardest place on a
screen to find anything, and it opened a sheet over the top of
everything. Two tabs instead: what Mira drafted, and what it was
drafted from, side by side at the top where the eye starts.

The sheet goes. One way to read the document is enough, and the tab is
the better one -- it keeps the screen and does not have to be
dismissed. The row in the panel that used to open the sheet switches to
the tab now, so everything agrees.

The sign-in stays under both, because it is the point of the screen
either way.
"""
import io
import sys

EDITS = [
    # which tab is showing
    ("""                 pay_refs: [], questions: [], rounds: [], team: [] };""",
     """                 pay_refs: [], questions: [], rounds: [], team: [],
                 tab: 'role' };"""),

    # the subcopy keeps the sentence and loses the link
    ("""          (jd ? ' <button type="button" class="rec-jd-see">View the job ' +
                'description</button>' : '') +
        '</p>' +""",
     """        '</p>' +
        (at >= 3 && jd
          ? '<div class="rec-tabs" role="tablist">' +
              [['role', 'Role details'], ['jd', 'Job description']]
                .map(function (t) {
                  return '<button type="button" class="rec-tab' +
                    (role.tab === t[0] ? ' is-on' : '') + '" role="tab" ' +
                    'aria-selected="' + (role.tab === t[0]) + '" ' +
                    'data-tab="' + t[0] + '">' + esc(t[1]) + '</button>';
                }).join('') +
            '</div>'
          : '') +"""),

    # the document, where the sections would be
    ("""        '<div class="rec-found-card">' +
          '<div class="rec-role">' +""",
     """        '<div class="rec-found-card">' +
          (role.tab === 'jd' && jd ? jd_panel() : '') +
          (role.tab === 'jd' && jd ? '' :
          '<div class="rec-role">' +"""),

    ("""            ROLE_ROWS.slice(2).map(role_row).join('') +
          '</div>' +""",
     """            ROLE_ROWS.slice(2).map(role_row).join('') +
          '</div>') +"""),

    # the parts only belong to the first tab
    ("""          (at >= 1 ?
          '<div class="rec-part">' +
            '<h3 class="rec-part-head">Screening questions' +""",
     """          (at >= 1 && role.tab === 'role' ?
          '<div class="rec-part">' +
            '<h3 class="rec-part-head">Screening questions' +"""),

    ("""          (at >= 2 ?
          '<div class="rec-part">' +
            '<h3 class="rec-part-head">Interview rounds' +""",
     """          (at >= 2 && role.tab === 'role' ?
          '<div class="rec-part">' +
            '<h3 class="rec-part-head">Interview rounds' +"""),

    ("""          (at >= 3 ?
          '<div class="rec-part">' +
            '<h3 class="rec-part-head">Pay</h3>' +""",
     """          (at >= 3 && role.tab === 'role' ?
          '<div class="rec-part">' +
            '<h3 class="rec-part-head">Pay</h3>' +"""),

    ("""          (at >= 3 ?
          '<div class="rec-part">' +
            '<h3 class="rec-part-head">Hiring team' +""",
     """          (at >= 3 && role.tab === 'role' ?
          '<div class="rec-part">' +
            '<h3 class="rec-part-head">Hiring team' +"""),

    # the panel's own row switches tabs rather than opening a sheet
    ("""      rail_set(2, 'jd', 'Job description', '', jd
        ? [{ say: jd_name || 'The job description', end: 'open',
             go: show_jd }]
        : []);""",
     """      rail_set(2, 'jd', 'Job description', '', jd
        ? [{ say: jd_name || 'The job description', end: 'read',
             go: function () {
               role.tab = 'jd';
               kept[2] = role_html();
               show_details(2, true);
             } }]
        : []);"""),

    # and the tabs are wired like everything else on this screen
    ("""      root.querySelectorAll('[data-invite]').forEach(function (b) {""",
     """      root.querySelectorAll('[data-tab]').forEach(function (b) {
        b.addEventListener('click', function () {
          role.tab = b.getAttribute('data-tab');
          again('');
        });
      });

      root.querySelectorAll('[data-invite]').forEach(function (b) {"""),
]

PANEL_JS = """    // the document itself, under the second tab
    function jd_panel() {
      var link = '';
      if (jd_file) {
        if (!jd_url) jd_url = window.URL.createObjectURL(jd_file);
        link = '<a class="rec-jd-open" href="' + esc(jd_url) + '" ' +
          'target="_blank" rel="noopener">Open the original</a>';
      }
      return '<div class="rec-jd-panel">' +
        '<p class="rec-jd-name"><b>' + esc(jd_name || 'The job ' +
          'description') + '</b>' + link + '</p>' +
        '<pre class="rec-jd-text">' + esc(jd.text || '') + '</pre>' +
      '</div>';
    }

"""

PANEL_ANCHOR = "    function role_row(r) {"

CSS = """    .rec-tabs { display:flex; gap:4px; margin:18px 0 0;
                border-bottom:1px solid #EDE9F8; }
    .rec-tab { position:relative; padding:9px 14px; border:0;
               background:none; font:inherit; font-size:13.5px;
               font-weight:600; color:#8A82A8; cursor:pointer;
               transition:color .14s; }
    .rec-tab:hover { color:#4E4766; }
    .rec-tab.is-on { color:#1A1430; }
    .rec-tab.is-on::after { content:""; position:absolute; left:10px;
                            right:10px; bottom:-1px; height:2px;
                            border-radius:2px; background:#7C5CF6; }
    .rec-tab:focus-visible { outline:2px solid #7C5CF6; outline-offset:-2px;
                             border-radius:8px; }
    .rec-jd-panel { display:flex; flex-direction:column; gap:10px; }
    .rec-jd-name { display:flex; align-items:baseline; gap:12px; margin:0; }
    .rec-jd-name b { flex:1; min-width:0; font-size:13px; color:#1A1430;
                     overflow:hidden; text-overflow:ellipsis;
                     white-space:nowrap; }
    .rec-jd-open { flex:none; font-size:12.5px; color:#6B4BE8;
                   text-decoration:underline; text-underline-offset:3px; }
    .rec-jd-text { margin:0; max-height:52vh; overflow:auto; font:inherit;
                   font-size:13px; line-height:1.65; color:#3A3356;
                   white-space:pre-wrap; word-break:break-word; }
"""

CSS_ANCHOR = """    .rec-invite { margin-left:auto; flex:none; display:inline-flex;"""

# the sheet, and everything that was only for it
DEAD_JS_HEAD = "    // the document all of this was read out of, kept one click away"
DEAD_JS_TAIL = "    // ---- what a step made, under that step"

DEAD_CSS = [
    "    .rec-jd-see { border:0; padding:0 0 1px; background:none; font:inherit;",
    "    /* the document itself */",
]

# the sheet's one line of wiring, inside wire_role
DEAD_WIRE = """      var see = root.querySelector('.rec-jd-see');
      if (see) see.addEventListener('click', show_jd);
"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-tabs' not in s, path + ': already tabbed'

    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    assert s.count(PANEL_ANCHOR) == 1, (path, 'panel', s.count(PANEL_ANCHOR))
    s = s.replace(PANEL_ANCHOR, PANEL_JS + PANEL_ANCHOR, 1)

    # the url the panel hands out, made once
    old = "    var jd_file = null;"
    new = "    var jd_url = '';          // the original, once, for the link\n" \
          "    var jd_file = null;"
    assert s.count(old) == 1, (path, 'jd_url', s.count(old))
    s = s.replace(old, new, 1)

    # a new file is a new url
    old = """        jd_file = file;
        jd_name = file.name || '';"""
    new = """        if (jd_url) { window.URL.revokeObjectURL(jd_url); jd_url = ''; }
        jd_file = file;
        jd_name = file.name || '';"""
    assert s.count(old) == 1, (path, 'revoke', s.count(old))
    s = s.replace(old, new, 1)

    # out with the sheet
    at = s.index(DEAD_JS_HEAD)
    end = s.index(DEAD_JS_TAIL, at)
    s = s[:at] + s[end:]

    assert s.count(DEAD_WIRE) == 1, (path, 'sheet wiring', s.count(DEAD_WIRE))
    s = s.replace(DEAD_WIRE, '', 1)

    for dead in DEAD_CSS:
        at = s.index(dead)
        end = s.index('\n\n', at)
        s = s[:at] + s[end + 1:]

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS + CSS_ANCHOR, 1)

    for gone in ['show_jd', 'rec-jd-ov', 'rec-jd-sheet', 'rec-jd-see']:
        assert gone not in s, (path, gone + ' survives')

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
