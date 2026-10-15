# -*- coding: utf-8 -*-
"""A wider company card, with the badge inside it.

The card was shrink-to-fit, so it was as wide as the company's name
happened to be -- "Stripe" made a small card and a longer name a bigger
one, which read as inconsistency rather than as fit. It is a fixed
420px now, centred, so every company gets the same object.

"Found" moves into the card and sits at its right edge, which is what
the extra width is for.
"""
import io
import sys

OLD_MARKUP = """              '<span class="rec-flow-found-say"><b>' + esc(who) + '</b>' +
                '<i>' + esc(site) + '</i></span>' +
            '</div>' +"""
NEW_MARKUP = """              '<span class="rec-flow-found-say"><b>' + esc(who) + '</b>' +
                '<i>' + esc(site) + '</i></span>' +
              '<span class="rec-flow-found-badge">Found</span>' +
            '</div>' +"""

OLD_CSS = """    .rec-flow-found { display:inline-flex; align-items:center; gap:13px;
                      margin-top:24px; padding:14px 20px 14px 14px;
                      border:1px solid #E7E2F6; border-radius:16px;
                      background:#FFFFFF; text-align:left; }"""
NEW_CSS = """    .rec-flow-found { display:flex; align-items:center; gap:13px;
                      width:min(420px, 100%); box-sizing:border-box;
                      margin:24px auto 0; padding:14px 18px 14px 14px;
                      border:1px solid #E7E2F6; border-radius:16px;
                      background:#FFFFFF; text-align:left; }
    .rec-flow-found-badge { margin-left:auto; flex:none; padding:5px 11px;
                            border-radius:100px; background:#F1EDFE;
                            color:#5A4BD8; font-size:11px; font-weight:700;
                            letter-spacing:.07em; text-transform:uppercase; }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-flow-found-badge' not in s, path + ': already badged'
    for old, new in ((OLD_MARKUP, NEW_MARKUP), (OLD_CSS, NEW_CSS)):
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
