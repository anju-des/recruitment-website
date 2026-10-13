# -*- coding: utf-8 -*-
"""One more section below the stages, on the same ramp.

The sky carries on past the light it reached for the stages, through violet
and down into near-black again -- the same mechanism as every other change
of ground on this page, measured from the new section's own top. Empty, the
way the light one and the violet one both started.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- the section ------------------------------------------------------------
old = """          </div>
        </section>
"""
start = s.index('<section class="rec-deep">')
end = s.index(old, start) + len(old)
s = s[:end] + """
        <!-- and down again, the same way -->
        <section class="rec-rest"></section>
""" + s[end:]

old = """    /* one screen of ramp, then a stretch of held scroll for each stage */
    .rec-deep { position:relative; min-height:340vh; }"""
new = """    /* one screen of ramp, then a stretch of held scroll for each stage */
    .rec-deep { position:relative; min-height:340vh; }
    /* its own ramp runs over the screen before it, which is exactly when the
       stage frame lets go, so the two never overlap */
    .rec-wrap > section.rec-rest { padding:0; }
    .rec-rest { position:relative; min-height:200vh; }"""
assert old in s, 'deep section rule changed'
s = s.replace(old, new, 1)

old = """      .rec-deep { min-height:0; padding-block:72px; }"""
new = """      .rec-deep { min-height:0; padding-block:72px; }
      .rec-rest { min-height:60vh; }"""
assert old in s, 'responsive deep rule changed'
s = s.replace(old, new, 1)

# ---- the ramp carries on -----------------------------------------------------
old = """               [2.5, [72, 58, 134]], [3, [239, 234, 255]]];"""
new = """               [2.5, [72, 58, 134]], [3, [239, 234, 255]],
               [3.5, [86, 66, 160]], [4, [26, 16, 54]]];"""
assert old in s, 'sky top ramp changed'
s = s.replace(old, new, 1)

old = """                [2.5, [54, 40, 108]], [3, [255, 255, 255]]];"""
new = """                [2.5, [54, 40, 108]], [3, [255, 255, 255]],
                [3.5, [58, 40, 112]], [4, [10, 5, 26]]];"""
assert old in s, 'sky foot ramp changed'
s = s.replace(old, new, 1)

old = """    var deep = document.querySelector('.rec-deep');"""
new = """    var deep = document.querySelector('.rec-deep');
    var rest = document.querySelector('.rec-rest');"""
assert old in s, 'script head changed'
s = s.replace(old, new, 1)

old = """      var t = c + back + down;"""
new = """      // ...and down one last time as the closing section comes up
      var last = 0;
      if (rest) {
        var rt = window.scrollY + rest.getBoundingClientRect().top;
        last = (window.scrollY - (rt - window.innerHeight)) / window.innerHeight;
        last = Math.min(1, Math.max(0, last));
      }
      var t = c + back + down + last;"""
assert old in s, 'sky progress changed'
s = s.replace(old, new, 1)

old = """      // dark from the chat through the windows, then light again for the stages
      var lit = t <= 1 ? t : (t <= 2 ? 1 : Math.max(0, 3 - t));"""
new = """      // dark, light, dark again: 1 wherever the ground is dark
      var lit = t <= 1 ? t
              : (t <= 2 ? 1
              : (t <= 3 ? 3 - t : Math.min(1, t - 3)));"""
assert old in s, 'glass alpha helper changed'
s = s.replace(old, new, 1)

old = "        head.classList.toggle('is-night', t > 0.5 && t < 2.6);"
new = "        head.classList.toggle('is-night', (t > 0.5 && t < 2.6) || t > 3.45);"
assert old in s, 'header night toggle changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('one more section, same ramp')
