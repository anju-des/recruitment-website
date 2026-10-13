# -*- coding: utf-8 -*-
"""A sphere of light opens in the last section and leaves the mark behind.

Scroll-driven like everything else on the page: the core expands out of
nothing, a ring travels past it, and once the light has opened the mark
resolves in the middle of it. Measured from the section's own top, so the
pin holds the frame still while it plays.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

MARKUP = """        <!-- and down again, the same way -->
        <section class="rec-rest">
          <div class="rec-orb-pin">
            <span class="rec-orb-glow" aria-hidden="true"></span>
            <span class="rec-orb-ring" aria-hidden="true"></span>
            <span class="rec-orb-core" aria-hidden="true"></span>
            <img class="rec-orb-mark" src="mira-mark.svg"
                 width="412" height="300" alt="Mira" loading="lazy">
          </div>
        </section>"""

old = """        <!-- and down again, the same way -->
        <section class="rec-rest"></section>"""
assert old in s, 'rest section markup changed'
s = s.replace(old, MARKUP, 1)

CSS = """
    /* ---- the opening ------------------------------------------------------- */
    .rec-orb-pin { position:sticky; top:0; height:100vh; display:grid;
                   place-items:center; overflow:hidden; }
    /* the light itself: a core that opens out of nothing, the halo it throws,
       and a ring that travels past both */
    .rec-orb-core { position:absolute; width:min(42vmin, 320px); aspect-ratio:1;
                    border-radius:50%; pointer-events:none;
                    background:radial-gradient(circle at 50% 50%,
                      rgba(255,255,255,.98) 0%, rgba(232,222,255,.92) 26%,
                      rgba(167,139,250,.55) 52%, rgba(124,92,246,0) 72%);
                    opacity:calc(0.25 + 0.75 * var(--orb, 0));
                    transform:scale(calc(0.04 + 0.96 * var(--orb, 0))); }
    .rec-orb-glow { position:absolute; width:min(96vmin, 860px); aspect-ratio:1;
                    border-radius:50%; pointer-events:none;
                    background:radial-gradient(circle at 50% 50%,
                      rgba(150,118,255,.42) 0%, rgba(110,80,220,.20) 34%,
                      rgba(60,36,140,.08) 56%, rgba(20,10,46,0) 72%);
                    opacity:var(--orb, 0);
                    transform:scale(calc(0.2 + 0.8 * var(--orb, 0))); }
    .rec-orb-ring { position:absolute; width:min(74vmin, 640px); aspect-ratio:1;
                    border-radius:50%; pointer-events:none;
                    box-shadow:inset 0 0 0 1px rgba(216,200,255,.55),
                               0 0 46px rgba(150,118,255,.30);
                    /* it overtakes the core and fades as it leaves */
                    opacity:calc(var(--orb, 0) * (1 - var(--orb, 0)) * 2.6);
                    transform:scale(calc(0.1 + 1.25 * var(--orb, 0))); }
    /* the mark resolves once the light has opened */
    .rec-orb-mark { position:relative; z-index:1; width:min(30vmin, 210px);
                    height:auto; filter:invert(1) brightness(1.9);
                    opacity:var(--mark, 0);
                    transform:scale(calc(0.94 + 0.06 * var(--mark, 0))); }
    @media (prefers-reduced-motion: reduce) {
      .rec-orb-core, .rec-orb-glow, .rec-orb-ring, .rec-orb-mark {
        transform:none; }
      .rec-orb-mark { opacity:1; }
    }
    @media (max-width:1000px) {
      .rec-orb-pin { position:static; height:auto; padding-block:84px; }
      .rec-orb-mark { width:min(46vmin, 180px); }
    }

"""
anchor = "    /* ---- suggestions ------"
assert anchor in s, 'suggestions block missing'
s = s.replace(anchor, CSS + anchor, 1)

# ---- driven from the section's own scroll ----------------------------------
old = """        last = Math.min(1, Math.max(0, last));
      }"""
new = """        last = Math.min(1, Math.max(0, last));
        // inside the section the frame is pinned, and the scroll opens the light
        var rspan = Math.max(1, rest.offsetHeight - window.innerHeight);
        var q = Math.min(1, Math.max(0, (window.scrollY - rt) / rspan));
        root.style.setProperty('--orb', q.toFixed(3));
        root.style.setProperty('--mark',
          Math.min(1, Math.max(0, (q - 0.42) / 0.38)).toFixed(3));
      }"""
assert old in s, 'rest ramp block changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('the light opens on the mark')
