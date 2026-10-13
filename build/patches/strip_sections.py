# -*- coding: utf-8 -*-
"""Clear the page back to the hero.

Everything below the hero comes out -- portal, flow, integrations, promises,
stats, plans, faq, closing cta -- along with the CSS and the script that only
those sections used. What stays: the page shell, the landing layout, the hero
and its composer, and the 48px section padding.

The full version is backed up next to this script before anything is cut.
"""
import io
import shutil

p = 'build_recruitment_page.py'
shutil.copyfile(p, 'build_recruitment_page.full.py')
shutil.copyfile('C:/Users/bharg/OneDrive/Desktop/MCP/EOR/docs/recruitment-copy.html',
                'recruitment-copy.full.html')

s = io.open(p, encoding='utf-8').read()


def cut(start, end, keep_end=True, label=''):
    """Drop everything from `start` up to `end`."""
    global s
    assert s.count(start) == 1, 'start marker not unique: ' + (label or start[:40])
    i = s.index(start)
    j = s.index(end, i)
    s = s[:i] + (end if keep_end else '') + s[j + len(end):]


# ---- markup: hero only -----------------------------------------------------
cut('\n        <!-- PORTAL -->', '\n      </div>\n    </div>\n  </div>\n</div>',
    label='portal..close')

# the observer only ever drove the portal image
cut('\n\n<script>\n  // Pop the portal in', '\n</script>\n', keep_end=False,
    label='portal script')

# ---- css -------------------------------------------------------------------
# the portal block sits between the landing layout and the composer
cut('\n\n    /* the portal under the hero copy,',
    '\n    /* ---- hero composer', label='portal css')

# everything from the flow down to the shared section padding, which stays
cut('\n    /* ---- posted role to signed offer',
    '\n    /* one padding for every section', label='section css')

# the coloured panels those sections used are gone
cut('\n\n    /* the two coloured panels are objects on the page rather than full-bleed',
    '\n\n    @media (max-width:1000px) {', label='panel margins')

# ---- the media queries keep only what still has an element ----------------
i = s.index('    @media (max-width:1000px) {')
j = s.index('"""', i)
s = s[:i] + """    @media (max-width:1000px) {
      .rec-wrap > section { padding:32px 24px; }
    }
    @media (max-width:640px) {
      .rec-compose-foot { flex-direction:column; align-items:stretch; }
      .rec-compose-post { width:100%; }
    }
""" + s[j:]

# ---- no sprite icons are drawn any more ------------------------------------
i = s.index('NEEDED = [')
j = s.index('\n', i)
s = s[:i] + "NEEDED = []  # the composer carries its own inline icons" + s[j:]

io.open(p, 'w', encoding='utf-8').write(s)

for dead in ('rec-flow', 'rec-tile', 'rec-promise', 'rec-stat', 'rec-tier',
             'rec-faq', 'rec-cta-band', 'rec-shot', 'rec-band'):
    assert dead not in s, 'leftover reference to ' + dead
print('stripped to the hero; backup at build_recruitment_page.full.py')
