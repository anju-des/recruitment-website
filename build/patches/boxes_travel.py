# -*- coding: utf-8 -*-
"""The boxes come down with the scroll instead of switching on.

They fade in from the first scroll and travel downward into place, arriving
exactly as the statement reaches the middle of the screen. One progress value
drives both, so they can't fall out of step with it.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- the field moves; the boxes keep their own depth and float ------------
old = """    .rec-boxes { position:absolute; left:50%; top:50%; translate:-50% -50%;
                 width:min(1200px, 92vw); height:1000px; pointer-events:none; }"""
new = """    /* The field fades in from the first scroll and slides down into place,
       landing as the statement centres. --rec-q runs 0 to 1 over exactly that
       stretch of scroll. */
    .rec-boxes { position:absolute; left:50%; top:50%; translate:-50% -50%;
                 width:min(1200px, 92vw); height:1000px; pointer-events:none;
                 opacity:var(--rec-q, 0);
                 transform:translateY(calc((1 - var(--rec-q, 0)) * -260px)); }
    @media (prefers-reduced-motion: reduce) {
      .rec-boxes { opacity:1; transform:none; }
    }"""
assert old in s, 'box field rule changed'
s = s.replace(old, new, 1)

old = """               animation:rec-box-float 9s ease-in-out infinite;
               opacity:0; transition:opacity .9s ease; }"""
new = """               animation:rec-box-float 9s ease-in-out infinite; }"""
assert old in s, 'box rule changed'
s = s.replace(old, new, 1)

old = """    .rec-box--d1 { filter:blur(2px); transform:scale(.94);
                   animation-duration:11s; animation-delay:-3s; }
    .rec-box--d2 { filter:blur(4px); transform:scale(.88);
                   animation-duration:13s; animation-delay:-6s; }"""
new = """    .rec-box--d1 { opacity:.7; filter:blur(2px); transform:scale(.94);
                   animation-duration:11s; animation-delay:-3s; }
    .rec-box--d2 { opacity:.45; filter:blur(4px); transform:scale(.88);
                   animation-duration:13s; animation-delay:-6s; }"""
assert old in s, 'depth rules changed'
s = s.replace(old, new, 1)

# the class-driven reveal and its stagger are no longer used
start = s.index("    /* they arrive well before the statement does")
end = s.index("    @keyframes rec-box-float")
block = s[start:end]
assert 'boxes-in' in block, 'box reveal block changed'
s = s[:start] + s[end:]

m = re.search(r'\n  // The boxes come in early.*?\n  \}\(\)\);\n', s, re.S)
assert m, 'box observer not found'
s = s[:m.start()] + '\n' + s[m.end():]
assert 'boxes-in' not in s, 'a boxes-in reference is left'

# ---- the progress value -----------------------------------------------------
old = """      root.style.setProperty('--sky-glow', (1 - c).toFixed(3));"""
new = """      root.style.setProperty('--sky-glow', (1 - c).toFixed(3));

      // 0 at the top of the page, 1 when the statement sits centred: the
      // stretch of scroll the boxes travel over
      if (say) {
        var box = say.getBoundingClientRect();
        var landing = window.scrollY + box.top + box.height / 2 - window.innerHeight / 2;
        var q = landing > 0 ? Math.min(1, Math.max(0, window.scrollY / landing)) : 1;
        root.style.setProperty('--rec-q', q.toFixed(3));
      }"""
assert old in s, 'glow assignment changed'
s = s.replace(old, new, 1)

old = """    var hero = document.querySelector('.rec-hero');
    var head = document.querySelector('.rec-head');"""
new = """    var hero = document.querySelector('.rec-hero');
    var head = document.querySelector('.rec-head');
    var say = document.querySelector('.rec-say');"""
assert old in s, 'script head changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('boxes travel down with the scroll')
