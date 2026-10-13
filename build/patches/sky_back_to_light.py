# -*- coding: utf-8 -*-
"""The sky comes back up to light purple for the windows.

The ramp used to end at night. It now carries on past it: as the chat section
comes up the screen, the same two colours travel back out of the dark into a
pale lavender, so the windows sit on light rather than black. One parameter
runs the whole journey -- 0 at the top of the page, 1 at full dark, 2 once the
windows are on screen -- so the header's own light/dark switch follows it too.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """    var TOP = [[0, [255, 255, 255]], [0.55, [72, 58, 134]], [1, [14, 17, 28]]];
    var FOOT = [[0, [230, 223, 250]], [0.55, [54, 40, 108]], [1, [8, 10, 18]]];"""
new = """    var TOP = [[0, [255, 255, 255]], [0.55, [72, 58, 134]], [1, [14, 17, 28]],
               [1.5, [59, 46, 110]], [2, [239, 233, 255]]];
    var FOOT = [[0, [230, 223, 250]], [0.55, [54, 40, 108]], [1, [8, 10, 18]],
                [1.5, [75, 58, 140]], [2, [214, 203, 250]]];"""
assert old in s, 'sky ramp changed'
s = s.replace(old, new, 1)

old = """      // the colour holds its daylight a little longer than the content does
      var c = p * p;
      root.style.setProperty('--sky-a', ramp(TOP, c));
      root.style.setProperty('--sky-b', ramp(FOOT, c));
      root.style.setProperty('--sky-glow', (1 - c).toFixed(3));"""
new = """      // the colour holds its daylight a little longer than the content does
      var c = p * p;
      // ...and past full dark it climbs back out again as the windows arrive
      var back = 0;
      if (chat) {
        var ct = window.scrollY + chat.getBoundingClientRect().top;
        back = (window.scrollY - (ct - window.innerHeight)) / window.innerHeight;
        back = Math.min(1, Math.max(0, back));
      }
      var t = c + back;
      root.style.setProperty('--sky-a', ramp(TOP, t));
      root.style.setProperty('--sky-b', ramp(FOOT, t));
      root.style.setProperty('--sky-glow', (1 - c).toFixed(3));"""
assert old in s, 'sky assignment changed'
s = s.replace(old, new, 1)

# the glass tint and the header follow the same journey, not just the way down
old = """      var al = function (a, b) { return (a + (b - a) * c).toFixed(3); };"""
new = """      var lit = Math.min(1, t > 1 ? 2 - t : t);   // 0 at either end, 1 at full dark
      var al = function (a, b) { return (a + (b - a) * lit).toFixed(3); };"""
assert old in s, 'glass alpha helper changed'
s = s.replace(old, new, 1)

old = """        head.classList.toggle('is-night', c > 0.5);"""
new = """        head.classList.toggle('is-night', t > 0.5 && t < 1.55);"""
assert old in s, 'header night toggle changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('the sky climbs back to light purple')
