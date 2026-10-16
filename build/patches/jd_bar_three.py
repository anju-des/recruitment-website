# -*- coding: utf-8 -*-
"""The bar is three segments, because the flow is three steps.

One sliding fill said "some fraction of the way" and left you to work
out of what. Three segments say which step you are in and how many are
left, which is the question anyone looking at a progress bar is asking.

It is driven from at_step, which already works out, for every step,
whether it is finished, current, or still ahead -- so the bar and the
rail can never disagree about where the flow is. The four places that
used to push a percentage at it are gone; they were each a chance for
the two to drift.

The current segment keeps a slow sweep across it, so a step that is
waiting on the network looks like it is waiting rather than stuck.
"""
import io
import sys

MARKUP_OLD = """        '<div class="rec-flow-bar"><span></span></div>' +"""
MARKUP_NEW = """        '<div class="rec-flow-bar" aria-hidden="true">' +
          '<i></i><i></i><i></i></div>' +"""

CSS_OLD = """    .rec-flow-bar { flex:none; height:3px; background:#EFECF9; }
    .rec-flow-bar span { display:block; height:100%; background:#7C5CF6;
                         width:var(--at, 25%); transition:width .25s ease; }"""

CSS_NEW = """    .rec-flow-bar { flex:none; display:flex; gap:3px; height:3px;
                    padding:0 3px; background:transparent; }
    .rec-flow-bar i { flex:1; position:relative; overflow:hidden;
                      border-radius:2px; background:#EFECF9;
                      transition:background .25s ease; }
    .rec-flow-bar i.is-done { background:#7C5CF6; }
    /* the step being worked on: a sweep, so waiting looks like waiting */
    .rec-flow-bar i.is-now::after { content:""; position:absolute; inset:0;
                                    border-radius:2px;
                                    background:linear-gradient(90deg,
                                      rgba(124,92,246,0) 0%,
                                      rgba(124,92,246,.95) 50%,
                                      rgba(124,92,246,0) 100%);
                                    animation:rec-bar-sweep 1.5s ease-in-out
                                              infinite; }
    @keyframes rec-bar-sweep { from { transform:translateX(-100%); }
                               to { transform:translateX(100%); } }"""

MOTION_OLD = """      .rec-flow-bar span { transition:none; }"""
MOTION_NEW = """      .rec-flow-bar i { transition:none; }
      .rec-flow-bar i.is-now::after { animation:none; opacity:.55; }"""

# at_step already knows, for every step, which of the three it is
STEP_OLD = """        var mark = all[k].querySelector('i');
        mark.textContent = over ? '\\u2713' : String(k + 1);
      }
    }"""

STEP_NEW = """        var mark = all[k].querySelector('i');
        mark.textContent = over ? '\\u2713' : String(k + 1);
      }
      // the bar is the same answer, drawn along the top
      var segs = flow.querySelectorAll('.rec-flow-bar i');
      for (var n = 0; n < segs.length; n++) {
        segs[n].classList.toggle('is-done', n < i || (n === i && done));
        segs[n].classList.toggle('is-now', n === i && !done);
      }
    }"""

# and the places that pushed a percentage at it
DEAD = [
    """      var total = STEPS.length + 1;
      flow.querySelector('.rec-flow-bar span').style.setProperty(
        '--at', Math.round(Math.min(at + 1, total) / total * 100) + '%');
""",
    """          flow.querySelector('.rec-flow-bar span')
              .style.setProperty('--at', '100%');
""",
    """      flow.querySelector('.rec-flow-bar span')
          .style.setProperty('--at', '100%');
""",
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-bar-sweep' not in s, path + ': already in three'

    for old, new in [(MARKUP_OLD, MARKUP_NEW), (CSS_OLD, CSS_NEW),
                     (MOTION_OLD, MOTION_NEW), (STEP_OLD, STEP_NEW)]:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    for dead in DEAD:
        assert s.count(dead) >= 1, (path, dead.strip()[:46], s.count(dead))
        s = s.replace(dead, '')

    assert "'.rec-flow-bar span'" not in s, path + ': a percentage survives'
    assert 'var total' not in s, path + ': an unused total survives'

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
