# -*- coding: utf-8 -*-
"""Nav items beside the Log in button.

Three of them carry a chevron, so they are buttons rather than links -- the
menus they imply are not built yet, and a link that goes nowhere is worse
than a control that has not been wired. Pricing is a real link.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

CHEVRON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
           'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
           '<path d="M6 9.5l6 6 6-6"/></svg>')

items = '\n'.join(
    '            <button type="button" class="rec-nav-item">%s %s</button>' % (label, CHEVRON)
    for label in ('Platform', 'Solutions', 'Resources'))

old = """        <a class="rec-login" href="#login">Log in</a>
      </header>"""
new = """        <div class="rec-head-right">
          <nav class="rec-nav" aria-label="Main">
%s
            <a class="rec-nav-item" href="#pricing">Pricing</a>
          </nav>
          <a class="rec-login" href="#login">Log in</a>
        </div>
      </header>""" % items
assert old in s, 'header markup changed'
s = s.replace(old, new, 1)

old = '    /* same near-black as the field\'s action, so the two read as one family */'
new = """    .rec-head-right { display:flex; align-items:center; gap:28px; }
    .rec-nav { display:flex; align-items:center; gap:24px; }
    .rec-nav-item { display:inline-flex; align-items:center; gap:5px; cursor:pointer;
                    background:none; border:none; padding:6px 0; font-family:inherit;
                    font-size:14.5px; font-weight:400; color:var(--text-primary);
                    transition:color .12s; }
    .rec-nav-item:hover { color:var(--primary-600); }
    .rec-nav-item svg { width:13px; height:13px; color:var(--text-muted); }

""" + old
assert old in s, 'login comment moved'
s = s.replace(old, new, 1)

old = '      .rec-login { height:34px; padding:0 14px; font-size:13.5px; }'
new = (old + '\n'
       '      /* no room for the nav beside the logo; it needs a menu of its own */\n'
       '      .rec-nav { display:none; }')
assert old in s, 'responsive login rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('nav added')
