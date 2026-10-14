# -*- coding: utf-8 -*-
"""The footer again: a line and the socials on the left, the nav on the right,
and the dark arriving on the sky ramp rather than as a slab of its own.

So the footer has no background. It is the ramp's sixth leg, 5 -> 6, running
back down through the same violet every other leg passes through, over the
screen before the footer's top -- which is the whole of the testimonial
section. The quotes therefore have to leave while it darkens, or the heading
would be near-black text on a near-black ground halfway through.

The footer is a full screen tall for the same reason the testimonials are:
the band finishes at the footer's top, and that is only reachable if what
follows it is at least a screen. Shorter, and the ramp would stop partway and
the page would end on a half-lit violet.
"""
import io
import sys

ICONS = [
    ('LinkedIn', '<rect x="3" y="3" width="18" height="18" rx="4"/>'
                 '<path d="M7.5 10.6v5.9"/>'
                 '<circle cx="7.5" cy="7.7" r=".85" fill="currentColor" stroke="none"/>'
                 '<path d="M11.6 16.5v-3.2a2.3 2.3 0 0 1 4.6 0v3.2"/>'
                 '<path d="M11.6 10.6v5.9"/>'),
    ('X', '<path d="M4.5 4.5l15 15"/><path d="M19.5 4.5l-15 15"/>'),
    ('YouTube', '<rect x="2.5" y="6" width="19" height="12" rx="4"/>'
                '<path d="M10.6 9.7l4.7 2.3-4.7 2.3z"/>'),
    ('Instagram', '<rect x="3" y="3" width="18" height="18" rx="5"/>'
                  '<circle cx="12" cy="12" r="3.6"/>'
                  '<circle cx="16.9" cy="7.1" r=".9" fill="currentColor" stroke="none"/>'),
]

COLUMNS = [
    ('Platform', ['Screening', 'Interviews', 'Scorecards', 'Offers']),
    ('Solutions', ['Startups', 'Scale-ups', 'Agencies']),
    ('Resources', ['Pricing', 'Help centre', 'Contact']),
    ('Company', ['About', 'Careers', 'Press']),
]


def social(name, body):
    return ("""              <a href="#%s" aria-label="%s">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                     stroke-width="1.6" stroke-linecap="round"
                     stroke-linejoin="round" aria-hidden="true">%s</svg>
              </a>""" % (name.lower(), name, body))


def column(title, items):
    links = '\n'.join(
        '                <li><a href="#%s">%s</a></li>'
        % (item.lower().replace(' ', '-'), item) for item in items)
    return """            <div class="rec-foot-col">
              <h3>%s</h3>
              <ul>
%s
              </ul>
            </div>""" % (title, links)


MARKUP = """
      <footer class="rec-foot">
        <div class="rec-foot-inner">
          <div class="rec-foot-say">
            <h2>Start hiring<br>with Mira.</h2>
            <div class="rec-foot-social">
%s
            </div>
          </div>
          <nav class="rec-foot-cols" aria-label="Footer">
%s
          </nav>
        </div>
        <div class="rec-foot-base">
          <small>&#169; 2026 Wisemonk. All rights reserved.</small>
          <nav aria-label="Legal">
            <a href="#privacy">Privacy</a>
            <a href="#terms">Terms</a>
            <a href="#login">Log in</a>
          </nav>
        </div>
      </footer>""" % ('\n'.join(social(n, b) for n, b in ICONS),
                      '\n'.join(column(t, i) for t, i in COLUMNS))

CSS = """
    /* ---- footer ------------------------------------------------------------ */
    /* No background: the dark is the sky's sixth leg, arriving on the scroll
       like every other change of ground on this page. */
    /* A full screen tall, because the ramp finishes at this element's top and
       that is only reachable when what follows it is at least a screen. */
    .rec-foot { position:relative; color:#9A93B4; box-sizing:border-box;
                min-height:100vh; display:flex; flex-direction:column;
                padding:clamp(48px, 7vh, 96px) clamp(22px, 5vw, 72px)
                        clamp(22px, 3vh, 34px);
                font-size:14px; line-height:1.6;
                opacity:var(--fin, 0);
                transform:translateY(calc((1 - var(--fin, 0)) * 24px)); }
    /* auto margins centre the body of it and leave the rule at the floor */
    .rec-foot-inner { width:min(1240px, 100%); margin:auto auto;
                      display:grid; grid-template-columns:1fr 1fr;
                      gap:clamp(40px, 5vw, 90px); align-items:start;
                      padding-bottom:clamp(40px, 6vh, 76px); }
    .rec-foot-say h2 { margin:0 0 clamp(26px, 3.4vh, 42px); color:#FFFFFF;
                       font-size:clamp(34px, 4.2vw, 66px); font-weight:500;
                       line-height:1.06; letter-spacing:-0.032em; }
    .rec-foot-social { display:flex; flex-wrap:wrap; gap:12px; }
    .rec-foot-social a { width:42px; height:42px; border-radius:50%;
                         display:grid; place-items:center; color:#D7D1EA;
                         box-shadow:inset 0 0 0 1px rgba(201,184,255,.22);
                         transition:background .15s, color .15s; }
    .rec-foot-social a:hover { background:rgba(255,255,255,.1); color:#FFFFFF; }
    .rec-foot-social svg { width:17px; height:17px; display:block; }
    .rec-foot-cols { display:grid; grid-template-columns:repeat(2, 1fr);
                     gap:clamp(28px, 4vh, 48px) clamp(24px, 3vw, 56px); }
    .rec-foot-col h3 { margin:0 0 16px; color:#7A7298; font-size:11px;
                       font-weight:600; letter-spacing:.13em;
                       text-transform:uppercase; }
    .rec-foot-col ul { margin:0; padding:0; list-style:none;
                       display:flex; flex-direction:column; gap:10px; }
    .rec-foot a { color:#B4ADCB; text-decoration:none; transition:color .15s; }
    .rec-foot a:hover, .rec-foot a:focus-visible { color:#FFFFFF; }
    .rec-foot a:focus-visible { outline:2px solid #7C5CF6; outline-offset:3px;
                                border-radius:4px; }
    .rec-foot-base { width:min(1240px, 100%); margin-inline:auto;
                     padding-top:clamp(18px, 2.4vh, 26px);
                     border-top:1px solid rgba(201,184,255,.14);
                     display:flex; flex-wrap:wrap; gap:14px 28px;
                     align-items:center; justify-content:space-between; }
    .rec-foot-base small { color:#6E6690; font-size:12.5px; }
    .rec-foot-base nav { display:flex; flex-wrap:wrap; gap:22px;
                         font-size:12.5px; }
    @media (max-width:860px) {
      .rec-foot-inner { grid-template-columns:1fr; }
    }
    @media (prefers-reduced-motion: reduce) {
      .rec-foot { transform:none; }
      .rec-foot a, .rec-foot-social a { transition:none; }
    }
"""

# --- the quotes have to go before the ground under them does -----------------
OLD_FADE_H = """                    opacity:var(--vh, 0);
                    transform:translateY(calc((1 - var(--vh, 0)) * 20px)); }"""
NEW_FADE_H = """                    opacity:calc(var(--vh, 0) * (1 - var(--tout, 0)));
                    transform:translateY(calc((1 - var(--vh, 0)) * 20px)); }"""
OLD_FADE_R = """                       opacity:var(--vh, 0);
                       transform:translateY(calc((1 - var(--vh, 0)) * 26px)); }"""
NEW_FADE_R = """                       opacity:calc(var(--vh, 0) * (1 - var(--tout, 0)));
                       transform:translateY(calc((1 - var(--vh, 0)) * 26px)); }"""

# --- the ramp ----------------------------------------------------------------
TOP_OLD = """               [4.5, [86, 66, 160]], [5, [240, 236, 255]]];"""
TOP_NEW = """               [4.5, [86, 66, 160]], [5, [240, 236, 255]],
               [5.5, [86, 66, 160]], [6, [16, 10, 30]]];"""
FOOT_OLD = """                [4.5, [58, 40, 112]], [5, [255, 255, 255]]];"""
FOOT_NEW = """                [4.5, [58, 40, 112]], [5, [255, 255, 255]],
                [5.5, [58, 40, 112]], [6, [6, 3, 14]]];"""

LIT_OLD = """      var lit = t <= 1 ? t
              : (t <= 2 ? 1
              : (t <= 3 ? 3 - t
              : (t <= 4 ? Math.min(1, t - 3) : Math.max(0, 5 - t))));"""
LIT_NEW = """      var lit = t <= 1 ? t
              : (t <= 2 ? 1
              : (t <= 3 ? 3 - t
              : (t <= 4 ? Math.min(1, t - 3)
              : (t <= 5 ? Math.max(0, 5 - t) : Math.min(1, t - 5)))));"""

NIGHT_OLD = """      head.classList.toggle('is-night',
          (t > 0.5 && t < 2.6) || (t > 3.45 && t < 4.55));"""
NIGHT_NEW = """      head.classList.toggle('is-night',
          (t > 0.5 && t < 2.6) || (t > 3.45 && t < 4.55) || t > 5.45);"""

JS_OLD = """      var t = c + back + down + last + voiceIn;"""
JS_NEW = """      // ...and down one last time for the footer, over the screen before its
      // top -- which is the whole of the testimonial section, so the quotes
      // leave first rather than turning into dark text on a dark ground
      var footIn = 0;
      if (foot) {
        var ft = window.scrollY + foot.getBoundingClientRect().top;
        footIn = (window.scrollY - (ft - window.innerHeight)) / window.innerHeight;
        footIn = Math.min(1, Math.max(0, footIn));
        var fb = function (a, b) {
          return Math.min(1, Math.max(0, (footIn - a) / (b - a))).toFixed(3);
        };
        root.style.setProperty('--tout', fb(0.12, 0.52));
        root.style.setProperty('--fin', fb(0.55, 0.95));
      }
      var t = c + back + down + last + voiceIn + footIn;"""

VAR_OLD = """    var voices = document.querySelector('.rec-voices');"""
VAR_NEW = """    var voices = document.querySelector('.rec-voices');
    var foot = document.querySelector('.rec-foot');"""

CSS_HEAD = "    /* ---- footer ---"
CSS_TAIL = "    /* ---- suggestions ---"
MARK_HEAD = "      <footer class=\"rec-foot\">"
MARK_TAIL = "      </footer>"


def patch(path):
    s = io.open(path, encoding='utf-8').read()

    a = s.index(CSS_HEAD)
    b = s.index(CSS_TAIL, a)
    assert '.rec-foot-brand' in s[a:b], path + ': not the footer CSS'
    s = s[:a] + CSS.lstrip('\n') + '\n' + s[b:]

    a = s.index(MARK_HEAD)
    b = s.index(MARK_TAIL, a) + len(MARK_TAIL)
    s = s[:a] + MARKUP.lstrip('\n') + s[b:]

    for old, new in ((OLD_FADE_H, NEW_FADE_H), (OLD_FADE_R, NEW_FADE_R),
                     (TOP_OLD, TOP_NEW), (FOOT_OLD, FOOT_NEW),
                     (LIT_OLD, LIT_NEW), (NIGHT_OLD, NIGHT_NEW),
                     (VAR_OLD, VAR_NEW), (JS_OLD, JS_NEW)):
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    assert 'rec-foot-brand' not in s, path + ': old footer left over'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
