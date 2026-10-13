# -*- coding: utf-8 -*-
"""Two things: clear the inherited page CSS, and put a gradient on the page.

The shell was copied from the BGV page, so it still carried that page's own
styles -- hero, plan cards, price lines, faq, and overrides on .wm-option-card.
With nothing left to style they are dead weight, and the .wm- overrides would
quietly restyle standard components the moment one is used again. Only the
column itself stays.

The background becomes a light blue-to-purple wash. Purple is outside the
Wisemonk palette, so the linter will flag it -- noted for the user.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- drop the inherited page styles ---------------------------------------
patch = '''
# The shell is the BGV page's, so it carries that page's own styles: hero,
# plan cards, price, faq and a set of .wm-option-card overrides. Nothing on
# this page uses them, and the .wm- ones would restyle a standard component
# the moment it is used -- so the whole block goes, bar the column itself.
m = re.search(r'    /\\* Page-specific layout.*?(?=  </style>)', shell, re.S)
assert m, 'page-specific css block not found in the shell'
shell = shell[:m.start()] + """    /* Page layout */
    .rec-wrap { width:100%; display:flex; flex-direction:column; gap:20px; }

    @media (max-width:1000px) {
      .content { padding:8px 20px 40px; }
    }

""" + shell[m.end():]
'''

anchor = "# ---------------------------------------------------------------- extra icons"
assert anchor in s, 'builder layout changed'
s = s.replace(anchor, patch.lstrip('\n') + '\n' + anchor, 1)

# ---- the gradient ----------------------------------------------------------
old = '    /* ---- landing layout ---------------------------------------------- */\n'
new = """    /* ---- page ground --------------------------------------------------- */
    /* A light wash from the palette's lightest blue into a soft violet. The
       violet is outside the Wisemonk palette and is here by request; it is
       fixed to the viewport so the tint doesn't band as the page scrolls. */
    body { background:linear-gradient(155deg,
             #EEF4FF 0%, #ECF0FF 28%, #F0ECFF 62%, #F6F0FF 100%);
           background-attachment:fixed; }

""" + old
assert old in s, 'landing layout marker moved'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('shell cleaned; gradient ground added')
