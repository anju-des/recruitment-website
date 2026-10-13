# -*- coding: utf-8 -*-
"""Put back what the last cut took with it.

Removing the hero's glow block used the next section's marker as its end,
and the header's CSS sat in between -- so the header, the layering rules and
the sky block all went. They go back here, in order.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """    /* ---- page ground --------------------------------------------------- */
    /* Plain white page; the only colour is the violet that gathers at the
       foot of the hero and hands over to whatever section comes next. */
    body { background:#FFFFFF; }
    .rec-hero { position:relative; }

"""
new = """    /* ---- the sky --------------------------------------------------------- */
    /* The whole backdrop is this one fixed layer: the violet wash at rest and
       the dark later on are the same colours travelling, set from script.
       Nothing is ever laid over the content, so the text never greys, and
       because it is fixed there is no seam between one section and the next. */
    body { background:#FFFFFF; }
    .rec-hero { position:relative; }
    .rec-sky { position:fixed; inset:0; z-index:-1; pointer-events:none;
               background:linear-gradient(180deg,
                 var(--sky-a, #FFFFFF) 0%, var(--sky-a, #FFFFFF) 34%,
                 var(--sky-b, #E6DFFA) 100%); }
    /* the drifting blob rides on the sky now, and fades as it darkens */
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
    @media (prefers-reduced-motion: reduce) { .rec-sky::before { animation:none; } }

    /* content sits above the sky; the header above that */
    .rec-head { position:relative; z-index:2; }
    .rec-wrap { position:relative; z-index:1; }
    .rec-hero-inner { display:flex; flex-direction:column; align-items:center;
                      width:100%;
                      transform:translateY(calc(var(--rec-lift, 0) * -1px));
                      opacity:var(--rec-fade, 1);
                      will-change:transform, opacity; }
    @media (prefers-reduced-motion: reduce) {
      .rec-hero-inner { transform:none; opacity:1; }
    }

    /* ---- header ---------------------------------------------------------- */
    .rec-head { display:flex; align-items:center; justify-content:space-between;
                height:72px; padding:0 48px; }
    .rec-logo { display:inline-flex; }
    .rec-logo img { height:30px; width:auto; display:block; }
    .rec-head-right { display:flex; align-items:center; gap:28px; }
    .rec-nav { display:flex; align-items:center; gap:24px; }
    .rec-nav-item { display:inline-flex; align-items:center; gap:5px; cursor:pointer;
                    background:none; border:none; padding:6px 0; font-family:inherit;
                    font-size:14.5px; font-weight:400; color:var(--text-primary);
                    transition:color .12s; }
    .rec-nav-item:hover { color:var(--primary-600); }
    .rec-nav-item svg { width:13px; height:13px; color:var(--text-muted); }
    /* same near-black as the field's action, so the two read as one family */
    .rec-login { display:inline-flex; align-items:center; height:38px; padding:0 20px;
                 border:none; border-radius:8px; background:#0f172a;
                 font-size:14px; font-weight:600; color:#ffffff;
                 transition:background .12s; }
    .rec-login:hover { background:#1e293b; }

"""
assert old in s, 'page ground block changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('sky, layering and header css restored')
