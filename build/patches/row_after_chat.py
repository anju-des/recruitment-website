# -*- coding: utf-8 -*-
"""The row waits for the conversation to finish.

Until the thread has played out, --row stays at 0 and the chat window sits
centred on its own. The moment the scroll is handed back, the point it was
handed back at becomes the row's starting line, so the next thing the reader
does is bring the other two in.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- the chat marks where it finished --------------------------------------
old = """    function release() {
      if (!held) return;
      held = false;"""
new = """    function release() {
      if (!held) return;
      held = false;
      // where the row starts counting from
      window.__miraDone = window.scrollY;"""
assert old in s, 'release changed'
s = s.replace(old, new, 1)

# a reader who never triggered the hold (reduced motion, no JS path) should
# still be able to assemble the row
old = """    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(update);
    }, { passive: true });
    window.addEventListener('resize', update);
    update();"""
new = """    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(update);
    }, { passive: true });
    window.addEventListener('resize', update);
    update();"""
assert old in s, 'scroll wiring changed'

old = """          // once the section pins, the row assembles: the chat window moves
          // down and left while the other two arrive from the right
          var row = Math.min(1, Math.max(0, (window.scrollY - winLanding) / 820));"""
new = """          // The row only starts once Mira has finished answering: until then
          // __miraDone is unset and the chat window stays centred alone.
          var rowStart = typeof window.__miraDone === 'number'
            ? Math.max(winLanding, window.__miraDone)
            : Infinity;
          var row = Math.min(1, Math.max(0, (window.scrollY - rowStart) / 820));"""
assert old in s, 'row assignment changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('the row waits for the answer')
