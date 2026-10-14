# -*- coding: utf-8 -*-
"""Two rows of wider cards, drifting right to left.

The grid becomes two tracks, each carrying its three quotes twice over and
travelling exactly one copy, so the lap closes on the same picture it opened
with. The second row starts half a lap in, or the two would move as one slab.

It is slow on purpose -- about 35 pixels a second, a lap taking the best part
of a minute. A row that hurries is a row nobody reads. Hovering stops the row
under the pointer, which is also what makes a moving card clickable.

Clipping is split in two. The section hides the horizontal overflow, because a
mask hides a thing without shortening the page it sticks out of, and a track
three screens wide would otherwise scroll the page sideways. The fade at the
ends is a mask on the row, and a mask clips to its own border box -- so the
row keeps 44px of room above and below for a card to rise into on hover, and
gives that room straight back with a negative margin.
"""
import io
import sys

VOICES = [
    ('Devika Rao', 'Head of Engineering, Halyard',
     'Two roles closed in a month and nobody on my team opened a CV. The '
     'shortlist was short, which is the part I didn&#8217;t expect.'),
    ('Tomas Lindqvist', 'Talent Lead, Tessellate',
     'I still make the call on every hire. I&#8217;ve just stopped losing '
     'Thursdays to finding an hour three people can agree on.'),
    ('Priya Menon', 'Founder, Brightfold',
     'The scorecard goes in once and every candidate comes back measured '
     'against it. For a team our size that&#8217;s the whole thing.'),
    ('Adaeze Okafor', 'VP People, Crosslight',
     'Time to offer went from six weeks to eleven days, and the candidates '
     'noticed before we did.'),
    ('J&#250;lia Ferreira', 'Engineering Manager, Northbeam',
     'The interview notes are written before I&#8217;m out of the room. I '
     'read them now instead of writing them.'),
    ('Sam Kwon', 'COO, Larkfield',
     'We hired across four time zones without a coordinator. That used to be '
     'a full job.'),
]

CARD = """                <figure class="rec-voice" tabindex="0" role="button"
                        aria-haspopup="dialog"%s>
                  <blockquote>%s</blockquote>
                  <figcaption>
                    <b>%s</b>
                    <span aria-hidden="true">&#183;</span>
                    <i>%s</i>
                  </figcaption>
                </figure>"""


def deck(rows, hidden):
    tag = ' aria-hidden="true"' if hidden else ''
    return '\n'.join(CARD % (tag, q, name, role) for name, role, q in rows)


def row(rows, n):
    return """            <div class="rec-voices-row">
              <div class="rec-voices-track">
%s
%s
              </div>
            </div>""" % (deck(rows, False), deck(rows, True))


MARKUP = """
        <!-- the ground comes back to the light, and the rows drift across it -->
        <section class="rec-voices">
          <h2 class="rec-voices-h">What the hiring teams say</h2>
          <div class="rec-voices-rows">
%s
%s
          </div>
        </section>""" % (row(VOICES[:3], 1), row(VOICES[3:], 2))

OLD_CSS_HEAD = """    /* two rows of three. `1fr` rows rather than auto: the quotes are different
       lengths, and auto rows would make the second row shallower than the
       first, which reads as crooked rather than as two rows */
    /* The mask clips to this element's own border box, so a card lifting on
       hover lost its top to it. The box gets room above and below, and the
       negative margin takes that room back off the layout, so nothing moves
       but there is somewhere for a card to rise into. */
    .rec-voices-grid { width:min(1600px, 94vw); margin-inline:auto;
                       padding-block:44px; margin-block:-44px;
                       display:grid; grid-template-columns:repeat(3, 1fr);
                       grid-auto-rows:1fr; gap:clamp(14px, 1.6vw, 24px);
                       opacity:var(--vh, 0);
                       transform:translateY(calc((1 - var(--vh, 0)) * 26px));
                       /* the ends give out rather than stop, so the rows read
                          as carrying on past the page instead of ending in a
                          hard column of white */
                       --vfade:clamp(36px, 6vw, 120px);
                       -webkit-mask-image:linear-gradient(90deg,
                         transparent 0, #000 var(--vfade),
                         #000 calc(100% - var(--vfade)), transparent 100%);
                       mask-image:linear-gradient(90deg,
                         transparent 0, #000 var(--vfade),
                         #000 calc(100% - var(--vfade)), transparent 100%); }
    .rec-voice { margin:0; display:flex; flex-direction:column;"""

NEW_CSS_HEAD = """    .rec-voices-rows { display:flex; flex-direction:column;
                       gap:clamp(14px, 1.6vw, 24px);
                       --vg:clamp(14px, 1.6vw, 24px);
                       --vcard:clamp(320px, 36vw, 560px);
                       --vfade:clamp(40px, 7vw, 160px);
                       opacity:var(--vh, 0);
                       transform:translateY(calc((1 - var(--vh, 0)) * 26px)); }
    /* The fade at the ends is a mask, and a mask clips to its own border box,
       so a card rising on hover lost its top to it. The row keeps room above
       and below and hands that room straight back with a negative margin:
       nothing moves, and there is somewhere to rise into. */
    .rec-voices-row { position:relative; width:100%;
                      padding-block:44px; margin-block:-44px;
                      -webkit-mask-image:linear-gradient(90deg,
                        transparent 0, #000 var(--vfade),
                        #000 calc(100% - var(--vfade)), transparent 100%);
                      mask-image:linear-gradient(90deg,
                        transparent 0, #000 var(--vfade),
                        #000 calc(100% - var(--vfade)), transparent 100%); }
    /* two copies of the three, travelling exactly one copy: half the track
       plus half a gap, since the track holds one gap fewer than twice the
       cards. The lap closes on the picture it opened with. */
    .rec-voices-track { display:flex; align-items:stretch; gap:var(--vg);
                        width:max-content;
                        animation:rec-voices-drift 48s linear infinite; }
    @keyframes rec-voices-drift {
      from { transform:translateX(0); }
      to   { transform:translateX(calc(-50% - var(--vg) / 2)); }
    }
    /* half a lap in, or the two rows move as one slab */
    .rec-voices-row:nth-child(2) .rec-voices-track { animation-delay:-24s; }
    /* the row under the pointer stops, which is also what makes a moving card
       something you can click */
    .rec-voices-row:hover .rec-voices-track { animation-play-state:paused; }
    .rec-voice { flex:none; width:var(--vcard);
                 margin:0; display:flex; flex-direction:column;"""

OLD_SEC = """    .rec-voices { position:relative; width:100%; box-sizing:border-box;
                  min-height:100vh;
                  display:flex; flex-direction:column; justify-content:center; }"""
NEW_SEC = """    /* a mask hides what sticks out without shortening the page it sticks out
       of, so the horizontal overflow of a track three screens wide is clipped
       here instead */
    .rec-voices { position:relative; width:100%; box-sizing:border-box;
                  min-height:100vh; overflow:hidden;
                  display:flex; flex-direction:column; justify-content:center; }"""

OLD_MQ = """    @media (max-width:1000px) {
      .rec-voices-grid { grid-template-columns:repeat(2, 1fr); }
    }
    @media (max-width:640px) {
      /* one column has no outer edge to give out at: the fade would only dim
         both sides of every card */
      .rec-voices-grid { grid-template-columns:1fr; grid-auto-rows:auto;
                         width:min(520px, 92vw);
                         -webkit-mask-image:none; mask-image:none; }
    }"""
NEW_MQ = """    @media (max-width:640px) {
      .rec-voices-rows { --vcard:min(86vw, 340px); --vfade:clamp(20px, 7vw, 40px); }
    }"""

OLD_RM = """      .rec-voices-h, .rec-voices-grid { transform:none; }
      .rec-voice { transition:none; }"""
NEW_RM = """      .rec-voices-h, .rec-voices-rows { transform:none; }
      .rec-voice { transition:none; }
      .rec-voices-track { animation:none; }"""

MARK_HEAD = "        <!-- the ground comes back to the light"
MARK_TAIL = "        </section>"


def patch(path):
    s = io.open(path, encoding='utf-8').read()

    for old, new in ((OLD_SEC, NEW_SEC), (OLD_CSS_HEAD, NEW_CSS_HEAD),
                     (OLD_MQ, NEW_MQ), (OLD_RM, NEW_RM)):
        assert s.count(old) == 1, (path, old.strip()[:50], s.count(old))
        s = s.replace(old, new, 1)

    a = s.index(MARK_HEAD)
    b = s.index(MARK_TAIL, a) + len(MARK_TAIL)
    assert s[a:b].count('class="rec-voice"') == 6, path + ': markup changed'
    s = s[:a] + MARKUP.lstrip('\n') + s[b:]

    assert s.count('class="rec-voice"') == 12, path + ': two decks per row'
    assert 'rec-voices-grid' not in s, path + ': a grid reference is left'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
