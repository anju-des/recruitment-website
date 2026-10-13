# -*- coding: utf-8 -*-
"""One continuous backdrop instead of a veil over two sections.

The grey cast and the hard line across the page came from the same thing: a
dark sheet laid over the content, with the violet ending at the hero's own
bottom edge. Both go away if the page has a single fixed backdrop whose
colours themselves travel from light to dark -- nothing is ever laid over the
text, and there is no section edge to see.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- markup ----------------------------------------------------------------
old = '      <div class="rec-dark" aria-hidden="true"></div>'
new = '      <div class="rec-sky" aria-hidden="true"></div>'
assert old in s, 'dark sheet markup changed'
s = s.replace(old, new, 1)

# ---- the backdrop ----------------------------------------------------------
old = """    /* ---- scrolling into the dark --------------------------------------- */
    /* One sheet over the whole viewport. It is above the hero's glow and
       below the content, so the page darkens while the words are still
       legible on their way out. */
    .rec-dark { position:fixed; inset:0; z-index:0; pointer-events:none;
                background:#0B0F19; opacity:var(--rec-dark, 0); }"""
new = """    /* ---- the sky --------------------------------------------------------- */
    /* The whole backdrop is this one fixed layer: the violet wash at rest and
       the dark later on are the same two colours travelling, set from script.
       Nothing is ever laid over the content, so the text never greys, and
       because it is fixed there is no seam between one section and the next. */
    .rec-sky { position:fixed; inset:0; z-index:-1; pointer-events:none;
               background:linear-gradient(180deg,
                 var(--sky-a, #FFFFFF) 0%, var(--sky-a, #FFFFFF) 34%,
                 var(--sky-b, #E6DFFA) 100%); }
    /* the drifting blob rides on the sky now, and fades out as it darkens */
    .rec-sky::before {
      content:""; position:absolute; left:50%; bottom:-140px;
      width:min(1100px, 90%); height:460px; translate:-50% 0; border-radius:50%;
      filter:blur(50px); opacity:var(--sky-glow, 1);
      background:radial-gradient(closest-side,
                 rgba(139,92,246,.40) 0%, rgba(124,131,246,.22) 45%,
                 rgba(139,92,246,0) 78%);
      animation:rec-glow 14s ease-in-out infinite;
    }
    @keyframes rec-glow {
      0%, 100% { transform:translateX(-90px) scale(1); }
      50%      { transform:translateX(90px) scale(1.14); }
    }
    @media (prefers-reduced-motion: reduce) { .rec-sky::before { animation:none; } }"""
assert old in s, 'dark sheet css changed'
s = s.replace(old, new, 1)

# the hero no longer paints its own glow, so it needs neither the layers nor
# the clipping that kept them from adding scroll
old_start = s.index('    /* the drifting blob hangs below the section; clipping it here stops it')
old_end = s.index('    /* ---- announcement chip')
block = s[old_start:old_end]
assert 'rec-breathe' in block and '.rec-hero::after' in block, 'hero glow block changed'
s = s[:old_start] + '    .rec-hero { position:relative; }\n\n' + s[old_end:]

s = s.replace('    body { background:var(--neutral-0); }',
              '    body { background:#FFFFFF; }', 1)

# ---- script ----------------------------------------------------------------
old = """      root.style.setProperty('--rec-lift', (p * 150).toFixed(2));
      root.style.setProperty('--rec-fade', (1 - Math.min(1, p * 1.25)).toFixed(3));
      root.style.setProperty('--rec-dark', (p * 0.96).toFixed(3));"""
new = """      root.style.setProperty('--rec-lift', (p * 150).toFixed(2));
      root.style.setProperty('--rec-fade', (1 - Math.min(1, p * 1.25)).toFixed(3));
      // the sky's own two colours travel; nothing is laid over the page
      root.style.setProperty('--sky-a', mix(SKY_A, NIGHT_A, p));
      root.style.setProperty('--sky-b', mix(SKY_B, NIGHT_B, p));
      root.style.setProperty('--sky-glow', (1 - p).toFixed(3));"""
assert old in s, 'scroll script changed'
s = s.replace(old, new, 1)

old = """    var hero = document.querySelector('.rec-hero');
    var root = document.documentElement;
    if (!hero) return;
    var ticking = false;"""
new = """    var hero = document.querySelector('.rec-hero');
    var root = document.documentElement;
    if (!hero) return;
    var ticking = false;

    var SKY_A = [255, 255, 255], SKY_B = [230, 223, 250];   // daylight
    var NIGHT_A = [14, 17, 28], NIGHT_B = [8, 10, 18];      // after dark

    function mix(from, to, t) {
      return 'rgb(' + from.map(function (c, i) {
        return Math.round(c + (to[i] - c) * t);
      }).join(',') + ')';
    }"""
assert old in s, 'script head changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('one continuous sky')
