# -*- coding: utf-8 -*-
"""A black footer under the testimonials.

This one brings its own ground rather than taking another leg on the sky
ramp. Every other change of ground on this page is a transition -- one thing
becoming another while you scroll through it -- and the ramp is what keeps
those from showing a seam. A footer is not that. It is a slab at the end, and
a slab is supposed to have an edge.

The columns name what the page itself showed: the four stages, by the words
used on the stage rail. The links are hashes, like the header's own, since
there is nowhere else to go yet.

The wordmark is the same dark file the header uses, run through
`brightness(0) invert(1)`: that flattens every opaque pixel to black and then
to white while leaving the alpha alone, which is exactly a white version of a
solid monochrome mark, and saves carrying a second file.
"""
import io
import sys

COLUMNS = [
    ('Platform', ['Screening', 'Interviews', 'Scorecards', 'Offers']),
    ('Solutions', ['Startups', 'Scale-ups', 'Agencies']),
    ('Resources', ['Pricing', 'Help centre', 'Contact']),
]


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
        <div class="rec-foot-top">
          <div class="rec-foot-brand">
            <img src="mira-logo.svg" width="1152" height="365" alt="Mira">
            <p>The recruiting agent behind Wisemonk Recruit. It reads every
               application, books the interviews and keeps the record. You make
               the calls.</p>
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
      </footer>""" % '\n'.join(column(t, i) for t, i in COLUMNS)

CSS = """
    /* ---- footer ------------------------------------------------------------ */
    /* Its own ground, not another leg on the sky ramp. Every other change of
       ground here is a transition and the ramp is what keeps those seamless;
       a footer is a slab at the end, and a slab is meant to have an edge. */
    .rec-foot { position:relative; background:#0A0616; color:#9A93B4;
                padding:clamp(56px, 7vh, 88px) clamp(22px, 5vw, 72px)
                        clamp(22px, 3vh, 32px);
                font-size:14px; line-height:1.6; }
    .rec-foot-top { width:min(1180px, 100%); margin-inline:auto;
                    display:flex; flex-wrap:wrap; gap:clamp(32px, 5vw, 80px);
                    align-items:flex-start;
                    padding-bottom:clamp(36px, 5vh, 60px); }
    .rec-foot-brand { flex:1 1 320px; max-width:420px; }
    /* the header's own dark wordmark, flattened to black and then inverted:
       white where it is opaque, untouched where it is not */
    .rec-foot-brand img { display:block; width:124px; height:auto;
                          margin-bottom:18px;
                          filter:brightness(0) invert(1); opacity:.92; }
    .rec-foot-brand p { margin:0; color:#8E86AC; font-size:14px; max-width:38ch; }
    .rec-foot-cols { flex:1 1 420px; display:flex; flex-wrap:wrap;
                     gap:clamp(28px, 4vw, 64px); }
    .rec-foot-col { min-width:124px; }
    .rec-foot-col h3 { margin:0 0 14px; color:#FFFFFF; font-size:13px;
                       font-weight:600; letter-spacing:.02em; }
    .rec-foot-col ul { margin:0; padding:0; list-style:none;
                       display:flex; flex-direction:column; gap:9px; }
    .rec-foot a { color:#9A93B4; text-decoration:none;
                  transition:color .15s; }
    .rec-foot a:hover, .rec-foot a:focus-visible { color:#FFFFFF; }
    .rec-foot a:focus-visible { outline:2px solid #7C5CF6; outline-offset:3px;
                                border-radius:3px; }
    .rec-foot-base { width:min(1180px, 100%); margin-inline:auto;
                     padding-top:clamp(18px, 2.4vh, 26px);
                     border-top:1px solid rgba(201,184,255,.12);
                     display:flex; flex-wrap:wrap; gap:14px 28px;
                     align-items:center; justify-content:space-between; }
    .rec-foot-base small { color:#6E6690; font-size:12.5px; }
    .rec-foot-base nav { display:flex; flex-wrap:wrap; gap:22px;
                         font-size:12.5px; }
    @media (prefers-reduced-motion: reduce) {
      .rec-foot a { transition:none; }
    }
"""

CSS_MARK = "    /* ---- suggestions ------"
SEC_TAIL = "        </section>"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-foot' not in s, path + ': already has a footer'

    assert s.count(CSS_MARK) == 1, path + ': suggestions marker changed'
    s = s.replace(CSS_MARK, CSS.lstrip('\n') + '\n' + CSS_MARK, 1)

    i = s.rindex(SEC_TAIL) + len(SEC_TAIL)
    s = s[:i] + '\n' + MARKUP.lstrip('\n') + s[i:]

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
