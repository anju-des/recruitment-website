# -*- coding: utf-8 -*-
"""The steps stand up and move to the left.

A rail down the side rather than a band across the top. The content sits
beside it, so "under step one" becomes "next to step one", which is what
a vertical stepper means by the same thing.

The connector changes axis with it: horizontally it was a flex child
taking the slack between labels, and vertically it is an absolute 1px
line at the circle's centre, spanning exactly the gap between two
circles. Those are different enough that the rule is rewritten rather
than nudged.

Below 860px the rail lies back down. A 220px column off the side of a
phone leaves nothing for the content, and the horizontal arrangement
already worked there.
"""
import io
import sys

OLD_MARKUP = """        '<div class="rec-flow-sand" aria-hidden="true"></div>' +
        '<ol class="rec-steps">' +
          ['Company details', 'Job board', 'Account']
            .map(function (s, i) {
              return '<li class="rec-step"><i>' + (i + 1) + '</i>' +
                '<b>' + s + '</b></li>';
            }).join('') +
        '</ol>' +
        '<div class="rec-flow-body"><div class="rec-flow-card"></div></div>';"""

NEW_MARKUP = """        '<div class="rec-flow-sand" aria-hidden="true"></div>' +
        '<div class="rec-flow-main">' +
          '<ol class="rec-steps">' +
            ['Company details', 'Job board', 'Account']
              .map(function (s, i) {
                return '<li class="rec-step"><i>' + (i + 1) + '</i>' +
                  '<b>' + s + '</b></li>';
              }).join('') +
          '</ol>' +
          '<div class="rec-flow-body"><div class="rec-flow-card"></div></div>' +
        '</div>';"""

OLD_CSS_HEAD = """    /* the three steps, in the header */
    .rec-steps { flex:none; display:flex; align-items:center; width:100%;
                 box-sizing:border-box; margin:0; list-style:none;
                 padding:15px clamp(18px, 3vw, 40px);
                 /* the sand is positioned and this row was not, so without
                    a layer of its own the gradient paints over the text */
                 position:relative; z-index:1; }
    .rec-step { display:flex; align-items:center; gap:8px; flex:none;
                color:#A49CC0; font-size:12.5px; }
    /* the rule takes the slack, so the labels keep their own size */
    .rec-step + .rec-step { flex:1; }
    .rec-step + .rec-step::before { content:""; flex:1; min-width:16px;
                                    height:1px; background:#E2DCF4;
                                    margin-right:8px; }"""

NEW_CSS_HEAD = """    /* the three steps, as a rail down the left */
    .rec-flow-main { flex:1; min-height:0; display:flex; }
    .rec-steps { flex:none; display:flex; flex-direction:column;
                 align-items:flex-start; box-sizing:border-box; margin:0;
                 list-style:none; width:clamp(200px, 22vw, 250px);
                 padding:clamp(22px, 3vw, 34px) clamp(18px, 2.4vw, 32px);
                 /* the sand is positioned and this was not, so without a
                    layer of its own the gradient paints over the text */
                 position:relative; z-index:1; }
    .rec-step { position:relative; display:flex; align-items:center;
                gap:10px; padding:14px 0; color:#A49CC0; font-size:12.5px; }
    /* a line from the circle above to this one, at the circle's centre */
    .rec-step + .rec-step::before { content:""; position:absolute;
                                    left:9.5px; top:-14px; width:1px;
                                    height:28px; background:#E2DCF4; }"""

OLD_MQ = """    @media (max-width:760px) {
      .rec-step b { display:none; }
      .rec-steps { padding:12px 18px; }
    }"""

NEW_MQ = """    /* a 220px column off the side of a phone leaves nothing for the
       content, so the rail lies back down */
    @media (max-width:860px) {
      .rec-flow-main { flex-direction:column; }
      .rec-steps { width:100%; flex-direction:row; align-items:center;
                   padding:12px 18px; }
      .rec-step { padding:0; flex:none; }
      .rec-step b { display:none; }
      .rec-step + .rec-step { flex:1; }
      .rec-step + .rec-step::before { position:static; flex:1; width:auto;
                                      min-width:14px; height:1px;
                                      margin-right:8px; }
    }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-flow-main' not in s, path + ': already a rail'
    for old, new in ((OLD_MARKUP, NEW_MARKUP), (OLD_CSS_HEAD, NEW_CSS_HEAD),
                     (OLD_MQ, NEW_MQ)):
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
