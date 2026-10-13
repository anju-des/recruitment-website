# -*- coding: utf-8 -*-
"""Scrolling lifts the hero away and turns the page dark.

One scroll progress value (0 at the top, 1 by the time the hero is 70% gone)
drives three things: the content rises, it fades, and a fixed dark sheet
comes up over the light background and the violet glow with it. The sheet
sits above the glow but below the content and the header, so the words stay
readable right up to the moment they have faded out.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- markup ----------------------------------------------------------------
old = '      <header class="rec-head">'
new = ('      <div class="rec-dark" aria-hidden="true"></div>\n\n'
       '      <header class="rec-head">')
assert old in s, 'header markup moved'
s = s.replace(old, new, 1)

# wrap everything the hero holds, so one element carries the lift and fade
m = re.search(r'(        <section class="rec-hero">\n)(.*?)(        </section>\n)', s, re.S)
assert m, 'hero section not found'
inner = '          <div class="rec-hero-inner">\n' + m.group(2) + '          </div>\n'
s = s[:m.start(2)] + inner + s[m.end(2):]

# ---- css -------------------------------------------------------------------
old = '    /* ---- header ------'
new = """    /* ---- scrolling into the dark --------------------------------------- */
    /* One sheet over the whole viewport. It is above the hero's glow and
       below the content, so the page darkens while the words are still
       legible on their way out. */
    .rec-dark { position:fixed; inset:0; z-index:0; pointer-events:none;
                background:#0B0F19; opacity:var(--rec-dark, 0); }
    .rec-head { position:relative; z-index:2; }
    .rec-wrap { position:relative; z-index:1; }
    .rec-hero-inner { display:flex; flex-direction:column; align-items:center;
                      width:100%;
                      transform:translateY(calc(var(--rec-lift, 0) * -1px));
                      opacity:var(--rec-fade, 1);
                      will-change:transform, opacity; }
    @media (prefers-reduced-motion: reduce) {
      .rec-hero-inner { transform:none; opacity:1; }
    }

""" + old
assert old in s, 'header css marker moved'
s = s.replace(old, new, 1)

# ---- script ----------------------------------------------------------------
m = re.search(r'(\n  \}\(\)\);\n)</script>\n', s)
assert m, 'script close not found'

ADD = """
  // Scroll progress drives the hero's exit and the dark sheet behind it.
  (function () {
    var hero = document.querySelector('.rec-hero');
    var root = document.documentElement;
    if (!hero) return;
    var ticking = false;

    function update() {
      var span = Math.max(1, hero.offsetHeight * 0.7);
      var p = Math.min(1, Math.max(0, window.scrollY / span));
      root.style.setProperty('--rec-lift', (p * 150).toFixed(2));
      root.style.setProperty('--rec-fade', (1 - Math.min(1, p * 1.25)).toFixed(3));
      root.style.setProperty('--rec-dark', (p * 0.96).toFixed(3));
      ticking = false;
    }

    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(update);
    }, { passive: true });
    window.addEventListener('resize', update);
    update();
  }());
"""
s = s[:m.end(1)] + ADD + '</script>\n' + s[m.end():]

io.open(p, 'w', encoding='utf-8').write(s)
print('hero exit + dark sheet wired')
