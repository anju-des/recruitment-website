# -*- coding: utf-8 -*-
"""Six testimonials at once: two rows of three, each in its own container.

Nothing moves any more -- no track, no steps, no dots. All six are on the page
at once, so the reader picks rather than waits.

Each one keeps the pull-quote setting it had on its own: the wordmark in the
company's ink, the quote in a large italic, the byline under it, centred.

`grid-auto-rows: 1fr` is what makes the two rows match. Row height is
otherwise set by the tallest card in each row on its own, and the quotes are
different lengths, so the second row would sit a little shallower than the
first and the grid would read as crooked rather than as two rows.
"""
import io
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

CARD = """              <figure class="rec-voice">
                <span class="rec-voice-mark">%s</span>
                <blockquote>%s</blockquote>
                <figcaption>
                  <b>%s</b>
                  <span aria-hidden="true">&#183;</span>
                  <i>%s</i>
                </figcaption>
              </figure>"""

cards = '\n'.join(CARD % (co, q, name, role) for co, ink, name, role, q in VOICES)

MARKUP = """
        <!-- the ground comes back to the light, and all six are on it -->
        <section class="rec-voices">
          <h2 class="rec-voices-h">The people on the other end of it</h2>
          <div class="rec-voices-grid">
%s
          </div>
        </section>""" % cards

INKS = '\n'.join(
    '    .rec-voice:nth-child(%d) { --ink:%s; }' % (i + 1, ink)
    for i, (co, ink, name, role, q) in enumerate(VOICES))

CSS = """
    /* ---- testimonials ------------------------------------------------------ */
    /* The light they sit on is the sky's own fifth leg, not a background of
       their own: a block laid over the fixed gradient is what reads as a seam. */
    /* the padding goes on the same selector that clears the page's own, or
       `.rec-wrap > section` outranks it and the section collapses */
    .rec-wrap > section.rec-voices { padding:clamp(70px, 9vh, 124px) 0
                                             clamp(90px, 12vh, 150px); }
    /* at least one screen tall, so the scroll that lightens the ground is the
       scroll that brings the rows in */
    .rec-voices { position:relative; width:100%; box-sizing:border-box;
                  min-height:100vh;
                  display:flex; flex-direction:column; justify-content:center; }
    .rec-voices-h { width:min(760px, 88vw); margin:0 auto clamp(44px, 6.5vh, 82px);
                    text-align:center; color:#1A1430;
                    font-size:clamp(22px, 1.5vw + 11px, 34px);
                    font-weight:600; line-height:1.24; letter-spacing:-0.025em;
                    text-wrap:balance;
                    opacity:var(--vh, 0);
                    transform:translateY(calc((1 - var(--vh, 0)) * 20px)); }
    /* two rows of three. `1fr` rows rather than auto: the quotes are different
       lengths, and auto rows would make the second row shallower than the
       first, which reads as crooked rather than as two rows */
    .rec-voices-grid { width:min(1180px, 92vw); margin-inline:auto;
                       display:grid; grid-template-columns:repeat(3, 1fr);
                       grid-auto-rows:1fr; gap:clamp(14px, 1.6vw, 24px);
                       opacity:var(--vh, 0);
                       transform:translateY(calc((1 - var(--vh, 0)) * 26px)); }
    .rec-voice { margin:0; display:flex; flex-direction:column;
                 align-items:center; justify-content:center; text-align:center;
                 box-sizing:border-box; border-radius:18px;
                 padding:clamp(24px, 2.6vw, 34px) clamp(20px, 2.2vw, 30px);
                 background:#FFFFFF; border:1px solid rgba(124,92,246,.15);
                 box-shadow:0 6px 22px rgba(58,38,116,.07); }
    /* set in type, not drawn: every company here is invented */
    .rec-voice-mark { color:var(--ink, #5B3FD0); text-transform:uppercase;
                      font-size:clamp(10.5px, 0.2vw + 9.5px, 12.5px);
                      font-weight:700; letter-spacing:.15em;
                      margin-bottom:clamp(14px, 1.6vw, 20px); }
@INKS@
    .rec-voice blockquote { margin:0 0 clamp(14px, 1.6vw, 20px);
                            font-family:Georgia, 'Times New Roman', Times, serif;
                            font-style:italic; color:#1A1430;
                            font-size:clamp(16px, 0.55vw + 11px, 20px);
                            line-height:1.45; letter-spacing:-0.008em;
                            text-wrap:balance; }
    .rec-voice blockquote::before { content:"\\201C"; }
    .rec-voice blockquote::after { content:"\\201D"; }
    .rec-voice figcaption { display:flex; align-items:center; justify-content:center;
                            flex-wrap:wrap; gap:7px; margin-top:auto;
                            font-size:clamp(11.5px, 0.15vw + 10.5px, 12.5px); }
    .rec-voice figcaption b { font-weight:600; color:#2C2545; }
    .rec-voice figcaption span { color:#A79FC8; }
    .rec-voice figcaption i { font-style:normal; color:#6F6790; }
    /* the closing words step aside before the ground under them lightens */
    .rec-say-last { opacity:calc(1 - var(--vout, 0)); }
    @media (max-width:1000px) {
      .rec-voices-grid { grid-template-columns:repeat(2, 1fr); }
    }
    @media (max-width:640px) {
      .rec-voices-grid { grid-template-columns:1fr; grid-auto-rows:auto; }
    }
    @media (prefers-reduced-motion: reduce) {
      .rec-voices-h, .rec-voices-grid { transform:none; }
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

    assert s.count('class="rec-voice"') == 6, path + ': one deck expected'
    for gone in ('rec-voices-track', 'rec-voices-rail', 'rec-voices-dots',
                 'rec-voices-run', 'rec-voices-dot', '--vstep', '--vfade'):
        assert gone not in s, path + ': ' + gone + ' is still there'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
