# -*- coding: utf-8 -*-
"""Testimonials at the foot of the page, on a light ground, moving by themselves.

The ground change goes on the sky ramp like every other one -- a fifth leg,
4 -> 5, climbing back out of the violet-black the closing section ends on --
rather than an opaque block laid over it, which is what left a seam the last
time a section brought its own background.

The row runs right to left on its own. Two copies of the same six cards sit in
one flex track and the track travels exactly one copy's width, so the seam
between them never arrives: that distance is half the track plus half a gap,
since the track carries one gap fewer than twice the cards.

People and companies are invented, and named apart from the candidates further
up the page so nobody reads them as the same person on the other side of the
table.
"""
import io
import sys

VOICES = [
    ('DR', 'Devika Rao', 'Head of Engineering, Halyard',
     'Two roles closed in a month and nobody on my team opened a CV. The '
     'shortlist was short, which is the part I didn&#8217;t expect.'),
    ('TL', 'Tomas Lindqvist', 'Talent Lead, Tessellate',
     'I still make the call on every hire. I&#8217;ve just stopped losing '
     'Thursdays to finding an hour three people can agree on.'),
    ('PM', 'Priya Menon', 'Founder, Brightfold',
     'The scorecard goes in once and every candidate comes back measured '
     'against it. For a team our size that&#8217;s the whole thing.'),
    ('AO', 'Adaeze Okafor', 'VP People, Crosslight',
     'Time to offer went from six weeks to eleven days, and the candidates '
     'noticed before we did.'),
    ('JF', 'J&#250;lia Ferreira', 'Engineering Manager, Northbeam',
     'The interview notes are written before I&#8217;m out of the room. I '
     'read them now instead of writing them.'),
    ('SK', 'Sam Kwon', 'COO, Larkfield',
     'We hired across four time zones without a coordinator. That used to be '
     'a full job.'),
]

CARD = """              <figure class="rec-voice"%s>
                <blockquote>%s</blockquote>
                <figcaption>
                  <span class="rec-voice-pic" aria-hidden="true">%s</span>
                  <span class="rec-voice-id">
                    <b>%s</b>
                    <i>%s</i>
                  </span>
                </figcaption>
              </figure>"""


def deck(hidden):
    tag = ' aria-hidden="true"' if hidden else ''
    return '\n'.join(CARD % (tag, q, ini, name, role)
                     for ini, name, role, q in VOICES)


MARKUP = """
        <!-- the ground comes back to the light, and the voices run past -->
        <section class="rec-voices">
          <h2 class="rec-voices-h">The people on the other end of it</h2>
          <div class="rec-voices-rail">
            <div class="rec-voices-track">
%s
%s
            </div>
          </div>
        </section>""" % (deck(False), deck(True))

CSS = """
    /* ---- testimonials ------------------------------------------------------ */
    /* The light they sit on is the sky's own fifth leg, not a background of
       their own: a block laid over the fixed gradient is what reads as a seam. */
    .rec-wrap > section.rec-voices { padding:0; }
    .rec-voices { position:relative; width:100%; --vg:18px;
                  padding-block:clamp(70px, 9vh, 124px) clamp(90px, 12vh, 150px);
                  overflow:hidden; }
    .rec-voices-h { width:min(760px, 88vw); margin:0 auto clamp(26px, 3.4vh, 44px);
                    text-align:center; color:#1A1430;
                    font-size:clamp(22px, 1.5vw + 11px, 34px);
                    font-weight:600; line-height:1.24; letter-spacing:-0.025em;
                    text-wrap:balance;
                    opacity:var(--vh, 0);
                    transform:translateY(calc((1 - var(--vh, 0)) * 20px)); }
    /* the ends of the row fade rather than stop */
    .rec-voices-rail { position:relative; width:100%; overflow:hidden;
                       opacity:var(--vh, 0);
                       -webkit-mask-image:linear-gradient(90deg,
                         transparent 0%, #000 8%, #000 92%, transparent 100%);
                       mask-image:linear-gradient(90deg,
                         transparent 0%, #000 8%, #000 92%, transparent 100%); }
    .rec-voices-track { display:flex; align-items:stretch; gap:var(--vg);
                        width:max-content; padding-inline:var(--vg);
                        animation:rec-voices-run 58s linear infinite; }
    /* one copy's width is half the track plus half a gap: the track holds one
       gap fewer than twice the cards */
    @keyframes rec-voices-run {
      from { transform:translateX(0); }
      to   { transform:translateX(calc(-50% - var(--vg) / 2)); }
    }
    .rec-voices-rail:hover .rec-voices-track { animation-play-state:paused; }
    .rec-voice { flex:none; width:338px; margin:0;
                 display:flex; flex-direction:column;
                 justify-content:space-between; gap:20px;
                 border-radius:16px; padding:24px 24px 22px;
                 background:#FFFFFF; border:1px solid rgba(124,92,246,.15);
                 box-shadow:0 6px 22px rgba(58,38,116,.07); }
    .rec-voice blockquote { margin:0; color:#2C2545; font-size:15px;
                            line-height:1.62; letter-spacing:-0.005em; }
    .rec-voice blockquote::before { content:"\\201C"; }
    .rec-voice blockquote::after { content:"\\201D"; }
    .rec-voice figcaption { display:flex; align-items:center; gap:11px; }
    .rec-voice-pic { flex:none; width:34px; height:34px; border-radius:50%;
                     display:grid; place-items:center; font-size:12px;
                     font-weight:600; color:#5B3FD0; letter-spacing:.01em;
                     background:linear-gradient(140deg,
                       rgba(167,139,250,.30), rgba(124,92,246,.16)); }
    .rec-voice-id b { display:block; font-size:13px; font-weight:600;
                      color:#1A1430; }
    .rec-voice-id i { display:block; margin-top:2px; font-style:normal;
                      font-size:11.5px; color:#6F6790; }
    /* the closing words step aside before the ground under them lightens */
    .rec-say-last { opacity:calc(1 - var(--vout, 0)); }
    @media (prefers-reduced-motion: reduce) {
      .rec-voices-h { transform:none; }
      .rec-voices-track { animation:none; }
      .rec-voices-rail { overflow-x:auto; }
    }
    @media (max-width:1000px) {
      .rec-voice { width:min(80vw, 300px); }
    }
"""

JS_OLD = """        root.style.setProperty('--s3', line(0.87, 0.96));
      }
      var t = c + back + down + last;"""
JS_NEW = """        root.style.setProperty('--s3', line(0.87, 0.96));
      }
      // ...and back up to the light over the screen before the voices, which
      // is the same screen the pinned frame spends letting go
      var voiceIn = 0;
      if (voices) {
        var vt = window.scrollY + voices.getBoundingClientRect().top;
        voiceIn = (window.scrollY - (vt - window.innerHeight)) / window.innerHeight;
        voiceIn = Math.min(1, Math.max(0, voiceIn));
        var vb = function (a, b) {
          return Math.min(1, Math.max(0, (voiceIn - a) / (b - a))).toFixed(3);
        };
        // the white words leave first, while the ground is still dark
        root.style.setProperty('--vout', vb(0.10, 0.48));
        root.style.setProperty('--vh', vb(0.55, 0.95));
      }
      var t = c + back + down + last + voiceIn;"""

TOP_OLD = "               [3.5, [86, 66, 160]], [4, [26, 16, 54]]];"
TOP_NEW = ("               [3.5, [86, 66, 160]], [4, [26, 16, 54]],\n"
           "               [4.5, [86, 66, 160]], [5, [240, 236, 255]]];")
FOOT_OLD = "                [3.5, [58, 40, 112]], [4, [10, 5, 26]]];"
FOOT_NEW = ("                [3.5, [58, 40, 112]], [4, [10, 5, 26]],\n"
            "                [4.5, [58, 40, 112]], [5, [255, 255, 255]]];")

LIT_OLD = """      var lit = t <= 1 ? t
              : (t <= 2 ? 1
              : (t <= 3 ? 3 - t : Math.min(1, t - 3)));"""
LIT_NEW = """      var lit = t <= 1 ? t
              : (t <= 2 ? 1
              : (t <= 3 ? 3 - t
              : (t <= 4 ? Math.min(1, t - 3) : Math.max(0, 5 - t))));"""

NIGHT_OLD = "head.classList.toggle('is-night', (t > 0.5 && t < 2.6) || t > 3.45);"
NIGHT_NEW = ("head.classList.toggle('is-night',\n"
             "          (t > 0.5 && t < 2.6) || (t > 3.45 && t < 4.55));")

REST_CLOSE = "        </section>\n"
CSS_MARK = "    /* ---- suggestions ------"
REST_VAR = "    var rest = document.querySelector('.rec-rest');"


def one(s, old, new, path, what):
    assert s.count(old) == 1, '%s: %s (%d matches)' % (path, what, s.count(old))
    return s.replace(old, new, 1)


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-voices' not in s, path + ': already has testimonials'

    i = s.rindex(REST_CLOSE) + len(REST_CLOSE)
    s = s[:i] + MARKUP + '\n' + s[i:]

    s = one(s, CSS_MARK, CSS + '\n' + CSS_MARK, path, 'suggestions marker')
    s = one(s, REST_VAR,
            REST_VAR + "\n    var voices = document.querySelector('.rec-voices');",
            path, 'script head')
    s = one(s, JS_OLD, JS_NEW, path, 'closing bands')
    s = one(s, TOP_OLD, TOP_NEW, path, 'sky top stops')
    s = one(s, FOOT_OLD, FOOT_NEW, path, 'sky foot stops')
    s = one(s, LIT_OLD, LIT_NEW, path, 'lit ramp')
    s = one(s, NIGHT_OLD, NIGHT_NEW, path, 'header night toggle')

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
