# -*- coding: utf-8 -*-
"""One pinned section: the chat window settles down and left, the other two
come in from the right.

Scroll drives the whole thing. The row starts with the chat window centred at
full size; as --row climbs it drifts down and left while the set shrinks to
fit three across, and the other two slide in from off-screen right, one after
the other.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- markup: the two windows rejoin the first, inside a pinned row ---------
m = re.search(r'\n *<!-- AND THE REST OF WHAT SHE RUNS -->\n'
              r' *<section class="rec-more-sec">\n *<div class="rec-more">\n(.*?)'
              r' *</div>\n *</section>\n', s, re.S)
assert m, 'the second window section was not found'
pair = m.group(1)
s = s[:m.start()] + '\n' + s[m.end():]

old = """        <section class="rec-chat-sec">
          <div class="rec-win">"""
new = """        <section class="rec-chat-sec">
          <div class="rec-wins-pin">
          <div class="rec-wins">
          <div class="rec-win">"""
assert old in s, 'chat section opening changed'
s = s.replace(old, new, 1)

old = """            </div>
          </div>
        </section>"""
new = """            </div>
          </div>
%s          </div>
          </div>
        </section>""" % pair
assert old in s, 'chat section close changed'
s = s.replace(old, new, 1)

# ---- css -------------------------------------------------------------------
old = """    .rec-chat-sec { min-height:110vh; display:grid; place-items:center; }
    /* the other two, in a section of their own */
    .rec-more-sec { min-height:100vh; display:grid; place-items:center; }
    .rec-more { display:flex; align-items:flex-start; gap:24px; }"""
new = """    /* tall enough to hold the row still while it assembles */
    .rec-chat-sec { position:relative; min-height:240vh; }
    .rec-wins-pin { position:sticky; top:0; height:100vh; display:grid; place-items:center; }
    /* At --row 0 the chat window sits centred at full size. As it climbs, the
       row drifts down and left and shrinks to the size that fits three
       across. The percentage is of the row's own width, so the first window
       is exactly centred whatever the three measure. */
    .rec-wins { display:flex; align-items:flex-start; gap:24px;
                transform:translate(calc((1 - var(--row, 0)) * (50% - 270px)),
                                    calc(var(--row, 0) * 54px))
                          scale(calc(1 - 0.29 * var(--row, 0))); }"""
assert old in s, 'chat section rules changed'
s = s.replace(old, new, 1)

old = """    /* they arrive one after the other once the section is in view */
    .rec-win--2, .rec-win--3 { opacity:0; transform:translateY(28px);
                               transition:opacity .7s ease, transform .7s ease; }
    .rec-more-sec.is-on .rec-win--2,
    .rec-more-sec.is-on .rec-win--3 { opacity:1; transform:none; }
    .rec-more-sec.is-on .rec-win--3 { transition-delay:.35s; }"""
new = """    /* each slides in from the right, one after the other */
    .rec-win--2 { opacity:var(--win2, 0);
                  transform:translateX(calc((1 - var(--win2, 0)) * 460px)); }
    .rec-win--3 { opacity:var(--win3, 0);
                  transform:translateX(calc((1 - var(--win3, 0)) * 460px)); }"""
assert old in s, 'side window rules changed'
s = s.replace(old, new, 1)

old = """      /* no room for two side by side: they stack */
      .rec-chat-sec, .rec-more-sec { min-height:0; padding-block:60px; }
      .rec-more { flex-direction:column; align-items:stretch; }
      .rec-win { width:100%; }"""
new = """      /* no room for a row: they stack, and nothing is pinned */
      .rec-chat-sec { min-height:0; padding-block:60px; }
      .rec-wins-pin { position:static; height:auto; }
      .rec-wins { flex-direction:column; align-items:stretch; transform:none; }
      .rec-win { width:100%; }
      .rec-win--2, .rec-win--3 { opacity:1; transform:none; }"""
assert old in s, 'responsive window rules changed'
s = s.replace(old, new, 1)

# ---- script ----------------------------------------------------------------
old = """          root.style.setProperty('--fall-o',
            Math.min(1, Math.max(0, (1 - f) / 0.2)).toFixed(3));"""
new = """          root.style.setProperty('--fall-o',
            Math.min(1, Math.max(0, (1 - f) / 0.2)).toFixed(3));

          // once the section pins, the row assembles: the chat window moves
          // down and left while the other two arrive from the right
          var row = Math.min(1, Math.max(0, (window.scrollY - winLanding) / 820));
          root.style.setProperty('--row', row.toFixed(4));
          root.style.setProperty('--win2',
            Math.min(1, Math.max(0, (row - 0.18) / 0.32)).toFixed(3));
          root.style.setProperty('--win3',
            Math.min(1, Math.max(0, (row - 0.54) / 0.32)).toFixed(3));"""
assert old in s, 'fall opacity assignment changed'
s = s.replace(old, new, 1)

m = re.search(r'\n  // The last two windows come in one after the other.*?\n  \}\(\)\);\n', s, re.S)
assert m, 'the pair observer was not found'
s = s[:m.start()] + '\n' + s[m.end():]
assert 'rec-more' not in s, 'a reference to the old section is left'

io.open(p, 'w', encoding='utf-8').write(s)
print('one pinned row: down-left, then in from the right')
