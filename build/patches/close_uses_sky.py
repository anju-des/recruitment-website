# -*- coding: utf-8 -*-
"""The closing section lights up the same way the rest of the page does.

Instead of carrying a gradient of its own, it hands the job back to the sky:
the same scroll-driven ramp that took the page from white to black now
carries on past black and climbs to light as this section arrives. One
mechanism for every transition on the page.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- the ramp carries on past black ----------------------------------------
old = """    var TOP = [[0, [255, 255, 255]], [0.55, [72, 58, 134]], [1, [5, 5, 8]]];
    var FOOT = [[0, [230, 223, 250]], [0.55, [54, 40, 108]], [1, [0, 0, 0]]];"""
new = """    var TOP = [[0, [255, 255, 255]], [0.55, [72, 58, 134]], [1, [5, 5, 8]],
               [1.5, [57, 45, 106]], [2, [239, 234, 255]]];
    var FOOT = [[0, [230, 223, 250]], [0.55, [54, 40, 108]], [1, [0, 0, 0]],
                [1.5, [72, 56, 136]], [2, [255, 255, 255]]];"""
assert old in s, 'sky ramp changed'
s = s.replace(old, new, 1)

old = """      var t = c;"""
new = """      // ...and climbs back out of it as the closing section arrives, over the
      // screenful before it reaches the top
      var back = 0;
      if (close) {
        var ct = window.scrollY + close.getBoundingClientRect().top;
        back = (window.scrollY - (ct - window.innerHeight)) / window.innerHeight;
        back = Math.min(1, Math.max(0, back));
      }
      var t = c + back;"""
assert old in s, 'sky progress changed'
s = s.replace(old, new, 1)

old = """      var al = function (a, b) { return (a + (b - a) * t).toFixed(3); };"""
new = """      var lit = Math.min(1, t > 1 ? 2 - t : t);   // 0 at either end, 1 at full dark
      var al = function (a, b) { return (a + (b - a) * lit).toFixed(3); };"""
assert old in s, 'glass alpha helper changed'
s = s.replace(old, new, 1)

old = """        head.classList.toggle('is-night', t > 0.5);"""
new = """        head.classList.toggle('is-night', t > 0.5 && t < 1.55);"""
assert old in s, 'header night toggle changed'
s = s.replace(old, new, 1)

old = """    var chat = document.querySelector('.rec-chat-sec');"""
new = """    var chat = document.querySelector('.rec-chat-sec');
    var close = document.querySelector('.rec-close');"""
assert old in s, 'script head changed'
s = s.replace(old, new, 1)

# ---- the section stops painting its own ground -----------------------------
old = """    /* It starts at the same black as the section above and climbs to white
       over its own first half, so there is no line where one ends and the
       other begins -- the light simply arrives. */
    .rec-wrap > section.rec-close { padding:0; }
    .rec-close { position:relative; min-height:140vh; }
    .rec-close-panel { height:140vh;
                       background:linear-gradient(180deg,
                         #000000 0%, #06060B 10%, #231D44 30%,
                         #EFEAFF 62%, #FFFFFF 100%); }"""
new = """    /* No ground of its own: the sky lightens behind it, the same way it
       darkened for the sections above. */
    .rec-wrap > section.rec-close { padding:0; }
    .rec-close { position:relative; min-height:120vh; }"""
assert old in s, 'closing styles changed'
s = s.replace(old, new, 1)

old = '          <div class="rec-close-panel"></div>\n'
assert old in s, 'closing panel markup changed'
s = s.replace(old, '', 1)

old = """      .rec-close, .rec-close-panel { min-height:110vh; height:110vh; }"""
new = """      .rec-close { min-height:100vh; }"""
assert old in s, 'responsive closing rule changed'
s = s.replace(old, new, 1)

assert 'rec-close-panel' not in s, 'a panel reference is left'
io.open(p, 'w', encoding='utf-8').write(s)
print('the closing section rides the sky')
