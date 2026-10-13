# -*- coding: utf-8 -*-
"""Make the violet at the foot of the hero move.

Two layers: the flat band stays and breathes, and a soft blob drifts across
behind it. Both are transform/opacity only, so the work stays on the
compositor and the text above never repaints.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """    .rec-hero::after {
      content:""; position:absolute; left:0; right:0; bottom:0; height:48%;
      z-index:-1; pointer-events:none;
      background:linear-gradient(180deg,
                 rgba(167,139,250,0) 0%, rgba(167,139,250,.14) 55%,
                 rgba(139,92,246,.26) 100%);
    }
"""
new = """    .rec-hero::after {
      content:""; position:absolute; left:0; right:0; bottom:0; height:48%;
      z-index:-1; pointer-events:none;
      background:linear-gradient(180deg,
                 rgba(167,139,250,0) 0%, rgba(167,139,250,.14) 55%,
                 rgba(139,92,246,.26) 100%);
      animation:rec-breathe 9s ease-in-out infinite;
    }
    /* a soft blob drifting across behind the band, which is what keeps the
       glow from reading as a flat fill */
    .rec-hero::before {
      content:""; position:absolute; left:50%; bottom:-140px;
      width:min(1100px, 90%); height:460px; translate:-50% 0; border-radius:50%;
      z-index:-1; pointer-events:none; filter:blur(50px);
      background:radial-gradient(closest-side,
                 rgba(139,92,246,.40) 0%, rgba(124,131,246,.22) 45%,
                 rgba(139,92,246,0) 78%);
      animation:rec-glow 14s ease-in-out infinite;
    }
    @keyframes rec-breathe {
      0%, 100% { opacity:.78; }
      50%      { opacity:1; }
    }
    @keyframes rec-glow {
      0%, 100% { transform:translateX(-90px) scale(1); opacity:.7; }
      50%      { transform:translateX(90px) scale(1.14); opacity:1; }
    }
    @media (prefers-reduced-motion: reduce) {
      .rec-hero::before, .rec-hero::after { animation:none; }
    }
"""
assert old in s, 'hero glow block changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('glow animated')
