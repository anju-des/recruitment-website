# -*- coding: utf-8 -*-
"""Geist in place of Inter, set the way the reference sets it, and the last
word carried in a blue-to-violet gradient.

The reference runs its headline at weight 500 with -0.03em tracking, not bold
-- that lightness is most of why it reads the way it does.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- the typeface ----------------------------------------------------------
old = """INTER = ('  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\\n'
         '  <link href="https://fonts.googleapis.com/css2?'
         'family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">\\n')"""
new = """INTER = ('  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\\n'
         '  <link href="https://fonts.googleapis.com/css2?'
         'family=Geist:wght@400;500;600;700&display=swap" rel="stylesheet">\\n')"""
assert old in s, 'font link patch changed'
s = s.replace(old, new, 1)
s = s.replace('# Inter, by request, in place of Satoshi across this page',
              '# Geist, by request, in place of Satoshi across this page', 1)

old = """    /* Inter by request, in place of the system's Satoshi */
    body, .wm-btn, input, textarea, select, button {
      font-family:'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif; }"""
new = """    /* Geist by request, in place of the system's Satoshi */
    body, .wm-btn, input, textarea, select, button {
      font-family:'Geist', system-ui, -apple-system, 'Segoe UI', sans-serif; }"""
assert old in s, 'font-family rule changed'
s = s.replace(old, new, 1)

# ---- the headline ----------------------------------------------------------
old = """    .rec-hero h1 { max-width:20ch; font-size:60px; font-weight:700; line-height:1.06;
                   letter-spacing:-0.035em; color:var(--grey-700); text-wrap:balance; }"""
new = """    .rec-hero h1 { max-width:20ch; font-size:60px; font-weight:500; line-height:1.06;
                   letter-spacing:-0.03em; color:var(--grey-700); text-wrap:balance; }
    /* the closing word carries the page's own blue-to-violet wash. Painted
       through the text, with a solid colour behind it for anything that
       cannot clip a background to a glyph. */
    .rec-grad { color:var(--primary-600);
                background:linear-gradient(100deg, #2684FF 0%, #5B7CFF 48%, #8B5CF6 100%);
                -webkit-background-clip:text; background-clip:text; }
    @supports ((-webkit-background-clip:text) or (background-clip:text)) {
      .rec-grad { color:transparent; }
    }"""
assert old in s, 'h1 rule changed'
s = s.replace(old, new, 1)

old = '          <h1>Hire the right talent, anywhere in the world.</h1>'
new = ('          <h1>Hire the right talent, anywhere in the\n'
       '              <span class="rec-grad">world.</span></h1>')
assert old in s, 'headline markup changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('Geist set; last word on a gradient')
