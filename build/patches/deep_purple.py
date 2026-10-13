# -*- coding: utf-8 -*-
"""The sky goes down into violet one more time.

Same mechanism as every other change of ground on this page: the ramp
simply carries on past the light it climbed to, through a saturated violet
and into a near-black purple, driven by how far the new section has come up
the screen. Nothing paints a background of its own.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- the section ------------------------------------------------------------
old = """        <!-- CLOSING (scroll room; the heading rides in the pinned frame) -->
        <section class="rec-close"></section>"""
new = """        <!-- CLOSING (scroll room; the heading rides in the pinned frame) -->
        <section class="rec-close"></section>

        <!-- and back down into violet, the same way -->
        <section class="rec-deep"></section>"""
assert old in s, 'closing markup changed'
s = s.replace(old, new, 1)

old = "    .rec-close { position:relative; min-height:35vh; }"
new = """    /* long enough that the light has a moment of its own before the ramp
       starts back down -- the two must not overlap */
    .rec-close { position:relative; min-height:150vh; }
    .rec-wrap > section.rec-deep { padding:0; }
    .rec-deep { position:relative; min-height:140vh; }"""
assert old in s, 'closing rule changed'
s = s.replace(old, new, 1)

old = "      .rec-close { min-height:40vh; }"
new = """      .rec-close { min-height:40vh; }
      .rec-deep { min-height:60vh; }"""
assert old in s, 'responsive closing rule changed'
s = s.replace(old, new, 1)

# ---- the ramp carries on past the light ------------------------------------
old = """    var TOP = [[0, [255, 255, 255]], [0.55, [72, 58, 134]], [1, [5, 5, 8]],
               [1.5, [57, 45, 106]], [2, [239, 234, 255]]];
    var FOOT = [[0, [230, 223, 250]], [0.55, [54, 40, 108]], [1, [0, 0, 0]],
                [1.5, [72, 56, 136]], [2, [255, 255, 255]]];"""
new = """    var TOP = [[0, [255, 255, 255]], [0.55, [72, 58, 134]], [1, [5, 5, 8]],
               [1.5, [57, 45, 106]], [2, [239, 234, 255]],
               [2.5, [138, 111, 214]], [3, [42, 22, 89]]];
    var FOOT = [[0, [230, 223, 250]], [0.55, [54, 40, 108]], [1, [0, 0, 0]],
                [1.5, [72, 56, 136]], [2, [255, 255, 255]],
                [2.5, [91, 63, 168]], [3, [20, 10, 46]]];"""
assert old in s, 'sky ramp changed'
s = s.replace(old, new, 1)

old = "    var close = document.querySelector('.rec-close');"
new = """    var close = document.querySelector('.rec-close');
    var deep = document.querySelector('.rec-deep');"""
assert old in s, 'script head changed'
s = s.replace(old, new, 1)

old = "      var t = c + back;"
new = """      // ...and then back down into violet as the last section comes up
      var down = 0;
      if (deep) {
        var dt = window.scrollY + deep.getBoundingClientRect().top;
        down = (window.scrollY - (dt - window.innerHeight)) / window.innerHeight;
        down = Math.min(1, Math.max(0, down));
      }
      var t = c + back + down;"""
assert old in s, 'sky progress changed'
s = s.replace(old, new, 1)

# the glass reads its strength off how dark the sky is, which now has two peaks
old = "      var lit = Math.min(1, t > 1 ? 2 - t : t);   // 0 at either end, 1 at full dark"
new = """      // 1 wherever the sky is dark, 0 where it is light -- twice over now
      var lit = t <= 1 ? t : (t <= 2 ? 2 - t : Math.min(1, t - 2));"""
assert old in s, 'glass alpha helper changed'
s = s.replace(old, new, 1)

old = "        head.classList.toggle('is-night', t > 0.5 && t < 1.55);"
new = "        head.classList.toggle('is-night', (t > 0.5 && t < 1.55) || t > 2.45);"
assert old in s, 'header night toggle changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('down into violet')
