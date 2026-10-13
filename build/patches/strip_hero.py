# -*- coding: utf-8 -*-
"""Take the hero out too, leaving an empty page to build on.

What's left is the shell, the empty .rec-wrap column, and the two rules that
set how sections stack in it: the 54px gap and the 48px padding.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

start = '\n        <!-- HERO -->'
end = '\n\n      </div>\n    </div>\n  </div>\n</div>'
assert s.count(start) == 1 and s.count(end) == 1, 'hero markers moved'
i, j = s.index(start), s.index(end)
s = s[:i] + s[j:]

# the hero's own layout, and the composer field it held
css_start = '    /* the hero lost its illustration'
css_end = '\n    /* one padding for every section'
assert css_start in s and css_end in s, 'hero css markers moved'
s = s[:s.index(css_start)] + s[s.index(css_end) + 1:]

# the only responsive rules left were the composer's
old = """    @media (max-width:640px) {
      .rec-compose-foot { flex-direction:column; align-items:stretch; }
      .rec-compose-post { width:100%; }
    }
"""
assert old in s, 'composer media query changed'
s = s.replace(old, '', 1)

io.open(p, 'w', encoding='utf-8').write(s)

for dead in ('rec-hero', 'rec-compose', 'hero-grid', 'hero-left', 'Mira AI'):
    assert dead not in s, 'leftover reference to ' + dead
print('hero removed; the page is an empty column now')
