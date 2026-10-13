# -*- coding: utf-8 -*-
"""The hero: one line, centred in the viewport, set in Inter.

Inter replaces Satoshi across the page by request -- it is outside the
Wisemonk type system, so the linter will say so.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- the typeface ----------------------------------------------------------
old = ("shell = shell.replace('<h1>Background Verification</h1>', "
       "'<h1>Recruitment Support</h1>')")
assert old in s, 'shell title anchor moved'
patch = old + '''

# Inter, by request, in place of Satoshi across this page
INTER = ('  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\\n'
         '  <link href="https://fonts.googleapis.com/css2?'
         'family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">\\n')
_sat = ('  <link href="https://api.fontshare.com/v2/css?'
        'f[]=satoshi@700,500,400&display=swap" rel="stylesheet">\\n')
assert _sat in shell, 'font link changed in the shell'
shell = shell.replace(_sat, _sat + INTER, 1)'''
s = s.replace(old, patch, 1)

# ---- markup ----------------------------------------------------------------
old = '      <div class="rec-wrap">\n'
new = '''      <div class="rec-wrap">

        <!-- HERO -->
        <section class="rec-hero">
          <h1>Hire the right talent, anywhere in the world.</h1>
          <p class="rec-hero-sub">A dedicated recruiter opens your role in the market you are
          hiring in, and Mira AI ranks every application against your scorecard as it
          arrives. You pay only when someone joins.</p>
        </section>
'''
assert s.count(old) == 1, 'wrap opening moved'
s = s.replace(old, new, 1)

# ---- css -------------------------------------------------------------------
old = '    /* ---- landing layout ---------------------------------------------- */\n'
new = """    /* ---- type ------------------------------------------------------------ */
    /* Inter by request, in place of the system's Satoshi */
    body, .wm-btn, input, textarea, select, button {
      font-family:'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif; }

    /* ---- hero ------------------------------------------------------------ */
    /* one line held in the middle of the first screen, nothing else competing */
    .rec-hero { min-height:calc(100vh - var(--rec-chrome)); display:flex;
                flex-direction:column; align-items:center; justify-content:center;
                text-align:center; }
    .rec-hero h1 { max-width:20ch; font-size:60px; font-weight:700; line-height:1.06;
                   letter-spacing:-0.035em; color:var(--grey-700); text-wrap:balance; }
    .rec-hero-sub { max-width:62ch; margin-top:22px; font-size:18px; font-weight:400;
                    line-height:1.6; color:var(--text-secondary); text-wrap:pretty; }
    @media (max-width:1000px) {
      .rec-hero h1 { font-size:40px; letter-spacing:-0.03em; }
      .rec-hero-sub { font-size:16px; margin-top:18px; }
    }

""" + old
assert old in s, 'landing layout marker moved'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('hero added')
