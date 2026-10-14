# -*- coding: utf-8 -*-
"""The testimonials as pull quotes: a wordmark, a large italic, a byline.

The box goes. What held the six apart was the card, so the mask does it now
instead -- a wider fade at both ends, so the neighbours are a ghost of the
next quote rather than a clipped one.

The wordmarks are set in type, not drawn. Every company here is invented, and
putting a real company's logo over an invented quote would be an endorsement
nobody gave. Each gets its own ink so the change of voice reads at a glance.

Georgia for the quote rather than a web serif: it has a real italic, it is on
every machine already, and the logos on this page have been slimmed once
because the page was slow to arrive. One more font file would undo some of
that for a few lines of text.
"""
import io
import re
import sys

#        company      ink        name                  role                      quote
VOICES = [
    ('Halyard', '#D9544A', 'Devika Rao', 'Head of Engineering',
     'Two roles closed in a month and nobody on my team opened a CV. The '
     'shortlist was short, which is the part I didn&#8217;t expect.'),
    ('Tessellate', '#1F7A68', 'Tomas Lindqvist', 'Talent Lead',
     'I still make the call on every hire. I&#8217;ve just stopped losing '
     'Thursdays to finding an hour three people can agree on.'),
    ('Brightfold', '#B5720F', 'Priya Menon', 'Founder',
     'The scorecard goes in once and every candidate comes back measured '
     'against it. For a team our size that&#8217;s the whole thing.'),
    ('Crosslight', '#2F56C9', 'Adaeze Okafor', 'VP People',
     'Time to offer went from six weeks to eleven days, and the candidates '
     'noticed before we did.'),
    ('Northbeam', '#6D43C9', 'J&#250;lia Ferreira', 'Engineering Manager',
     'The interview notes are written before I&#8217;m out of the room. I '
     'read them now instead of writing them.'),
    ('Larkfield', '#A83566', 'Sam Kwon', 'COO',
     'We hired across four time zones without a coordinator. That used to be '
     'a full job.'),
]

CARD = """              <figure class="rec-voice"%s>
                <span class="rec-voice-mark">%s</span>
                <blockquote>%s</blockquote>
                <figcaption>
                  <b>%s</b>
                  <span aria-hidden="true">&#183;</span>
                  <i>%s</i>
                </figcaption>
              </figure>"""


def deck(hidden):
    tag = ' aria-hidden="true"' if hidden else ''
    return '\n'.join(CARD % (tag, co, q, name, role)
                     for co, ink, name, role, q in VOICES)


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

INKS = '\n'.join(
    '    .rec-voice:nth-child(6n+%d) { --ink:%s; }' % (i + 1, ink)
    for i, (co, ink, name, role, q) in enumerate(VOICES))

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
                  /* the quote is sized off the rail, so the inset that centres
                     it is a peek plus a gap on either side -- and that is
                     exactly how much of each neighbour shows */
                  --vrail:min(960px, 92vw);
                  --vg:clamp(12px, 1.4vw, 18px);
                  --vpeek:clamp(28px, 6vw, 88px);
                  --vcard:calc(var(--vrail) - 2 * (var(--vpeek) + var(--vg)));
                  --vstep:calc(var(--vcard) + var(--vg)); }
    .rec-voices-h { width:min(760px, 88vw); margin:0 auto clamp(44px, 6.5vh, 82px);
                    text-align:center; color:#1A1430;
                    font-size:clamp(22px, 1.5vw + 11px, 34px);
                    font-weight:600; line-height:1.24; letter-spacing:-0.025em;
                    text-wrap:balance;
                    opacity:var(--vh, 0);
                    transform:translateY(calc((1 - var(--vh, 0)) * 20px)); }
    /* without a card to hold the six apart, the fade at the ends does it: the
       neighbours read as a ghost of the next quote, not a cut-off one */
    .rec-voices-rail { position:relative; width:var(--vrail); margin-inline:auto;
                       overflow:hidden; opacity:var(--vh, 0);
                       padding-left:calc(var(--vpeek) + var(--vg));
                       box-sizing:border-box;
                       -webkit-mask-image:linear-gradient(90deg,
                         transparent 0%, #000 9%, #000 91%, transparent 100%);
                       mask-image:linear-gradient(90deg,
                         transparent 0%, #000 9%, #000 91%, transparent 100%); }
    .rec-voices-track { display:flex; align-items:stretch; gap:var(--vg);
                        width:max-content;
                        animation:rec-voices-run 33s ease-in-out infinite; }
    /* a quote holds in the middle, then slides on: six steps of 5.5s, of which
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
    /* a set height, so a short quote and a long one hold the byline on the
       same line as each other */
    .rec-voice { flex:none; width:var(--vcard); margin:0;
                 min-height:clamp(260px, 22vw, 330px);
                 display:flex; flex-direction:column;
                 align-items:center; justify-content:center; text-align:center; }
    /* set in type, not drawn: every company here is invented */
    .rec-voice-mark { color:var(--ink, #5B3FD0); text-transform:uppercase;
                      font-size:clamp(12px, 0.3vw + 10px, 15px); font-weight:700;
                      letter-spacing:.15em;
                      margin-bottom:clamp(18px, 2.4vh, 30px); }
@INKS@
    .rec-voice blockquote { margin:0 0 clamp(18px, 2.4vh, 30px);
                            font-family:Georgia, 'Times New Roman', Times, serif;
                            font-style:italic; color:#1A1430;
                            font-size:clamp(21px, 1.5vw + 11px, 36px);
                            line-height:1.34; letter-spacing:-0.012em;
                            text-wrap:balance; }
    .rec-voice blockquote::before { content:"\\201C"; }
    .rec-voice blockquote::after { content:"\\201D"; }
    .rec-voice figcaption { display:flex; align-items:center; justify-content:center;
                            flex-wrap:wrap; gap:8px;
                            font-size:clamp(12px, 0.2vw + 11px, 13.5px); }
    .rec-voice figcaption b { font-weight:600; color:#2C2545; }
    .rec-voice figcaption span { color:#A79FC8; }
    .rec-voice figcaption i { font-style:normal; color:#6F6790; }
    /* the dots keep the same clock: one length, six starts, one page load */
    .rec-voices-dots { display:flex; justify-content:center; gap:8px;
                       margin-top:clamp(26px, 3.2vh, 40px);
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
""".replace('@INKS@', INKS)

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
    assert s[a:b].count('class="rec-voice"') == 18, path + ': markup changed'
    s = s[:a] + MARKUP.lstrip('\n') + s[b:]

    assert s.count('class="rec-voice"') == 18, path + ': three decks expected'
    assert s.count('rec-voice-pic') == 0, path + ': the avatar should be gone'
    assert len(re.findall(r'<i></i>', s)) == 6, path + ': six dots expected'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
