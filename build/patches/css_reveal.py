# -*- coding: utf-8 -*-
"""Drive the portal reveal from CSS rather than a scroll listener.

A scroll-driven animation is updated by the compositor off the scroll position
itself, so it needs no scroll events and no JS. `interpolate-size` is what lets
the keyframe end on `height: auto`, i.e. the image's own height, without having
to measure it.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- drop the script -------------------------------------------------------
start = s.index('\n<script>\n  // Grow the portal screenshot')
end = s.index('</script>\n', start) + len('</script>\n')
block = s[start:end]
assert 'requestAnimationFrame' in block, 'reveal script changed'
s = s[:start] + '\n' + s[end:]

# ---- css -------------------------------------------------------------------
old = """    .rec-shot-sec { margin-top:-54px; }
    .rec-shot { max-width:1200px; margin-inline:auto; height:var(--rec-peek);
                border-radius:16px 16px 0 0; overflow:hidden; line-height:0;
                border:8px solid var(--primary-100); border-bottom:none;
                will-change:height; }"""
new = """    /* the page's own blue sits behind the portal once it is fully open */
    .rec-shot-sec { margin-top:-54px; background:var(--bg-subtle); }
    .rec-shot { max-width:1200px; margin-inline:auto; height:var(--rec-peek);
                border-radius:16px 16px 0 0; overflow:hidden; line-height:0;
                border:8px solid var(--primary-100); border-bottom:none; }

    /* Reveal: the sliver grows to the image's full height over the first 60vh
       of scrolling. The timeline is the page scroller, so this needs no scroll
       listener. Browsers without scroll-driven animations ignore the timeline
       and land on the end state, i.e. the whole screenshot -- which is the
       right thing to show when the effect cannot run. */
    @keyframes rec-reveal { from { height:var(--rec-peek); } to { height:auto; } }
    .rec-shot { animation:rec-reveal linear both; animation-timeline:scroll(root block);
                animation-range:0 60vh; }"""
assert old in s, 'shot css changed'
s = s.replace(old, new, 1)

# `height: auto` is only animatable with this opted in
s = s.replace('    * { margin:0; padding:0; box-sizing:border-box; }',
              '    * { margin:0; padding:0; box-sizing:border-box; }\n'
              '    :root { interpolate-size:allow-keywords; }  /* lets height animate to auto */', 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('reveal is now css-driven')
