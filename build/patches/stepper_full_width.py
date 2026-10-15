# -*- coding: utf-8 -*-
"""The steps move below the header and take the whole width.

In the header they were a third object competing with the logo and the
close for the same row, and they stayed as narrow as their own text. On
their own band under the progress line they get the full width, and the
connectors stretch to fill it instead of being two fixed 22px dashes.

The stretch is on the rules, not the steps: each step after the first
grows, and the rule inside it takes the slack, so the labels stay their
own size and only the space between them changes.
"""
import io
import sys

OLD_MARKUP = """          '<ol class="rec-steps">' +
            ['Company details', 'Job board', 'Account']
              .map(function (s, i) {
                return '<li class="rec-step"><i>' + (i + 1) + '</i>' +
                  '<b>' + s + '</b></li>';
              }).join('') +
          '</ol>' +
          '<button type="button" class="rec-flow-x" aria-label="Close">&#215;</button>' +
        '</div>' +
        '<div class="rec-flow-bar"><span></span></div>' +"""

NEW_MARKUP = """          '<button type="button" class="rec-flow-x" aria-label="Close">&#215;</button>' +
        '</div>' +
        '<div class="rec-flow-bar"><span></span></div>' +
        '<ol class="rec-steps">' +
          ['Company details', 'Job board', 'Account']
            .map(function (s, i) {
              return '<li class="rec-step"><i>' + (i + 1) + '</i>' +
                '<b>' + s + '</b></li>';
            }).join('') +
        '</ol>' +"""

OLD_CSS = """    .rec-steps { display:flex; align-items:center; gap:10px; margin:0;
                 padding:0; list-style:none; }
    .rec-step { display:flex; align-items:center; gap:7px; color:#A49CC0;
                font-size:12.5px; }
    .rec-step + .rec-step::before { content:""; width:22px; height:1px;
                                    background:#E2DCF4; margin-right:3px; }"""

NEW_CSS = """    .rec-steps { flex:none; display:flex; align-items:center; width:100%;
                 box-sizing:border-box; margin:0; list-style:none;
                 padding:15px clamp(18px, 3vw, 40px);
                 border-bottom:1px solid #F2EEFB; }
    .rec-step { display:flex; align-items:center; gap:8px; flex:none;
                color:#A49CC0; font-size:12.5px; }
    /* the rule takes the slack, so the labels keep their own size */
    .rec-step + .rec-step { flex:1; }
    .rec-step + .rec-step::before { content:""; flex:1; min-width:16px;
                                    height:1px; background:#E2DCF4;
                                    margin-right:8px; }"""

OLD_MQ = """    @media (max-width:760px) {
      .rec-step b { display:none; }
      .rec-steps { gap:6px; }
      .rec-step + .rec-step::before { width:14px; }
    }"""
NEW_MQ = """    @media (max-width:760px) {
      .rec-step b { display:none; }
      .rec-steps { padding:12px 18px; }
    }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in ((OLD_MARKUP, NEW_MARKUP), (OLD_CSS, NEW_CSS),
                     (OLD_MQ, NEW_MQ)):
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    # it must no longer be a child of the header row
    head = s[s.index("'<div class=\"rec-flow-head\">' +"):s.index("'<div class=\"rec-flow-bar\">")]
    assert 'rec-steps' not in head, path + ': still inside the header'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
