# -*- coding: utf-8 -*-
"""The lines whiten with the scroll, not on a timer.

All three are grey when the section arrives; each one then takes its own
stretch of scroll to come up to white, so the reader sets the pace and it
runs backwards when they scroll back.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """    /* the text is always there in grey; what moves is the colour, one line at
       a time, and it fills forwards so each line keeps the white it reaches */
    .rec-say.rec-in .rec-line { animation:rec-line-white .7s ease-out both; }
    .rec-say.rec-in .rec-line:nth-child(2) { animation-delay:.5s; }
    .rec-say.rec-in .rec-line:nth-child(3) { animation-delay:1s; }
    @keyframes rec-line-white {
      from { color:#8E97AE; }
      to   { color:#FFFFFF; }
    }
    @media (prefers-reduced-motion: reduce) {
      .rec-say.rec-in .rec-line { animation:none; color:#FFFFFF; }
    }"""
new = """    /* The text is always there in grey; what moves is the colour, one line at
       a time, driven by the scroll itself -- --l1/2/3 each run 0 to 1 over
       their own stretch of the approach. */
    .rec-line:nth-child(1) { color:color-mix(in srgb, #FFFFFF calc(var(--l1, 0) * 100%), #8E97AE); }
    .rec-line:nth-child(2) { color:color-mix(in srgb, #FFFFFF calc(var(--l2, 0) * 100%), #8E97AE); }
    .rec-line:nth-child(3) { color:color-mix(in srgb, #FFFFFF calc(var(--l3, 0) * 100%), #8E97AE); }
    @media (prefers-reduced-motion: reduce) {
      .rec-line { color:#FFFFFF; }
    }"""
assert old in s, 'line colour rules changed'
s = s.replace(old, new, 1)

old = """        root.style.setProperty('--rec-q', q.toFixed(3));"""
new = """        root.style.setProperty('--rec-q', q.toFixed(3));
        // each line comes up to white over its own slice of the last stretch
        var band = function (a, b) {
          return Math.min(1, Math.max(0, (q - a) / (b - a))).toFixed(3);
        };
        root.style.setProperty('--l1', band(0.68, 0.78));
        root.style.setProperty('--l2', band(0.78, 0.88));
        root.style.setProperty('--l3', band(0.88, 0.98));"""
assert old in s, 'progress assignment changed'
s = s.replace(old, new, 1)

# the observer that used to time the lines has nothing left to do
m = re.search(r'\n  // The lines turn white one at a time.*?\n  \}\(\)\);\n', s, re.S)
assert m, 'statement observer not found'
s = s[:m.start()] + '\n' + s[m.end():]
assert 'rec-in' not in s, 'a rec-in reference is left'

io.open(p, 'w', encoding='utf-8').write(s)
print('lines whiten with the scroll')
