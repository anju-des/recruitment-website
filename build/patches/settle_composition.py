# -*- coding: utf-8 -*-
"""Even out the resting frame and stop the page drifting into blank light."""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = "                transform:translateY(calc(var(--win-down, 0) * 15vh))"
new = "                transform:translateY(calc(var(--win-down, 0) * 13vh))"
assert old in s
s = s.replace(old, new, 1)

old = "    .rec-close-h { position:absolute; top:11vh; left:50%; translate:-50% 0;"
new = "    .rec-close-h { position:absolute; top:14vh; left:50%; translate:-50% 0;"
assert old in s
s = s.replace(old, new, 1)

# a short tail: the frame lets go near the foot of the page, so the pair is
# still on screen when the scrolling runs out
old = "    .rec-close { position:relative; min-height:70vh; }"
new = "    .rec-close { position:relative; min-height:35vh; }"
assert old in s
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('composition settled')
