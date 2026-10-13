# -*- coding: utf-8 -*-
"""The window turns light, and keeps its size, in the closing frame.

The dark treatment was only ever for the black sky it arrives on. Every
dark rule is now conditional on the window not carrying `is-light`, so the
light base underneath simply comes back -- over half a second, so it reads
as the room turning on rather than a switch. It barely shrinks now: the
heading takes the top of the frame and the window keeps the rest.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- it stays close to full size ------------------------------------------
old = """                transform:translateY(calc(var(--win-down, 0) * 13vh))
                          scale(calc(1 - 0.30 * var(--win-down, 0))); }"""
new = """                transform:translateY(calc(var(--win-down, 0) * 8vh))
                          scale(calc(1 - 0.06 * var(--win-down, 0))); }"""
assert old in s, 'row transform changed'
s = s.replace(old, new, 1)

old = "    .rec-close-h { position:absolute; top:14vh; left:50%; translate:-50% 0;"
new = "    .rec-close-h { position:absolute; top:9vh; left:50%; translate:-50% 0;"
assert old in s, 'heading placement changed'
s = s.replace(old, new, 1)

# ---- the dark treatment yields to `is-light` -------------------------------
start = s.index('    .rec-win--dark { background:#000000;')
end = s.index('    .rec-ask-send {')
block = s[start:end]
assert block.count('.rec-win--dark') >= 20, 'dark block changed'
block = block.replace('.rec-win--dark', '.rec-win--dark:not(.is-light)')
s = s[:start] + block + s[end:]

# ---- and the change is a fade, not a cut -----------------------------------
old = """    .rec-turn { max-width:76%; padding:11px 14px; border-radius:14px; font-size:14.5px;
                line-height:1.5; opacity:0; transform:translateY(10px);
                transition:opacity .45s ease, transform .45s ease; }"""
new = """    .rec-turn { max-width:76%; padding:11px 14px; border-radius:14px; font-size:14.5px;
                line-height:1.5; opacity:0; transform:translateY(10px);
                transition:opacity .45s ease, transform .45s ease,
                           background-color .55s ease, color .55s ease; }"""
assert old in s, 'turn rule changed'
s = s.replace(old, new, 1)

old = "    .rec-ask-send { width:30px;"
new = """    /* the dark-to-light handover reads as the room turning on */
    .rec-win, .rec-win-bar, .rec-win-dots, .rec-turn--card, .rec-card-head,
    .rec-card-head b, .rec-card-head i, .rec-card-count, .rec-row, .rec-row-k,
    .rec-row-v, .rec-row-src, .rec-ask, .rec-ask-hint, .rec-ask-tools,
    .rec-turn--chips button, .rec-turn--meta, .rec-turn--say, .rec-dot {
      transition:background-color .55s ease, color .55s ease,
                 box-shadow .55s ease, background .55s ease;
    }
    .rec-win-logo { transition:filter .55s ease; }
    @media (prefers-reduced-motion: reduce) {
      .rec-win, .rec-win-bar, .rec-turn--card, .rec-card-head, .rec-row,
      .rec-ask, .rec-win-logo { transition:none; }
    }

    .rec-ask-send { width:30px;"""
assert old in s, 'send rule changed'
s = s.replace(old, new, 1)

# ---- driven from the same progress as the move -----------------------------
old = "        root.style.setProperty('--close-in', band(1.9, 1.35));   // then the words"
new = """        root.style.setProperty('--close-in', band(1.9, 1.35));   // then the words
        // once it has arrived in the light, it drops the dark treatment
        if (win) { win.classList.toggle('is-light', parseFloat(band(2.4, 1.85)) > 0.5); }"""
assert old in s, 'closing bands changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('light at the end')
