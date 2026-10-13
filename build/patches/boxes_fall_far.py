# -*- coding: utf-8 -*-
"""The boxes fall the whole way to the window, not 460px into thin air.

The drop is now measured: the gap between the field and the chat window, run
over exactly the scroll between the statement landing and the window centring.
They hold their strength for most of the trip and only fade in the last fifth,
as they reach the window.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """               opacity:calc(var(--d-op, 1) * (1 - var(--say-out, 0)));
               transform:translate(calc(var(--fx, 0) * var(--field-w) * var(--say-out, 0)),
                                   calc(var(--say-out, 0) * 460px))
                         scale(calc(var(--d-scale, 1) * (1 - 0.68 * var(--say-out, 0)))); }"""
new = """               opacity:calc(var(--d-op, 1) * var(--fall-o, 1));
               transform:translate(calc(var(--fx, 0) * var(--field-w) * var(--fall, 0)),
                                   var(--fall-px, 0px))
                         scale(calc(var(--d-scale, 1) * (1 - 0.7 * var(--fall, 0)))); }"""
assert old in s, 'box fall rule changed'
s = s.replace(old, new, 1)

old = """        // and past the landing it leaves again, over the next 520px
        var past = (window.scrollY - landing) / 520;
        root.style.setProperty('--say-out', Math.min(1, Math.max(0, past)).toFixed(3));"""
new = """        // and past the landing it leaves again, over the next 520px
        var past = (window.scrollY - landing) / 520;
        root.style.setProperty('--say-out', Math.min(1, Math.max(0, past)).toFixed(3));

        // The boxes keep going, all the way into the window: the drop is the
        // real distance between the two, run over the scroll between the
        // statement landing and the window centring.
        if (win) {
          var wb = win.getBoundingClientRect();
          var fieldY = window.scrollY + box.top + box.height / 2;
          var winY = window.scrollY + wb.top + wb.height / 2;
          var winLanding = winY - window.innerHeight / 2;
          var f = (window.scrollY - landing) / Math.max(1, winLanding - landing);
          f = Math.min(1, Math.max(0, f));
          root.style.setProperty('--fall', f.toFixed(4));
          root.style.setProperty('--fall-px', ((winY - fieldY) * f).toFixed(1) + 'px');
          // full strength until the last fifth of the journey
          root.style.setProperty('--fall-o',
            Math.min(1, Math.max(0, (1 - f) / 0.2)).toFixed(3));
        }"""
assert old in s, 'exit assignment changed'
s = s.replace(old, new, 1)

old = """    var next = document.querySelector('.rec-next');"""
new = """    var next = document.querySelector('.rec-next');
    var win = document.querySelector('.rec-win');"""
assert old in s, 'script head changed'
s = s.replace(old, new, 1)

old = """      .rec-box { transform:scale(var(--d-scale, 1)); opacity:var(--d-op, 1); }"""
assert old in s, 'reduced-motion box rule changed'
io.open(p, 'w', encoding='utf-8').write(s)
print('the fall now reaches the window')
