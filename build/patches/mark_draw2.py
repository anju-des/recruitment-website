# -*- coding: utf-8 -*-
"""Draw the real mark, not a trace of it.

My first attempt used the traced path AS the artwork, and the trace was not
good enough -- it came out a flattened S. The shape now comes from the logo
itself, masked over the metallic gradient, and the traced path is demoted to
a mask that gates how much of it is revealed. A rough path is fine for that:
every edge you see is still the real logo, the path only decides how far
along the loop the reveal has got.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

src = io.open('C:/Users/bharg/OneDrive/Desktop/MCP/EOR/docs/mira-mark.svg',
              encoding='utf-8').read()
m = re.search(r'xlink:href="(data:image/png;base64,[^"]+)"', src)
assert m, 'could not find the embedded bitmap in mira-mark.svg'
png = m.group(1)

# a centreline through the loop: in at the lower-right free end, round the
# right lobe, across the middle, round the left lobe, out at the top left
PATH = ('M236 214 '
        'C276 222 322 196 332 152 '
        'C342 108 308 78 270 92 '
        'C238 104 220 130 206 150 '
        'C192 170 172 196 142 208 '
        'C104 222 68 194 72 148 '
        'C76 104 100 82 128 86')

MARKUP = """            <span class="rec-orb-mark" role="img" aria-label="Mira">
              <svg class="rec-orb-face" viewBox="0 0 412 300" aria-hidden="true">
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
                  <!-- the logo's own alpha, so every edge is the real mark -->
                  <mask id="rec-logo" style="mask-type:alpha">
                    <image x="0" y="0" width="412" height="300"
                           href="%s"/>
                  </mask>
                  <!-- and the loop that gates how much of it has arrived -->
                  <mask id="rec-draw">
                    <path class="rec-orb-path" pathLength="1" d="%s"/>
                  </mask>
                </defs>
                <g mask="url(#rec-draw)">
                  <rect width="412" height="300" fill="url(#rec-metal)"
                        mask="url(#rec-logo)"/>
                </g>
              </svg>
            </span>""" % (png, PATH)

start = s.index('            <span class="rec-orb-mark" role="img" aria-label="Mira">')
end = s.index('</span>', s.index('rec-orb-path', start)) + len('</span>')
old = s[start:end]
assert 'rec-orb-face' in old, 'mark markup changed'
s = s[:start] + MARKUP + s[end:]

old = """    .rec-orb-path { fill:none; stroke:url(#rec-metal); stroke-width:31;
                    stroke-linecap:round; stroke-linejoin:round;
                    /* pathLength 1 makes the draw a plain 1 to 0 ramp */
                    stroke-dasharray:1;
                    stroke-dashoffset:calc(1 - var(--draw, 0)); }"""
new = """    /* wide enough to clear the mark's own stroke either side of the line */
    .rec-orb-path { fill:none; stroke:#FFFFFF; stroke-width:104;
                    stroke-linecap:round; stroke-linejoin:round;
                    /* pathLength 1 makes the draw a plain 1 to 0 ramp */
                    stroke-dasharray:1;
                    stroke-dashoffset:calc(1 - var(--draw, 0)); }"""
assert old in s, 'path rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('the real mark, revealed along the loop')
