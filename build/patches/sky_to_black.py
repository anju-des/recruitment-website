# -*- coding: utf-8 -*-
"""The sky ends black and stays there.

It used to climb back out of the dark into lavender for the window section.
Now the window is black, so the page behind it goes black too and holds: the
ramp ends at black and there is no journey back up.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """    var TOP = [[0, [255, 255, 255]], [0.55, [72, 58, 134]], [1, [14, 17, 28]],
               [1.5, [59, 46, 110]], [2, [239, 233, 255]]];
    var FOOT = [[0, [230, 223, 250]], [0.55, [54, 40, 108]], [1, [8, 10, 18]],
                [1.5, [75, 58, 140]], [2, [214, 203, 250]]];"""
new = """    var TOP = [[0, [255, 255, 255]], [0.55, [72, 58, 134]], [1, [5, 5, 8]]];
    var FOOT = [[0, [230, 223, 250]], [0.55, [54, 40, 108]], [1, [0, 0, 0]]];"""
assert old in s, 'sky ramp changed'
s = s.replace(old, new, 1)

old = """      // ...and past full dark it climbs back out again as the windows arrive
      var back = 0;
      if (chat) {
        var ct = window.scrollY + chat.getBoundingClientRect().top;
        back = (window.scrollY - (ct - window.innerHeight)) / window.innerHeight;
        back = Math.min(1, Math.max(0, back));
      }
      var t = c + back;"""
new = """      var t = c;"""
assert old in s, 'sky climb-back changed'
s = s.replace(old, new, 1)

old = """      var lit = Math.min(1, t > 1 ? 2 - t : t);   // 0 at either end, 1 at full dark
      var al = function (a, b) { return (a + (b - a) * lit).toFixed(3); };"""
new = """      var al = function (a, b) { return (a + (b - a) * t).toFixed(3); };"""
assert old in s, 'glass alpha helper changed'
s = s.replace(old, new, 1)

old = """        head.classList.toggle('is-night', t > 0.5 && t < 1.55);"""
new = """        head.classList.toggle('is-night', t > 0.5);"""
assert old in s, 'header night toggle changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('the sky ends black')
