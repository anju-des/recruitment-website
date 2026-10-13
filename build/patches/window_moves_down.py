# -*- coding: utf-8 -*-
"""The window travels down, then the heading appears above it.

The heading moves into the pinned frame with the window, so the two can be
on screen together: as the closing section approaches, the window slides
down the screen, and once it has settled the heading comes up in the space
it left. Both are slices of the same approach, so the order is fixed.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- the heading joins the pinned frame ------------------------------------
old = """        <!-- CLOSING -->
        <section class="rec-close">
          <h2 class="rec-close-h">Mira at every stage</h2>
        </section>"""
new = """        <!-- CLOSING (scroll room; the heading rides in the pinned frame) -->
        <section class="rec-close"></section>"""
assert old in s, 'closing section markup changed'
s = s.replace(old, new, 1)

old = """          <div class="rec-wins-pin">
          <div class="rec-wins">"""
new = """          <div class="rec-wins-pin">
          <h2 class="rec-close-h">Mira at every stage</h2>
          <div class="rec-wins">"""
assert old in s, 'pinned frame markup changed'
s = s.replace(old, new, 1)

# ---- the chat section needs room to hold the pin through the handover ------
old = "    .rec-chat-sec { position:relative; min-height:150vh; margin-top:-55vh; }"
new = "    .rec-chat-sec { position:relative; min-height:260vh; margin-top:-55vh; }"
assert old in s, 'chat section rule changed'
s = s.replace(old, new, 1)

old = """    .rec-wins { position:absolute; top:50%; left:50%; translate:-50% -50%;
                display:flex; }"""
new = """    /* --win-down carries it towards the foot of the screen as the closing
       section arrives, leaving the top of the frame for the heading */
    .rec-wins { position:absolute; top:50%; left:50%; translate:-50% -50%;
                display:flex;
                transform:translateY(calc(var(--win-down, 0) * 34vh))
                          scale(calc(1 - 0.12 * var(--win-down, 0))); }"""
assert old in s, 'row rule changed'
s = s.replace(old, new, 1)

old = """    .rec-close { position:relative; min-height:120vh; display:grid; place-items:center;
                 text-align:center; }
    /* --close-in runs 0 to 1 over the approach, so the words arrive with the
       light rather than switching on at a threshold */
    .rec-close-h { max-width:18ch; font-size:clamp(30px, 2.4vw + 14px, 58px);"""
new = """    .rec-close { position:relative; min-height:120vh; }
    /* it sits in the upper part of the pinned frame, above the window, and
       only once --close-in starts -- which is after the window has moved */
    .rec-close-h { position:absolute; top:16vh; left:50%; translate:-50% 0;
                   width:min(92vw, 900px); text-align:center;
                   max-width:18ch; font-size:clamp(30px, 2.4vw + 14px, 58px);"""
assert old in s, 'closing heading rule changed'
s = s.replace(old, new, 1)

old = """                   opacity:var(--close-in, 0);
                   transform:translateY(calc((1 - var(--close-in, 0)) * 40px)); }"""
new = """                   margin-inline:auto;
                   opacity:var(--close-in, 0);
                   transform:translateY(calc((1 - var(--close-in, 0)) * 40px)); }"""
assert old in s, 'closing heading motion changed'
s = s.replace(old, new, 1)

# ---- the two bands, in order ----------------------------------------------
old = """        // the heading takes a longer, slower run than the sky does
        var cin = (window.scrollY - (ct - window.innerHeight * 1.25))
                  / (window.innerHeight * 1.1);
        root.style.setProperty('--close-in', Math.min(1, Math.max(0, cin)).toFixed(3));"""
new = """        var vh = window.innerHeight;
        // first the window travels down the screen...
        var down = (window.scrollY - (ct - vh * 1.15)) / (vh * 0.55);
        root.style.setProperty('--win-down', Math.min(1, Math.max(0, down)).toFixed(3));
        // ...and only once it has settled does the heading come up above it
        var cin = (window.scrollY - (ct - vh * 0.5)) / (vh * 0.55);
        root.style.setProperty('--close-in', Math.min(1, Math.max(0, cin)).toFixed(3));"""
assert old in s, 'closing bands changed'
s = s.replace(old, new, 1)

old = """      .rec-close { min-height:100vh; }"""
new = """      .rec-close { min-height:40vh; }
      .rec-close-h { position:static; translate:none; opacity:1; transform:none;
                     margin:0 auto 32px; }"""
assert old in s, 'responsive closing rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('window moves down, then the heading arrives above it')
