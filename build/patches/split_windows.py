# -*- coding: utf-8 -*-
"""The first window stands alone again; the other two get their own section.

The row that assembled around the chat window is gone. You read that window
by itself, scroll on, and the next section brings the other two in one after
the other -- both the same size as the first.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- pull the two side windows out of the chat section ---------------------
m = re.search(r'\n *<div class="rec-win rec-win--side rec-win--2">.*?'
              r'\n *<div class="rec-win rec-win--side rec-win--3">.*?\n          </div>\n',
              s, re.S)
assert m, 'side windows not found'
side = m.group(0)
s = s[:m.start()] + '\n' + s[m.end():]

# the wrappers that pinned the row go with them
old = """        <section class="rec-chat-sec">
          <div class="rec-wins-pin">
          <div class="rec-wins">
          <div class="rec-win">"""
new = """        <section class="rec-chat-sec">
          <div class="rec-win">"""
assert old in s, 'chat section opening changed'
s = s.replace(old, new, 1)

old = """            </div>
          </div>
          </div>
          </div>
        </section>"""
new = """            </div>
          </div>
        </section>

        <!-- AND THE REST OF WHAT SHE RUNS -->
        <section class="rec-more-sec">
          <div class="rec-more">%s          </div>
        </section>""" % side.replace('rec-win--side ', '')
assert old in s, 'chat section close changed'
s = s.replace(old, new, 1)

# ---- css -------------------------------------------------------------------
# the comment block above this rule has shifted more than once, so the whole
# stretch is matched by its ends rather than quoted in full
start = s.index('    /* tall enough to hold the row still while the three assemble */')
end = s.index('    .rec-win { flex:none; width:540px; border-radius:16px; overflow:hidden;')
s = s[:start] + """    .rec-chat-sec { min-height:110vh; display:grid; place-items:center; }
    /* the other two, in a section of their own */
    .rec-more-sec { min-height:100vh; display:grid; place-items:center; }
    .rec-more { display:flex; align-items:flex-start; gap:24px; }
""" + s[end:]


old = """    /* the two that arrive later */
    .rec-win--side { width:296px; opacity:0; transform:translateY(26px); }
    .rec-win--2 { opacity:var(--win2, 0);
                  transform:translateY(calc((1 - var(--win2, 0)) * 26px)); }
    .rec-win--3 { opacity:var(--win3, 0);
                  transform:translateY(calc((1 - var(--win3, 0)) * 26px)); }"""
new = """    /* they arrive one after the other once the section is in view */
    .rec-win--2, .rec-win--3 { opacity:0; transform:translateY(28px);
                               transition:opacity .7s ease, transform .7s ease; }
    .rec-more-sec.is-on .rec-win--2,
    .rec-more-sec.is-on .rec-win--3 { opacity:1; transform:none; }
    .rec-more-sec.is-on .rec-win--3 { transition-delay:.35s; }"""
assert old in s, 'side window rules changed'
s = s.replace(old, new, 1)

old = """      /* no room for a row of three: they stack and stay put */
      .rec-chat-sec { min-height:0; padding-block:60px; }
      .rec-wins-pin { position:static; height:auto; }
      .rec-wins { flex-direction:column; align-items:stretch; transform:none; }
      .rec-win { width:100%; }
      .rec-win--side { width:100%; opacity:1; transform:none; }"""
new = """      /* no room for two side by side: they stack */
      .rec-chat-sec, .rec-more-sec { min-height:0; padding-block:60px; }
      .rec-more { flex-direction:column; align-items:stretch; }
      .rec-win { width:100%; }"""
assert old in s, 'responsive window rules changed'
s = s.replace(old, new, 1)

# ---- script ----------------------------------------------------------------
old = """
          // past the window, the row assembles: it slides left and the other
          // two arrive, one after the other
          var row = (window.scrollY - winLanding) / 760;
          row = Math.min(1, Math.max(0, row));
          root.style.setProperty('--row', row.toFixed(4));
          root.style.setProperty('--win2',
            Math.min(1, Math.max(0, (row - 0.12) / 0.34)).toFixed(3));
          root.style.setProperty('--win3',
            Math.min(1, Math.max(0, (row - 0.5) / 0.34)).toFixed(3));"""
assert old in s, 'row assignment changed'
s = s.replace(old, '', 1)

old = "</script>\n</body>"
new = """
  // The last two windows come in one after the other, and again on the way
  // back: the class comes off once the section has left.
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

io.open(p, 'w', encoding='utf-8').write(s)
print('windows split across two sections')
