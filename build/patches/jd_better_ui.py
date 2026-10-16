# -*- coding: utf-8 -*-
"""A screen taller than the window, and questions that read as writing.

Two things, both from the same screen getting long.

The scroll: the body centred its card with align-items:center. A flex
item taller than its container overflows at both ends, and the part
above the top cannot be reached -- scrollTop does not go negative. So
the heading was simply gone. Auto margins centre the same way and give
that up as soon as the item is too tall, which is exactly the
behaviour wanted. The card starts at the top and all of it scrolls.

The questions: three identical boxes with empty space under the text
read as a form to fill in, when they are Mira's writing offered for
correction. They read as writing now -- no border until you touch one,
and each box the height of what it holds, measured after every change
rather than guessed from a character count.

The rounds get the same treatment, since they are the same kind of
thing: a name you might change, not a field you must complete.
"""
import io
import sys

CSS_EDITS = [
    # the scroll
    ("""    .rec-flow-body { flex:1; min-height:0; overflow:auto;
                     display:flex; align-items:center; justify-content:center;
                     padding:clamp(24px, 4vw, 56px) clamp(18px, 3vw, 40px); }
    .rec-flow-card { width:min(680px, 100%); }""",
     """    /* not align-items:center -- a flex item taller than its container
       overflows both ends and the top of it cannot be scrolled to. An auto
       margin centres the same way and stops as soon as it does not fit. */
    .rec-flow-body { flex:1; min-height:0; overflow:auto;
                     display:flex; align-items:flex-start;
                     justify-content:flex-start;
                     padding:clamp(24px, 4vw, 56px) clamp(18px, 3vw, 40px); }
    .rec-flow-card { width:min(680px, 100%); margin:auto; }"""),

    # the questions
    ("""    .rec-qs li, .rec-rounds li { display:flex; align-items:flex-start;
                                 gap:11px; }
    .rec-qs b, .rec-rounds b { flex:none; width:22px; height:22px;
                               margin-top:5px; border-radius:50%;
                               display:grid; place-items:center;
                               background:#F1EEFA; color:#6B4BE8;
                               font-size:11px; font-weight:700; }
    .rec-q-in { flex:1; min-width:0; resize:vertical; overflow-x:hidden;
                border:1px solid #ECE7F9;
                border-radius:10px; padding:9px 12px; background:#FFFFFF;
                font:inherit; font-size:14px; line-height:1.45;
                color:#2A2440; outline:none; }
    .rec-q-in:focus { border-color:#7C5CF6; background:#FCFBFF; }
    .rec-rounds li { align-items:center; }
    .rec-rounds b { margin-top:0; }
    .rec-r-in { flex:1; min-width:0; border:1px solid #ECE7F9;
                border-radius:10px; padding:9px 12px; background:#FFFFFF;
                font:inherit; font-size:14px; font-weight:600; color:#1A1430;
                outline:none; }
    .rec-r-in:focus { border-color:#7C5CF6; background:#FCFBFF; }
    .rec-r-mins { flex:none; display:inline-flex; align-items:center; gap:4px;
                  font-size:12.5px; color:#9A93B8; }
    .rec-r-min { width:38px; border:1px solid #ECE7F9; border-radius:8px;
                 padding:7px 6px; background:#FFFFFF; font:inherit;
                 font-size:13px; font-weight:600; color:#1A1430;
                 text-align:center; outline:none; }
    .rec-r-min:focus { border-color:#7C5CF6; }""",

     """    .rec-qs li, .rec-rounds li { display:flex; align-items:flex-start;
                                 gap:12px; border-radius:10px;
                                 transition:background .14s; }
    .rec-qs li:hover, .rec-rounds li:hover { background:#FAF9FE; }
    .rec-qs li:focus-within, .rec-rounds li:focus-within {
      background:#F7F5FE; }
    .rec-qs b, .rec-rounds b { flex:none; width:20px; height:20px;
                               margin:9px 0 0 8px; border-radius:50%;
                               display:grid; place-items:center;
                               background:#EFEBFC; color:#7C5CF6;
                               font-size:10.5px; font-weight:700; }
    /* writing, not a form: no border until it is being changed */
    .rec-q-in { flex:1; min-width:0; resize:none; overflow:hidden;
                border:1px solid transparent; border-radius:9px;
                padding:8px 10px 8px 0; margin-right:8px; background:none;
                font:inherit; font-size:14.5px; line-height:1.5;
                color:#2A2440; outline:none; }
    .rec-q-in:focus { border-color:#D8CFF8; background:#FFFFFF;
                      padding-left:10px; margin-right:8px; }
    .rec-rounds li { align-items:center; }
    .rec-rounds b { margin:0 0 0 8px; }
    .rec-r-in { flex:1; min-width:0; border:1px solid transparent;
                border-radius:9px; padding:10px 10px 10px 0; background:none;
                font:inherit; font-size:14.5px; font-weight:600;
                color:#1A1430; outline:none; }
    .rec-r-in:focus { border-color:#D8CFF8; background:#FFFFFF;
                      padding-left:10px; }
    .rec-r-mins { flex:none; display:inline-flex; align-items:baseline;
                  gap:3px; margin-right:10px; font-size:12px;
                  color:#A49CC0; }
    .rec-r-min { width:30px; border:0; border-bottom:1px solid transparent;
                 padding:2px 0; background:none; font:inherit;
                 font-size:14px; font-weight:600; color:#1A1430;
                 text-align:right; outline:none; }
    .rec-r-min:hover { border-bottom-color:#E7E2F6; }
    .rec-r-min:focus { border-bottom-color:#7C5CF6; }"""),
]

# a box the height of what it holds, measured rather than guessed
GROW_JS = """
      // a textarea does not size itself: measure after every change.
      // Measured twice -- once now, once after the next frame -- because
      // a measurement taken before the text has been laid out comes back
      // wrong, and a box kept to a sane height even then.
      function grow(box) {
        function fit() {
          box.style.height = 'auto';
          var h = box.scrollHeight + 2;
          box.style.height = (h > 10 && h < 400 ? h : 64) + 'px';
        }
        fit();
        if (window.requestAnimationFrame) window.requestAnimationFrame(fit);
      }
      root.querySelectorAll('.rec-q-in').forEach(function (box) {
        grow(box);
        box.addEventListener('input', function () { grow(box); });
      });
"""

GROW_ANCHOR = """      root.querySelectorAll('.rec-q-in').forEach(function (box) {
        box.addEventListener('input', function () {
          role.questions[Number(box.getAttribute('data-q'))] = box.value;
          kept_again();
        });
      });"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'function grow(box)' not in s, path + ': already grows'

    for old, new in CSS_EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    assert s.count(GROW_ANCHOR) == 1, (path, 'grow', s.count(GROW_ANCHOR))
    s = s.replace(GROW_ANCHOR, GROW_ANCHOR + GROW_JS, 1)

    # the row count was a guess at the height; the measurement replaces it
    old = """                  // a long question gets the line it needs, not a scrollbar
                  '<textarea class="rec-q-in" rows="' +
                    (q.length > 86 ? 3 : 2) + '" data-q="' + i + '">' +"""
    new = """                  // one row to start: grow() sizes it to its contents
                  '<textarea class="rec-q-in" rows="1" data-q="' + i + '">' +"""
    assert s.count(old) == 1, (path, 'rows', s.count(old))
    s = s.replace(old, new, 1)

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
