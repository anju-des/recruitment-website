# -*- coding: utf-8 -*-
"""Text out first, then the boxes drop away.

Two problems with the old exit. The statement and the boxes were leaving over
the same stretch, so the text still looked present while everything around it
was already falling. And the fall was aimed at the chat window's position on
the page -- which is nowhere near the screen while this section is pinned, so
it just looked like they slid off the bottom.

Now the text clears first, and the boxes then drop out of the frame over the
last fifth, converging and shrinking as they go, finishing exactly as the
section unpins and the window takes over.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """        // once all three are white it leaves, and is gone with a beat of the
        // pinned stretch still to run
        root.style.setProperty('--say-out', slice(0.70, 0.88));"""
new = """        // once all three are white the statement leaves, on its own
        root.style.setProperty('--say-out', slice(0.62, 0.80));"""
assert old in s, 'say-out slice changed'
s = s.replace(old, new, 1)

old = """        if (chat) {
          // Measured from the chat SECTION, not the window: the window is
          // pinned, so its own rect barely moves with the scroll and every
          // progress built on it came out as zero.
          var cb = chat.getBoundingClientRect();
          var chatTop = window.scrollY + cb.top;
          var fieldY = window.scrollY + box.top + box.height / 2;
          var winY = chatTop + window.innerHeight / 2;
          var winLanding = chatTop;"""
new = """        if (chat) {
          // Measured from the chat SECTION, not the window: the window is
          // pinned, so its own rect barely moves with the scroll and every
          // progress built on it came out as zero.
          var cb = chat.getBoundingClientRect();
          var chatTop = window.scrollY + cb.top;
          var winLanding = chatTop;"""
assert old in s, 'fall target block changed'
s = s.replace(old, new, 1)

old = """          // the boxes fall away over the same last stretch
          var f = parseFloat(slice(0.70, 1));
          root.style.setProperty('--fall', f.toFixed(4));
          root.style.setProperty('--fall-px', ((winY - fieldY) * f).toFixed(1) + 'px');
          // full strength until the last fifth of the journey
          root.style.setProperty('--fall-o',
            Math.min(1, Math.max(0, (1 - f) / 0.2)).toFixed(3));"""
new = """          // and only then do the boxes drop out of the frame. The distance is
          // a screenful rather than the gap to the window: that window is far
          // down the page and nowhere near the viewport while this section is
          // pinned, so aiming at it just looked like a slide off the bottom.
          var f = parseFloat(slice(0.80, 1));
          root.style.setProperty('--fall', f.toFixed(4));
          root.style.setProperty('--fall-px', (f * window.innerHeight * 0.62).toFixed(1) + 'px');
          root.style.setProperty('--fall-o',
            Math.min(1, Math.max(0, (1 - f) / 0.45)).toFixed(3));"""
assert old in s, 'fall assignment changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('text clears, then the boxes drop')
