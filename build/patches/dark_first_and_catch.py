# -*- coding: utf-8 -*-
"""The chat window goes dark, and the boxes land on it.

Two things. The first window takes a dark treatment of its own, so it reads
against the dark sky it arrives on. And the chat section is pulled up to
overlap the end of the statement's pinned run, so the window is already
rising into the lower half of the screen while the boxes are still falling --
without that overlap there is simply nothing on screen for them to reach.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- the first window is dark ----------------------------------------------
old = '          <div class="rec-win">'
new = '          <div class="rec-win rec-win--dark">'
assert s.count(old) == 1, 'chat window markup changed'
s = s.replace(old, new, 1)

old = "    /* each slides in from the right, one after the other */"
new = """    /* The chat window keeps a dark treatment: it arrives while the sky is
       still dark, and the boxes land on it there. */
    .rec-win--dark { background:#141829;
                     box-shadow:0 24px 70px rgba(0,0,0,.45), 0 0 46px rgba(139,92,246,.16),
                                inset 0 0 0 1px rgba(255,255,255,.08); }
    .rec-win--dark .rec-win-bar { background:rgba(255,255,255,.03);
                                  box-shadow:inset 0 -1px 0 rgba(255,255,255,.07); }
    .rec-win--dark .rec-win-logo { filter:invert(1) brightness(1.7); }
    .rec-win--dark .rec-win-dots { color:#6B7488; }
    .rec-win--dark .rec-turn--you { background:rgba(255,255,255,.10); color:#F2F3F8; }
    .rec-win--dark .rec-turn--typing { background:rgba(255,255,255,.07); }
    .rec-win--dark .rec-dot { background:#A8AFC2; }
    .rec-win--dark .rec-turn--meta { color:#8E97AE; }
    .rec-win--dark .rec-turn--meta svg { color:#A78BFA; }
    .rec-win--dark .rec-turn--say { color:#E8EAF2; }
    .rec-win--dark .rec-turn--card { box-shadow:inset 0 0 0 1px rgba(255,255,255,.08); }
    .rec-win--dark .rec-card-head { background:rgba(255,255,255,.04); }
    .rec-win--dark .rec-card-head b { color:#F2F3F8; }
    .rec-win--dark .rec-card-head i, .rec-win--dark .rec-row-k,
    .rec-win--dark .rec-row-src { color:#8E97AE; }
    .rec-win--dark .rec-card-count { color:#A78BFA; }
    .rec-win--dark .rec-row { box-shadow:inset 0 1px 0 rgba(255,255,255,.06); }
    .rec-win--dark .rec-row-v { color:#F2F3F8; }
    .rec-win--dark .rec-turn--chips button { color:#E8EAF2; background:rgba(255,255,255,.07); }
    .rec-win--dark .rec-turn--chips button:hover { background:rgba(255,255,255,.13); }
    .rec-win--dark .rec-ask { background:rgba(255,255,255,.05); }
    .rec-win--dark .rec-ask-hint { color:#7D869B; }
    .rec-win--dark .rec-ask-tools { color:#7D869B; }

    /* each slides in from the right, one after the other */"""
assert old in s, 'side window comment moved'
s = s.replace(old, new, 1)

# ---- the window rises while the boxes are still falling --------------------
old = """    /* tall enough to hold the row still while it assembles */
    .rec-chat-sec { position:relative; min-height:240vh; }"""
new = """    /* Pulled up so its window is already climbing into the lower half of the
       screen while the statement section is still pinned -- that overlap is
       what the falling boxes land on. */
    .rec-chat-sec { position:relative; min-height:240vh; margin-top:-55vh; }"""
assert old in s, 'chat section rule changed'
s = s.replace(old, new, 1)

old = """    .rec-say-pin { position:sticky; top:0; height:100vh; display:grid; place-items:center; }"""
new = """    /* above the chat window, so the boxes fall in front of it */
    .rec-say-pin { position:sticky; top:0; height:100vh; display:grid; place-items:center;
                   z-index:2; }"""
assert old in s, 'pin rule changed'
s = s.replace(old, new, 1)

# the drop now ends where that window's top edge is
old = """          root.style.setProperty('--fall-px', (f * window.innerHeight * 0.62).toFixed(1) + 'px');
          root.style.setProperty('--fall-o',
            Math.min(1, Math.max(0, (1 - f) / 0.45)).toFixed(3));"""
new = """          root.style.setProperty('--fall-px', (f * window.innerHeight * 0.46).toFixed(1) + 'px');
          // they hold their strength until they are on the window, and go out
          // over the last quarter of the drop
          root.style.setProperty('--fall-o',
            Math.min(1, Math.max(0, (1 - f) / 0.25)).toFixed(3));"""
assert old in s, 'fall assignment changed'
s = s.replace(old, new, 1)

old = """      .rec-chat-sec { min-height:0; padding-block:60px; }"""
new = """      .rec-chat-sec { min-height:0; margin-top:0; padding-block:60px; }"""
assert old in s, 'responsive chat rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('dark chat window; the boxes land on it')
