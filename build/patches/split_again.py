# -*- coding: utf-8 -*-
"""The chat window gets its view to itself again.

The other two move out into a section of their own below it, so the reader
finishes with Mira, scrolls on, and meets the results there. The row that
assembled around the chat window -- the slide left, the shrink, the two
arriving from the right -- is gone with them. And the chat window itself goes
black.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- the two result windows move to their own section ----------------------
m = re.search(r'\n *<div class="rec-win rec-win--2">.*?'
              r'\n *<div class="rec-win rec-win--3">.*?\n          </div>\n', s, re.S)
assert m, 'the two result windows were not found'
pair = m.group(0)
s = s[:m.start()] + '\n' + s[m.end():]

old = """          </div>
          </div>
        </section>"""
new = """          </div>
          </div>
        </section>

        <!-- WHAT CAME OF IT -->
        <section class="rec-more-sec">
          <div class="rec-more">%s          </div>
        </section>""" % pair
assert old in s, 'chat section close changed'
s = s.replace(old, new, 1)

# ---- css: no row, just the window; the pair gets its own section -----------
old = """    /* Pulled up so its window is already climbing into the lower half of the
       screen while the statement section is still pinned -- that overlap is
       what the falling boxes land on. */
    .rec-chat-sec { position:relative; min-height:240vh; margin-top:-55vh; }"""
new = """    /* Pulled up so its window is already climbing into the lower half of the
       screen while the statement section is still pinned -- that overlap is
       what the falling boxes land on. */
    .rec-chat-sec { position:relative; min-height:150vh; margin-top:-55vh; }
    /* the results, in a section of their own further down */
    .rec-more-sec { min-height:100vh; display:grid; place-items:center; }
    .rec-more { display:flex; align-items:stretch; gap:24px; }"""
assert old in s, 'chat section rule changed'
s = s.replace(old, new, 1)

start = s.index('    /* At --row 0 the chat window sits centred')
end = s.index('    .rec-win { flex:none; width:540px;')
block = s[start:end]
assert '--row' in block, 'row rule block changed'
s = s[:start] + """    .rec-wins { position:absolute; top:50%; left:50%; translate:-50% -50%;
                display:flex; }
""" + s[end:]

old = """    /* each slides in from the right, one after the other */
    .rec-win--2 { opacity:var(--win2, 0);
                  transform:translateX(calc((1 - var(--win2, 0)) * 460px)); }
    .rec-win--3 { opacity:var(--win3, 0);
                  transform:translateX(calc((1 - var(--win3, 0)) * 460px)); }"""
new = """    /* they arrive one after the other once their own section is in view */
    .rec-win--2, .rec-win--3 { opacity:0; transform:translateY(28px);
                               transition:opacity .7s ease, transform .7s ease; }
    .rec-more-sec.is-on .rec-win--2,
    .rec-more-sec.is-on .rec-win--3 { opacity:1; transform:none; }
    .rec-more-sec.is-on .rec-win--3 { transition-delay:.35s; }"""
assert old in s, 'side window rules changed'
s = s.replace(old, new, 1)

# ---- black for the chat window ---------------------------------------------
old = """    .rec-win--dark { background:#141829;"""
new = """    .rec-win--dark { background:#000000;"""
assert old in s, 'dark window rule changed'
s = s.replace(old, new, 1)

old = """      /* no room for a row: they stack, and nothing is pinned */
      .rec-chat-sec { min-height:0; margin-top:0; padding-block:60px; }
      .rec-wins-pin { position:static; height:auto; }
      .rec-wins { position:static; translate:none; transform:none;
                  flex-direction:column; align-items:stretch; }
      .rec-win { width:100%; max-height:none; }
      .rec-win--2, .rec-win--3 { opacity:1; transform:none; }"""
new = """      /* nothing is pinned and the pair stacks */
      .rec-chat-sec, .rec-more-sec { min-height:0; margin-top:0; padding-block:60px; }
      .rec-wins-pin { position:static; height:auto; }
      .rec-wins { position:static; translate:none; }
      .rec-more { flex-direction:column; align-items:stretch; }
      .rec-win { width:100%; max-height:none; }"""
assert old in s, 'responsive window rules changed'
s = s.replace(old, new, 1)

# ---- script: the row progress goes; the pair gets an observer --------------
start = s.index("          // The row only starts once Mira has finished answering")
end = s.index("      if (head) {", start)
block = s[start:end]
assert '--row' in block, 'row script block changed'
s = s[:start] + s[end:]

old = "</script>\n</body>"
new = """
  // The two result windows arrive one after the other, and again on the way
  // back: the class comes off once their section has left.
  (function () {
    var more = document.querySelector('.rec-more-sec');
    if (!more || !('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.intersectionRatio >= 0.45) more.classList.add('is-on');
        else if (!e.isIntersecting) more.classList.remove('is-on');
      });
    }, { threshold: [0, 0.45] });
    io.observe(more);
  }());
</script>
</body>"""
assert old in s, 'script close not found'
s = s.replace(old, new, 1)

assert '--row' not in s and '--win2' not in s, 'a row reference is left'
io.open(p, 'w', encoding='utf-8').write(s)
print('chat window alone and black; results below')
