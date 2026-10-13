# -*- coding: utf-8 -*-
"""Run the handover while the frame is still pinned.

The pin releases exactly one screen before the closing section's top, so
bands timed off that top were firing after the frame had already started
scrolling away. Everything now plays out inside the pin and comes to rest
just as it lets go: the window travels down, the heading comes up above it,
and the sky lightens around them.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """        back = (window.scrollY - (ct - window.innerHeight)) / window.innerHeight;
        back = Math.min(1, Math.max(0, back));
        var vh = window.innerHeight;
        // first the window travels down the screen...
        var down = (window.scrollY - (ct - vh * 1.15)) / (vh * 0.55);
        root.style.setProperty('--win-down', Math.min(1, Math.max(0, down)).toFixed(3));
        // ...and only once it has settled does the heading come up above it
        var cin = (window.scrollY - (ct - vh * 0.5)) / (vh * 0.55);
        root.style.setProperty('--close-in', Math.min(1, Math.max(0, cin)).toFixed(3));"""
new = """        var vh = window.innerHeight;
        // measured back from the closing section's top, which is one screen
        // past the moment the pinned frame lets go
        var band = function (a, b) {
          return Math.min(1, Math.max(0,
            (window.scrollY - (ct - vh * a)) / (vh * (a - b)))).toFixed(3);
        };
        back = parseFloat(band(2.5, 1.5));      // the sky lightens
        root.style.setProperty('--win-down', band(2.4, 1.85));   // window drops
        root.style.setProperty('--close-in', band(1.9, 1.35));   // then the words"""
assert old in s, 'closing bands changed'
s = s.replace(old, new, 1)

# a short light runway after the frame lets go, instead of a screenful of nothing
old = "    .rec-close { position:relative; min-height:120vh; }"
new = "    .rec-close { position:relative; min-height:70vh; }"
assert old in s, 'closing section rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('handover plays inside the pin')
