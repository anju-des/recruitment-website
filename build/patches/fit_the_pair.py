# -*- coding: utf-8 -*-
"""Size the resting composition so the heading has room above the window."""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """                transform:translateY(calc(var(--win-down, 0) * 34vh))
                          scale(calc(1 - 0.12 * var(--win-down, 0))); }"""
new = """                transform:translateY(calc(var(--win-down, 0) * 15vh))
                          scale(calc(1 - 0.30 * var(--win-down, 0))); }"""
assert old in s, 'row transform changed'
s = s.replace(old, new, 1)

old = "    .rec-close-h { position:absolute; top:16vh; left:50%; translate:-50% 0;"
new = "    .rec-close-h { position:absolute; top:11vh; left:50%; translate:-50% 0;"
assert old in s, 'heading placement changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('composition fitted')
