# -*- coding: utf-8 -*-
"""Pin the statement, then colour it line by line.

The text arrives grey, settles in the middle of the screen, and stays there
while the next stretch of scroll brings each line up to white in turn. Only
after all three are white does it leave, with the boxes falling away towards
the window below.

One value runs the pinned stretch: 0 where the section pins, 1 where it
unpins, with each piece of the choreography taking its own slice of it.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- markup: the boxes and the statement ride in a sticky frame ------------
old = '          <div class="rec-boxes" aria-hidden="true">'
new = ('          <div class="rec-say-pin">\n'
       '          <div class="rec-boxes" aria-hidden="true">')
assert old in s, 'boxes markup changed'
s = s.replace(old, new, 1)

old = """          </p>
        </section>"""
new = """          </p>
          </div>
        </section>"""
assert old in s, 'statement close changed'
s = s.replace(old, new, 1)

# ---- css -------------------------------------------------------------------
old = """    /* a long run at this section: the lines have the whole approach to
       travel over, so the scroll through it is unhurried */
    .rec-next { position:relative; min-height:260vh; display:grid; place-items:center; }"""
new = """    /* The statement is pinned for the length of this section: it settles in
       the middle of the screen and stays there while the lines colour. */
    .rec-next { position:relative; min-height:300vh; }
    .rec-say-pin { position:sticky; top:0; height:100vh; display:grid; place-items:center; }"""
assert old in s, 'statement section rule changed'
s = s.replace(old, new, 1)

old = """      .rec-say { max-width:30ch; }"""
new = """      .rec-say { max-width:30ch; }
      .rec-next { min-height:0; }
      .rec-say-pin { position:static; height:auto; padding-block:80px; }"""
assert old in s, 'responsive statement rule changed'
s = s.replace(old, new, 1)

# ---- script: one value for the pinned stretch ------------------------------
old = """      if (next) {
        // Measured from the section, which never moves. Measuring the
        // statement itself fed its own transform back into the calculation:
        // the further it slid, the further along the exit it thought it was.
        var box = next.getBoundingClientRect();
        var landing = window.scrollY + box.top + box.height / 2 - window.innerHeight / 2;"""
new = """      if (next) {
        // Measured from the section, which never moves. Measuring the
        // statement itself fed its own transform back into the calculation:
        // the further it slid, the further along the exit it thought it was.
        var box = next.getBoundingClientRect();
        // the statement is centred from the moment the section pins
        var landing = window.scrollY + box.top;"""
assert old in s, 'landing block changed'
s = s.replace(old, new, 1)

# the band helper sits between these lines, so the stretch is matched by its
# ends rather than quoted in full
start = s.index("        // each line comes up to white over its own slice of the last stretch")
end = s.index("        // they are up to full strength by the first third of that travel")
s = s[:start] + """        // pp runs 0 to 1 across the pinned stretch, and every part of the
        // choreography takes a slice of it
        var pinSpan = Math.max(1, next.offsetHeight - window.innerHeight);
        var pp = Math.min(1, Math.max(0, (window.scrollY - landing) / pinSpan));
        var slice = function (a, b) {
          return Math.min(1, Math.max(0, (pp - a) / (b - a))).toFixed(3);
        };
        // the lines come up to white one at a time, while nothing else moves
        root.style.setProperty('--l1', slice(0.08, 0.26));
        root.style.setProperty('--l2', slice(0.28, 0.46));
        root.style.setProperty('--l3', slice(0.48, 0.66));
""" + s[end:]


old = """        // and past the landing it leaves again, over the next 520px
        var past = (window.scrollY - landing) / 520;
        root.style.setProperty('--say-out', Math.min(1, Math.max(0, past)).toFixed(3));"""
new = """        // only once all three are white does the statement leave
        root.style.setProperty('--say-out', slice(0.74, 0.96));"""
assert old in s, 'say-out assignment changed'
s = s.replace(old, new, 1)

old = """          var f = (window.scrollY - landing) / Math.max(1, winLanding - landing);
          f = Math.min(1, Math.max(0, f));"""
new = """          // the boxes fall away over the same last stretch
          var f = parseFloat(slice(0.70, 1));"""
assert old in s, 'fall progress changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('statement pinned; lines colour in place')
