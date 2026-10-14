# -*- coding: utf-8 -*-
"""A banner card across the top of the footer.

It takes the empty stretch the footer opened with and puts the ask in it: the
page has spent its whole length showing what Mira does and until now ended
without once saying what to do about it.

The copy is the page's own, not new claims -- the hero already says Mira ranks
every application against your scorecard as it arrives and that you pay only
when someone joins.

The two buttons need more weight than `.rec-foot a`, which sets every link in
here to the same muted violet. A single class loses to it: `.rec-foot a` is
one class and one element, so the plain `.rec-foot-cta-go` ties on classes
and loses on the element. Hence the two-class selectors.
"""
import io
import sys

MARKUP = """      <footer class="rec-foot">
        <div class="rec-foot-cta">
          <div class="rec-foot-cta-say">
            <h2>Your next hire is already in the pile.</h2>
            <p>Mira ranks every application against your scorecard as it
               arrives, books the interviews and keeps the record. You pay
               only when someone joins.</p>
          </div>
          <div class="rec-foot-cta-act">
            <a class="rec-foot-cta-go" href="#start">Start a role</a>
            <a class="rec-foot-cta-alt" href="#demo">Book a demo</a>
          </div>
        </div>
"""
OLD_OPEN = """      <footer class="rec-foot">
"""

CSS = """    /* the banner across the top: the page spends its length showing what
       Mira does and used to end without saying what to do about it */
    .rec-foot-cta { position:relative; z-index:1; width:100%;
                    box-sizing:border-box;
                    display:flex; flex-wrap:wrap; align-items:center;
                    justify-content:space-between; gap:clamp(22px, 3vw, 52px);
                    margin-bottom:clamp(30px, 4.5vh, 64px);
                    border-radius:clamp(18px, 1.6vw, 26px);
                    padding:clamp(28px, 3.2vw, 50px) clamp(26px, 3.2vw, 54px);
                    background:linear-gradient(135deg,
                      rgba(150,110,245,.26) 0%, rgba(58,86,226,.15) 100%);
                    box-shadow:inset 0 0 0 1px rgba(201,184,255,.18);
                    opacity:var(--fin, 0);
                    transform:translateY(calc((1 - var(--fin, 0)) * 18px)); }
    .rec-foot-cta-say { flex:1 1 420px; }
    .rec-foot-cta h2 { margin:0 0 10px; color:#FFFFFF;
                       font-size:clamp(21px, 1.3vw + 11px, 32px);
                       font-weight:600; line-height:1.2;
                       letter-spacing:-0.025em; text-wrap:balance; }
    .rec-foot-cta p { margin:0; color:#B4ADCB; font-size:14.5px;
                      max-width:56ch; }
    .rec-foot-cta-act { flex:none; display:flex; flex-wrap:wrap; gap:12px; }
    /* two classes, because `.rec-foot a` is a class and an element and would
       otherwise win and paint both of these the same muted violet */
    .rec-foot-cta .rec-foot-cta-go,
    .rec-foot-cta .rec-foot-cta-alt {
      display:inline-flex; align-items:center; border-radius:10px;
      padding:13px 24px; font-size:14.5px; font-weight:600;
      text-decoration:none; white-space:nowrap;
      transition:background .15s, color .15s; }
    .rec-foot-cta .rec-foot-cta-go { background:#FFFFFF; color:#1A1430; }
    .rec-foot-cta .rec-foot-cta-go:hover { background:#EDE9FC; }
    .rec-foot-cta .rec-foot-cta-alt { color:#E4DFF6;
      box-shadow:inset 0 0 0 1px rgba(201,184,255,.3); }
    .rec-foot-cta .rec-foot-cta-alt:hover { background:rgba(255,255,255,.09);
      color:#FFFFFF; }
    @media (prefers-reduced-motion: reduce) {
      .rec-foot-cta { transform:none; }
    }
"""

ANCHOR = """    /* Sand across the foot of the page."""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-foot-cta' not in s, path + ': already has the banner'

    assert s.count(OLD_OPEN) == 1, path + ': footer open tag changed'
    s = s.replace(OLD_OPEN, MARKUP, 1)

    assert s.count(ANCHOR) == 1, path + ': sand comment changed'
    s = s.replace(ANCHOR, CSS + ANCHOR, 1)

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
