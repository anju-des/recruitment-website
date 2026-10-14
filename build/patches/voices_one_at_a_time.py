# -*- coding: utf-8 -*-
"""One testimonial at a time, with its neighbours showing at the edges.

The row still travels right to left by itself, but in steps now: a card holds
in the middle for four and a half seconds, then slides on. The card is sized
off the rail rather than the rail off the card, so the inset that centres it
(a peek plus a gap) is the same number on both sides, and the two neighbours
show by exactly that much.

Three copies of the deck, not two. The travel is one copy, from the second
copy's first card to the third's, so the frame at the end of a lap is the
same picture as the frame at the start -- neighbours included. With two
copies the left peek would be empty at the top of each lap and full at the
bottom of it, which is a visible jump once every half minute.

The dots run on their own copy of the same clock: six animations of the same
length, each offset by one step, all started by the same page load.
"""
import io
import re
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


DOTS = '\n'.join('              <i></i>' for _ in VOICES)

MARKUP = """
        <!-- the ground comes back to the light, and the voices step past -->
        <section class="rec-voices">
          <h2 class="rec-voices-h">The people on the other end of it</h2>
          <div class="rec-voices-rail">
            <div class="rec-voices-track">
%s
%s
%s
            </div>
          </div>
          <div class="rec-voices-dots" aria-hidden="true">
%s
          </div>
        </section>""" % (deck(True), deck(False), deck(True), DOTS)

CSS = """
    /* ---- testimonials ------------------------------------------------------ */
    /* The light they sit on is the sky's own fifth leg, not a background of
       their own: a block laid over the fixed gradient is what reads as a seam. */
    /* the padding goes on the same selector that clears the page's own, or
       `.rec-wrap > section` outranks it and the section collapses */
    .rec-wrap > section.rec-voices { padding:clamp(70px, 9vh, 124px) 0
                                             clamp(90px, 12vh, 150px); }
    /* one screen tall, so the scroll that lightens the ground is exactly the
       scroll that brings the row in -- and so the page ends on a full screen
       of it rather than a strip under the fold */
    .rec-voices { position:relative; width:100%; overflow:hidden;
                  box-sizing:border-box; min-height:100vh;
                  display:flex; flex-direction:column; justify-content:center;
                  /* the card is sized off the rail, so the inset that centres
                     it is a peek plus a gap on either side -- and that is
                     exactly how much of each neighbour shows */
                  --vrail:min(840px, 92vw);
                  --vg:clamp(12px, 1.4vw, 18px);
                  --vpeek:clamp(24px, 4vw, 58px);
                  --vcard:calc(var(--vrail) - 2 * (var(--vpeek) + var(--vg)));
                  --vstep:calc(var(--vcard) + var(--vg)); }
    .rec-voices-h { width:min(760px, 88vw); margin:0 auto clamp(26px, 3.4vh, 44px);
                    text-align:center; color:#1A1430;
                    font-size:clamp(22px, 1.5vw + 11px, 34px);
                    font-weight:600; line-height:1.24; letter-spacing:-0.025em;
                    text-wrap:balance;
                    opacity:var(--vh, 0);
                    transform:translateY(calc((1 - var(--vh, 0)) * 20px)); }
    /* the inset centres the card; overflow is clipped at the padding edge, so
       the neighbours stay visible inside it */
    .rec-voices-rail { position:relative; width:var(--vrail); margin-inline:auto;
                       overflow:hidden; opacity:var(--vh, 0);
                       padding-left:calc(var(--vpeek) + var(--vg));
                       box-sizing:border-box;
                       -webkit-mask-image:linear-gradient(90deg,
                         transparent 0%, #000 7%, #000 93%, transparent 100%);
                       mask-image:linear-gradient(90deg,
                         transparent 0%, #000 7%, #000 93%, transparent 100%); }
    .rec-voices-track { display:flex; align-items:stretch; gap:var(--vg);
                        width:max-content;
                        animation:rec-voices-run 33s ease-in-out infinite; }
    /* a card holds in the middle, then slides on: six steps of 5.5s, of which
       the last 0.9s is the move */
    @keyframes rec-voices-run {
      0%,     13.94% { transform:translateX(calc(var(--vstep) * -6)); }
      16.67%, 30.60% { transform:translateX(calc(var(--vstep) * -7)); }
      33.33%, 47.27% { transform:translateX(calc(var(--vstep) * -8)); }
      50%,    63.94% { transform:translateX(calc(var(--vstep) * -9)); }
      66.67%, 80.60% { transform:translateX(calc(var(--vstep) * -10)); }
      83.33%, 97.27% { transform:translateX(calc(var(--vstep) * -11)); }
      100%           { transform:translateX(calc(var(--vstep) * -12)); }
    }
    .rec-voices-rail:hover .rec-voices-track,
    .rec-voices-rail:hover ~ .rec-voices-dots i { animation-play-state:paused; }
    .rec-voice { flex:none; width:var(--vcard); margin:0;
                 display:flex; flex-direction:column;
                 justify-content:space-between; gap:clamp(20px, 2.4vw, 30px);
                 border-radius:20px;
                 padding:clamp(24px, 3vw, 38px) clamp(22px, 3vw, 40px);
                 background:#FFFFFF; border:1px solid rgba(124,92,246,.15);
                 box-shadow:0 8px 28px rgba(58,38,116,.08); }
    .rec-voice blockquote { margin:0; color:#2C2545;
                            font-size:clamp(16px, 0.5vw + 13px, 21px);
                            line-height:1.58; letter-spacing:-0.012em; }
    .rec-voice blockquote::before { content:"\\201C"; }
    .rec-voice blockquote::after { content:"\\201D"; }
    .rec-voice figcaption { display:flex; align-items:center; gap:12px; }
    .rec-voice-pic { flex:none; width:38px; height:38px; border-radius:50%;
                     display:grid; place-items:center; font-size:13px;
                     font-weight:600; color:#5B3FD0; letter-spacing:.01em;
                     background:linear-gradient(140deg,
                       rgba(167,139,250,.30), rgba(124,92,246,.16)); }
    .rec-voice-id b { display:block; font-size:14px; font-weight:600;
                      color:#1A1430; }
    .rec-voice-id i { display:block; margin-top:2px; font-style:normal;
                      font-size:12px; color:#6F6790; }
    /* the dots keep the same clock: one length, six starts, one page load */
    .rec-voices-dots { display:flex; justify-content:center; gap:8px;
                       margin-top:clamp(22px, 2.8vh, 32px);
                       opacity:var(--vh, 0); }
    .rec-voices-dots i { width:7px; height:7px; border-radius:50%;
                         background:#4A3B86; opacity:.24;
                         animation:rec-voices-dot 33s ease-in-out infinite; }
    @keyframes rec-voices-dot {
      0%,     13.94% { opacity:1; transform:scale(1.2); }
      16.67%, 100%   { opacity:.24; transform:scale(1); }
    }
    .rec-voices-dots i:nth-child(1) { animation-delay:-33s; }
    .rec-voices-dots i:nth-child(2) { animation-delay:-27.5s; }
    .rec-voices-dots i:nth-child(3) { animation-delay:-22s; }
    .rec-voices-dots i:nth-child(4) { animation-delay:-16.5s; }
    .rec-voices-dots i:nth-child(5) { animation-delay:-11s; }
    .rec-voices-dots i:nth-child(6) { animation-delay:-5.5s; }
    /* the closing words step aside before the ground under them lightens */
    .rec-say-last { opacity:calc(1 - var(--vout, 0)); }
    @media (prefers-reduced-motion: reduce) {
      .rec-voices-h { transform:none; }
      .rec-voices-track { animation:none; }
      .rec-voices-rail { overflow-x:auto; padding-left:0; }
      .rec-voices-dots { display:none; }
    }
"""

CSS_HEAD = "    /* ---- testimonials ---"
CSS_TAIL = "    /* ---- suggestions ---"
MARK_HEAD = "        <!-- the ground comes back to the light"
MARK_TAIL = "        </section>"


def patch(path):
    s = io.open(path, encoding='utf-8').read()

    a = s.index(CSS_HEAD)
    b = s.index(CSS_TAIL, a)
    assert 'rec-voices-track' in s[a:b], path + ': not the testimonials CSS'
    s = s[:a] + CSS.lstrip('\n') + '\n' + s[b:]

    a = s.index(MARK_HEAD)
    b = s.index(MARK_TAIL, a) + len(MARK_TAIL)
    assert s[a:b].count('class="rec-voice"') == 12, path + ': markup changed'
    s = s[:a] + MARKUP.lstrip('\n') + s[b:]

    assert s.count('class="rec-voice"') == 18, path + ': three decks expected'
    assert len(re.findall(r'<i></i>', s)) == 6, path + ': six dots expected'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
