# -*- coding: utf-8 -*-
"""The loop draws itself: from the bottom-right end, round and out to the top left.

A stroke can only be drawn if there is a path to draw, and the mark we have
is a bitmap -- so the shape is now a traced vector of it. The stroke carries
the same metallic gradient, the wrapper still casts the body, and the draw
runs on its own scroll band after the light has opened.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# traced from the mark: one continuous stroke with two free ends, starting at
# the lower-right so the loop closes through the centre and opens top-left
PATH = ('M232 206 '
        'C268 220 318 198 330 156 '
        'C342 110 310 80 272 92 '
        'C240 102 222 128 206 150 '
        'C190 172 170 198 138 208 '
        'C100 220 66 196 70 148 '
        'C74 104 96 84 124 88')

MARKUP = """            <span class="rec-orb-mark" role="img" aria-label="Mira">
              <svg class="rec-orb-face" viewBox="0 0 412 300" fill="none"
                   aria-hidden="true">
                <defs>
                  <linearGradient id="rec-metal" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0" stop-color="#FFFFFF"/>
                    <stop offset="0.14" stop-color="#EFE9FF"/>
                    <stop offset="0.27" stop-color="#9B88E2"/>
                    <stop offset="0.38" stop-color="#6E5CB8"/>
                    <stop offset="0.5" stop-color="#FDFBFF"/>
                    <stop offset="0.62" stop-color="#8C7ACF"/>
                    <stop offset="0.76" stop-color="#E4DBFF"/>
                    <stop offset="0.88" stop-color="#7E6BC6"/>
                    <stop offset="1" stop-color="#FFFFFF"/>
                  </linearGradient>
                </defs>
                <path class="rec-orb-path" pathLength="1" d="%s"/>
              </svg>
            </span>""" % PATH

start = s.index('            <span class="rec-orb-mark" role="img" aria-label="Mira">')
end = s.index('</span>', s.index('rec-orb-face', start)) + len('</span>')
old = s[start:end]
assert 'rec-orb-face' in old, 'mark markup changed'
s = s[:start] + MARKUP + s[end:]

old_start = s.index('    /* polish is light, dark, light again across the form */')
old_end = s.index('    @media (prefers-reduced-motion: reduce) {', old_start)
old = s[old_start:old_end]
assert 'mira-mark.svg' in old, 'face rule changed'

new = """    /* polish is light, dark, light again along the form */
    .rec-orb-face { display:block; width:100%; height:100%; overflow:visible; }
    .rec-orb-path { fill:none; stroke:url(#rec-metal); stroke-width:31;
                    stroke-linecap:round; stroke-linejoin:round;
                    /* pathLength 1 makes the draw a plain 1 to 0 ramp */
                    stroke-dasharray:1;
                    stroke-dashoffset:calc(1 - var(--draw, 0)); }

"""
s = s[:old_start] + new + s[old_end:]

old = """      .rec-orb-face { animation:none; }"""
new = """      .rec-orb-path { stroke-dashoffset:0; }"""
assert old in s, 'reduced motion rule changed'
s = s.replace(old, new, 1)

# the sheen keyframes sat inside the block just replaced, so they are already
# gone with the gradient background they drove
assert 'rec-sheen' not in s, 'a sheen reference is left'

# ---- the draw runs after the light has opened ------------------------------
old = """        // the light leaves over the last stretch, once it is fully open
        root.style.setProperty('--orb-out',
          Math.min(1, Math.max(0, (q - 0.76) / 0.24)).toFixed(3));"""
new = """        // the loop draws itself once the mark is there
        root.style.setProperty('--draw',
          Math.min(1, Math.max(0, (q - 0.44) / 0.34)).toFixed(3));
        // the light leaves over the last stretch, once it is fully open
        root.style.setProperty('--orb-out',
          Math.min(1, Math.max(0, (q - 0.76) / 0.24)).toFixed(3));"""
assert old in s, 'orb-out band changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('the loop draws itself')
