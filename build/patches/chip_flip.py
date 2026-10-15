# -*- coding: utf-8 -*-
"""The hero chip turns over to a second message.

The swap happens at the halfway frame, where the chip is edge-on and
invisible, so the width change between two different-length lines is never
seen -- which is why this flips the whole pill rather than cross-fading the
text inside a fixed box.

The flip rides a wrapper, not the chip itself: the chip already uses
transform for its hover lift, and an animation on the same element would
win every argument with it.

It holds while a pointer is on it or focus is inside it, and under
prefers-reduced-motion it swaps the words with no rotation at all rather
than stopping -- the second message is the point, not the animation.
"""
import io
import sys

OLD_MARKUP = """          <a class="rec-chip" href="#mira">
            <span class="rec-chip-dot" aria-hidden="true"></span>
            Mira, your AI recruiting agent
            <span class="rec-chip-more">Read more<svg viewBox="0 0 24 24" fill="none\""""

NEW_MARKUP = """          <span class="rec-chip-flip">
          <a class="rec-chip" href="#mira">
            <span class="rec-chip-dot" aria-hidden="true"></span>
            <span class="rec-chip-text">Mira, your AI recruiting agent</span>
            <span class="rec-chip-more">Read more<svg viewBox="0 0 24 24" fill="none\""""

OLD_SHUT = """<path d="M9.4 7.5h7.1v7.1"/></svg></span>
          </a>
          <h1>Hire the right talent, anywhere in the"""

NEW_SHUT = """<path d="M9.4 7.5h7.1v7.1"/></svg></span>
          </a>
          </span>
          <h1>Hire the right talent, anywhere in the"""

OLD_CSS = """    .rec-chip { display:inline-flex; align-items:center; gap:14px; margin-bottom:32px;"""

NEW_CSS = """    /* the pill turns over; the words change while it is edge-on */
    .rec-chip-flip { display:inline-block; margin-bottom:32px; }
    .rec-chip-flip > .rec-chip { margin-bottom:0; }
    .rec-chip-flip.is-turn { animation:rec-chip-turn .62s ease both; }
    @keyframes rec-chip-turn {
      0%   { transform:perspective(620px) rotateX(0deg); }
      49%  { transform:perspective(620px) rotateX(90deg); }
      51%  { transform:perspective(620px) rotateX(-90deg); }
      100% { transform:perspective(620px) rotateX(0deg); }
    }
    @media (prefers-reduced-motion: reduce) {
      .rec-chip-flip.is-turn { animation:none; }
    }
    .rec-chip { display:inline-flex; align-items:center; gap:14px; margin-bottom:32px;"""

JS = r"""
  // The hero chip carries two messages. The words change at the halfway
  // frame, where the pill is edge-on, so the width difference is never seen.
  (function () {
    var flip = document.querySelector('.rec-chip-flip');
    var text = flip && flip.querySelector('.rec-chip-text');
    if (!flip || !text) return;

    var SAYS = ['Mira, your AI recruiting agent', 'Pay only on a hire'];
    var at = 0;
    var held = false;
    var still = window.matchMedia('(prefers-reduced-motion: reduce)');

    function turn() {
      if (held) return;
      at = (at + 1) % SAYS.length;
      if (still.matches) { text.textContent = SAYS[at]; return; }
      flip.classList.add('is-turn');
      window.setTimeout(function () { text.textContent = SAYS[at]; }, 300);
      window.setTimeout(function () { flip.classList.remove('is-turn'); }, 640);
    }

    window.setInterval(turn, 5200);

    // leave it alone while someone is reading it or tabbing through it
    flip.addEventListener('mouseenter', function () { held = true; });
    flip.addEventListener('mouseleave', function () { held = false; });
    flip.addEventListener('focusin', function () { held = true; });
    flip.addEventListener('focusout', function () { held = false; });
  }());
"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-chip-flip' not in s, path + ': already flips'
    for old, new in ((OLD_MARKUP, NEW_MARKUP), (OLD_SHUT, NEW_SHUT),
                     (OLD_CSS, NEW_CSS)):
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    i = s.rindex('</script>')
    s = s[:i] + JS + s[i:]
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
