# -*- coding: utf-8 -*-
"""A sticky header that becomes a glass bar once the page moves.

At the top it is bare, sitting straight on the page. As soon as anything
scrolls it gathers into a translucent, blurred container. And because the
page turns dark underneath it, the bar has a night state too -- dark glass,
light type, inverted logo, inverted button -- or it would go invisible the
moment the sky changes.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- markup: one inner element to carry the glass --------------------------
m = re.search(r'(      <header class="rec-head">\n)(.*?)(      </header>\n)', s, re.S)
assert m, 'header markup not found'
inner = ('        <div class="rec-head-inner">\n'
         + m.group(2).replace('\n        ', '\n          ').rstrip() + '\n'
         + '        </div>\n')
s = s[:m.start(2)] + inner + s[m.end(2):]

# ---- css -------------------------------------------------------------------
old = """    /* content sits above the sky; the header above that, and it leaves on
       the same fade so nothing is left floating over the dark */
    .rec-head { position:relative; z-index:2; opacity:var(--rec-fade, 1); }"""
new = """    /* content sits above the sky; the header rides above it and stays */
    .rec-head { position:sticky; top:0; z-index:5; }"""
assert old in s, 'header layering rule changed'
s = s.replace(old, new, 1)

old = """    /* ---- header ---------------------------------------------------------- */
    .rec-head { display:flex; align-items:center; justify-content:space-between;
                height:72px; padding:0 48px; }"""
new = """    /* ---- header ---------------------------------------------------------- */
    .rec-head { padding:10px 24px; }
    .rec-head-inner { position:relative; max-width:1240px; margin-inline:auto;
                      display:flex; align-items:center; justify-content:space-between;
                      height:60px; padding:0 24px; border-radius:14px;
                      transition:background .3s, box-shadow .3s, backdrop-filter .3s; }
    /* the glass only appears once the page has moved */
    .rec-head.is-stuck .rec-head-inner {
      background:rgba(255,255,255,.70);
      -webkit-backdrop-filter:saturate(165%) blur(14px);
      backdrop-filter:saturate(165%) blur(14px);
      box-shadow:0 10px 30px rgba(18,22,32,.10), inset 0 0 0 1px rgba(255,255,255,.65); }
    /* after dark the same bar flips: dark glass, light type */
    .rec-head.is-stuck.is-night .rec-head-inner {
      background:rgba(16,19,32,.60);
      box-shadow:0 10px 30px rgba(0,0,0,.38), inset 0 0 0 1px rgba(255,255,255,.10); }
    .rec-head.is-night .rec-nav-item { color:#E8EAF2; }
    .rec-head.is-night .rec-nav-item:hover { color:#FFFFFF; }
    .rec-head.is-night .rec-nav-item svg { color:#9AA2B8; }
    .rec-head.is-night .rec-logo img { filter:invert(1) brightness(1.7); }
    .rec-head.is-night .rec-login { background:#FFFFFF; color:#0F172A; }
    .rec-head.is-night .rec-login:hover { background:#E8EAF2; }
    .rec-logo img, .rec-nav-item, .rec-login {
      transition:filter .25s, color .25s, background .25s; }"""
assert old in s, 'header rule changed'
s = s.replace(old, new, 1)

old = '      .rec-head { height:64px; padding:0 24px; }'
new = ('      .rec-head { padding:8px 14px; }\n'
       '      .rec-head-inner { height:54px; padding:0 14px; }')
assert old in s, 'responsive header rule changed'
s = s.replace(old, new, 1)

# ---- script: tell the bar when it is stuck, and when it is night -----------
old = """    var hero = document.querySelector('.rec-hero');
    var root = document.documentElement;"""
new = """    var hero = document.querySelector('.rec-hero');
    var head = document.querySelector('.rec-head');
    var root = document.documentElement;"""
assert old in s, 'script head changed'
s = s.replace(old, new, 1)

old = """      root.style.setProperty('--sky-glow', (1 - c).toFixed(3));"""
new = """      root.style.setProperty('--sky-glow', (1 - c).toFixed(3));
      if (head) {
        head.classList.toggle('is-stuck', window.scrollY > 8);
        head.classList.toggle('is-night', c > 0.5);
      }"""
assert old in s, 'glow assignment changed'
s = s.replace(old, new, 1)

# the hero sits under a sticky bar now, so it should not also reserve its height
old = '    "--rec-chrome:80px;", 1)'
new = '    "--rec-chrome:0px;", 1)'
assert old in s, 'chrome token changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('sticky glass header')
