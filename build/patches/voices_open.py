# -*- coding: utf-8 -*-
"""A card lifts under the pointer, and opens as a sheet when it is clicked.

The sheet is built in script and hung off <body> rather than written into the
section. A fixed element is positioned against the nearest transformed
ancestor rather than the viewport, and the grid above carries a transform for
its reveal -- inside it the backdrop would cover the grid instead of the page.

The page behind is scroll-driven, so the sheet swallows wheel and touch while
it is open: scrolling there would move the sky and the closing words about
underneath it and leave the reader somewhere else when it shut.
"""
import io
import sys

OLD_HEAD = '<h2 class="rec-voices-h">The people on the other end of it</h2>'
NEW_HEAD = '<h2 class="rec-voices-h">What the hiring teams say</h2>'

OLD_FIG = '              <figure class="rec-voice">'
NEW_FIG = ('              <figure class="rec-voice" tabindex="0" role="button"\n'
           '                      aria-haspopup="dialog">')

CSS_ANCHOR = """    /* the closing words step aside before the ground under them lightens */"""

CSS = """    /* a card lifts under the pointer, and opens as a sheet when clicked */
    .rec-voice { cursor:pointer;
                 transition:transform .22s cubic-bezier(.2,.7,.3,1),
                            box-shadow .22s ease; }
    .rec-voice:hover, .rec-voice:focus-visible {
      transform:translateY(-5px) scale(1.025);
      box-shadow:0 18px 44px rgba(58,38,116,.15); }
    .rec-voice:focus-visible { outline:2px solid #7C5CF6; outline-offset:3px; }
    /* `display:grid` below would beat the default [hidden] rule on its own */
    .rec-voice-modal[hidden] { display:none; }
    .rec-voice-modal { position:fixed; inset:0; z-index:200;
                       display:grid; place-items:center;
                       padding:clamp(16px, 4vw, 48px);
                       background:rgba(22,16,44,.55);
                       opacity:0; transition:opacity .2s ease; }
    .rec-voice-modal.is-on { opacity:1; }
    .rec-voice-sheet { position:relative; box-sizing:border-box;
                       width:min(680px, 100%); max-height:86vh; overflow:auto;
                       background:#FFFFFF; border-radius:22px; text-align:center;
                       padding:clamp(44px, 5vw, 62px) clamp(26px, 4vw, 56px);
                       box-shadow:0 30px 80px rgba(20,12,48,.3);
                       transform:translateY(12px) scale(.98);
                       transition:transform .22s cubic-bezier(.2,.7,.3,1); }
    .rec-voice-modal.is-on .rec-voice-sheet { transform:none; }
    .rec-voice-sheet blockquote { margin:0 0 clamp(18px, 2.4vw, 28px);
                                  font-family:Georgia, 'Times New Roman', Times, serif;
                                  font-style:italic; color:#1A1430;
                                  font-size:clamp(20px, 1.1vw + 13px, 30px);
                                  line-height:1.4; letter-spacing:-0.012em;
                                  text-wrap:balance; }
    .rec-voice-sheet blockquote::before { content:"\\201C"; }
    .rec-voice-sheet blockquote::after { content:"\\201D"; }
    .rec-voice-who { margin:0; display:flex; flex-wrap:wrap; gap:7px;
                     align-items:center; justify-content:center;
                     font-size:clamp(12.5px, 0.2vw + 11.5px, 14px); }
    .rec-voice-who b { font-weight:600; color:#2C2545; }
    .rec-voice-who span { color:#A79FC8; }
    .rec-voice-who i { font-style:normal; color:#6F6790; }
    .rec-voice-x { position:absolute; top:14px; right:14px;
                   width:36px; height:36px; border-radius:50%;
                   display:grid; place-items:center; cursor:pointer;
                   border:none; background:#F2EFFB; color:#4E4470;
                   font-size:20px; line-height:1; font-family:inherit;
                   transition:background .15s; }
    .rec-voice-x:hover { background:#E6E0F7; }
"""

OLD_RM = """    @media (prefers-reduced-motion: reduce) {
      .rec-voices-h, .rec-voices-grid { transform:none; }
    }"""
NEW_RM = """    @media (prefers-reduced-motion: reduce) {
      .rec-voices-h, .rec-voices-grid { transform:none; }
      .rec-voice, .rec-voice-modal, .rec-voice-sheet { transition:none; }
      .rec-voice:hover, .rec-voice:focus-visible { transform:none; }
      .rec-voice-modal.is-on .rec-voice-sheet { transform:none; }
    }"""

JS = """
  // A card opens as a sheet. It is built here and hung off <body>, not written
  // into the section: a fixed element is positioned against the nearest
  // transformed ancestor rather than the viewport, and the grid carries a
  // transform for its reveal, so inside it the backdrop would cover the grid
  // instead of the page.
  (function () {
    var cards = [].slice.call(document.querySelectorAll('.rec-voice'));
    if (!cards.length) return;

    var wrap = document.createElement('div');
    wrap.className = 'rec-voice-modal';
    wrap.hidden = true;
    wrap.innerHTML = '<div class="rec-voice-sheet" role="dialog" aria-modal="true"'
      + ' aria-label="Testimonial">'
      + '<button type="button" class="rec-voice-x" aria-label="Close">&#215;</button>'
      + '<blockquote></blockquote><p class="rec-voice-who"></p></div>';
    document.body.appendChild(wrap);

    var quote = wrap.querySelector('blockquote');
    var who = wrap.querySelector('.rec-voice-who');
    var shut = wrap.querySelector('.rec-voice-x');
    var from = null;

    function open(card) {
      quote.textContent = card.querySelector('blockquote').textContent;
      who.innerHTML = card.querySelector('figcaption').innerHTML;
      from = card;
      wrap.hidden = false;
      // a frame between showing it and the class, or the transition has
      // nothing to run from
      window.requestAnimationFrame(function () { wrap.classList.add('is-on'); });
      shut.focus();
    }

    function close() {
      wrap.classList.remove('is-on');
      window.setTimeout(function () { wrap.hidden = true; }, 220);
      if (from) from.focus();
      from = null;
    }

    cards.forEach(function (card) {
      card.addEventListener('click', function () { open(card); });
      card.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') {
          e.preventDefault();
          open(card);
        }
      });
    });

    shut.addEventListener('click', close);
    wrap.addEventListener('click', function (e) { if (e.target === wrap) close(); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !wrap.hidden) close();
    });
    // the close button is the only thing in here to land on
    wrap.addEventListener('keydown', function (e) {
      if (e.key === 'Tab') { e.preventDefault(); shut.focus(); }
    });
    // the page behind is scroll-driven: scrolling it now would move the sky
    // and the closing words about, and leave the reader somewhere else
    wrap.addEventListener('wheel', function (e) { e.preventDefault(); },
                          { passive: false });
    wrap.addEventListener('touchmove', function (e) { e.preventDefault(); },
                          { passive: false });
  }());
"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-voice-modal' not in s, path + ': already has the sheet'

    assert s.count(OLD_HEAD) == 1, path + ': heading changed'
    s = s.replace(OLD_HEAD, NEW_HEAD, 1)

    assert s.count(OLD_FIG) == 6, '%s: %d figures' % (path, s.count(OLD_FIG))
    s = s.replace(OLD_FIG, NEW_FIG)

    assert s.count(CSS_ANCHOR) == 1, path + ': css anchor changed'
    s = s.replace(CSS_ANCHOR, CSS + CSS_ANCHOR, 1)

    assert s.count(OLD_RM) == 1, path + ': reduced-motion block changed'
    s = s.replace(OLD_RM, NEW_RM, 1)

    i = s.rindex('</script>')
    s = s[:i] + JS + s[i:]

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
