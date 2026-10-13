# -*- coding: utf-8 -*-
"""Make the portal a proper second section: its own heading, normal spacing,
and a pop-up entrance instead of the sliver-at-the-hero's-floor crop.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- markup: give the section a heading ------------------------------------
old = """        <!-- PORTAL -->
        <section class="rec-shot-sec">
          <div class="rec-shot">"""
new = """        <!-- PORTAL -->
        <section class="rec-shot-sec">
          <div class="rec-band">
            <h2>One workspace for every open role</h2>
            <p>Post a role, read Mira&rsquo;s shortlist, book the interviews and decide
            &mdash; without leaving the portal.</p>
          </div>
          <div class="rec-shot">"""
assert old in s, 'portal section markup changed'
s = s.replace(old, new, 1)

# ---- hero goes back to a normal full-screen section ------------------------
s = s.replace('min-height:calc(100vh - var(--rec-chrome) - var(--rec-peek));',
              'min-height:calc(100vh - var(--rec-chrome));', 1)
s = s.replace("    .rec-wrap > section.rec-hero { padding-bottom:0; }\n", "", 1)
s = s.replace("    .rec-wrap > section.rec-shot-sec { padding:0 48px; }\n", "", 1)

# ---- the shot itself -------------------------------------------------------
old_css_start = s.index("    /* the page's own blue sits behind the portal")
old_css_end = s.index('    /* ---- hero composer')
old_css = s[old_css_start:old_css_end]
assert 'rec-reveal' in old_css, 'shot css changed'

new_css = """    /* the page's own blue sits behind the portal */
    .rec-shot-sec { background:var(--bg-subtle); }
    .rec-shot { max-width:1200px; margin-inline:auto; border-radius:16px; overflow:hidden;
                line-height:0; border:8px solid var(--primary-100); }
    .rec-shot img { width:100%; height:auto; display:block; }

    /* Pops up as the section scrolls into view: driven by the element's own
       view timeline, so it needs no scroll listener and cannot fall out of
       sync. Browsers without scroll-driven animations land on the end state,
       which is simply the image in place. */
    @keyframes rec-popup {
      from { transform:translateY(40px) scale(.96); opacity:0; }
      to   { transform:none; opacity:1; }
    }
    .rec-shot { transform-origin:50% 100%;
                animation:rec-popup cubic-bezier(.22,.61,.36,1) both;
                animation-timeline:view(); animation-range:entry 10% cover 38%; }
    @media (prefers-reduced-motion: reduce) {
      .rec-shot { animation:none; }
    }

"""
s = s[:old_css_start] + new_css + s[old_css_end:]

# --rec-peek no longer means anything
s = s.replace('"--rec-chrome:140px; --rec-peek:150px;", 1)',
              '"--rec-chrome:140px;", 1)', 1)
assert '--rec-peek' not in s, 'a reference to the old peek token is left'

io.open(p, 'w', encoding='utf-8').write(s)
print('portal is now a section with its own heading')
