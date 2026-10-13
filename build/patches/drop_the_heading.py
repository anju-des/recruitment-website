# -*- coding: utf-8 -*-
"""The heading goes, and with it the reason the window moved at all.

The downward travel and the shrink were both only there to clear space at
the top of the frame. With nothing to clear, the windows stay centred and
at full size -- the only thing the closing scroll does now is bring the
light up and slide the row across.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = '          <h2 class="rec-close-h">Mira at every stage</h2>\n'
assert old in s, 'heading markup changed'
s = s.replace(old, '', 1)

old = """    /* it sits in the upper part of the pinned frame, above the window, and
       only once --close-in starts -- which is after the window has moved */
    .rec-close-h { position:absolute; top:9vh; left:50%; translate:-50% 0;
                   width:min(92vw, 900px); text-align:center;
                   max-width:18ch; font-size:clamp(30px, 2.4vw + 14px, 58px);
                   font-weight:600; line-height:1.1; letter-spacing:-0.03em;
                   color:var(--grey-700); text-wrap:balance;
                   margin-inline:auto;
                   opacity:var(--close-in, 0);
                   transform:translateY(calc((1 - var(--close-in, 0)) * 40px)); }
    @media (prefers-reduced-motion: reduce) {
      .rec-close-h { opacity:1; transform:none; }
    }
"""
assert old in s, 'heading rule changed'
s = s.replace(old, '', 1)

old = """      .rec-close { min-height:40vh; }
      .rec-close-h { position:static; translate:none; opacity:1; transform:none;
                     margin:0 auto 32px; }"""
new = "      .rec-close { min-height:40vh; }"
assert old in s, 'responsive closing rule changed'
s = s.replace(old, new, 1)

# ---- the windows stay centred, and full size -------------------------------
old = """                transform:scale(calc(1 - 0.06 * var(--win-down, 0)))
                          translateX(calc((1 - var(--wins, 0)) * (50% - 270px)))
                          translateY(calc(var(--win-down, 0) * 8vh)); }"""
new = """                transform:translateX(calc((1 - var(--wins, 0)) * (50% - 270px))); }"""
assert old in s, 'row transform changed'
s = s.replace(old, new, 1)

old = "    .rec-win { flex:none; width:540px; height:min(660px, calc(100vh - 190px));"
new = "    .rec-win { flex:none; width:540px; height:min(720px, calc(100vh - 110px));"
assert old in s, 'window height changed'
s = s.replace(old, new, 1)

old = """        root.style.setProperty('--close-in', band(2.9, 2.35));   // then the words
"""
assert old in s, 'closing bands changed'
s = s.replace(old, '', 1)

old = """        root.style.setProperty('--win-down', band(3.4, 2.85));   // window drops
        // once it has arrived in the light, it drops the dark treatment"""
new = """        // once the sky is light, the window drops the dark treatment"""
assert old in s, 'win-down line changed'
s = s.replace(old, new, 1)

assert 'rec-close-h' not in s, 'a heading reference is left'
assert '--close-in' not in s, 'a close-in reference is left'
assert '--win-down' not in s.split("if (win)")[0].split('back = parseFloat')[1], 'win-down still set'

io.open(p, 'w', encoding='utf-8').write(s)
print('heading removed; the row stays centred at full size')
