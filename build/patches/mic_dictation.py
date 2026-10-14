# -*- coding: utf-8 -*-
"""Dictation on the mic, through the browser's own SpeechRecognition.

The icon stays in the markup as the decoration it was: it is part of the
picture of the product, and it should look the same in a browser that cannot
do this (Firefox has no SpeechRecognition at all). Script upgrades it to a
real button only where the API exists, which is also why the swap happens
here rather than in the HTML -- a button that does nothing is a worse promise
than a picture.

Two details worth keeping:

The example briefs open on `input`, so writing a transcript into the field
would pop that list open over the words as they arrive. Dictation writes the
value without dispatching, and closes the list when it starts.

The field is one row with its overflow hidden, which is fine for a line
someone types and not for a paragraph someone says. It grows to five rows
while dictating and scrolls after that.
"""
import io
import sys

CSS_OLD = """    /* decorative, like the + and the @: it is a picture of the field this
       stands in for, and a button here would announce a dictation this page
       cannot do */
    .rec-compose-mic { width:38px; height:38px; border-radius:50%;
                       display:grid; place-items:center; color:#9aa6b8; }
    .rec-compose-mic svg { width:19px; height:19px; display:block; }"""

CSS_NEW = """    /* A picture by default -- it looks the same in a browser with no
       SpeechRecognition to offer. Script turns it into a button where there
       is one, and `.is-live` is what that upgrade adds. */
    .rec-compose-mic { width:38px; height:38px; border-radius:50%;
                       display:grid; place-items:center; color:#9aa6b8;
                       border:0; background:none; padding:0; font:inherit;
                       position:relative;
                       transition:background .12s, color .12s; }
    .rec-compose-mic svg { width:19px; height:19px; display:block; }
    .rec-compose-mic.is-live { cursor:pointer; }
    .rec-compose-mic.is-live:hover { background:#F1F3F8; color:#5C6779; }
    .rec-compose-mic.is-live:focus-visible { outline:2px solid #7C5CF6;
                                             outline-offset:2px; }
    .rec-compose-mic.is-on { color:#FFFFFF; background:#7C5CF6; }
    .rec-compose-mic.is-on:hover { color:#FFFFFF; background:#6B4BE8; }
    /* a ring leaving the button, so it is plain that it is listening */
    .rec-compose-mic.is-on::after { content:""; position:absolute; inset:0;
                                    border-radius:50%; pointer-events:none;
                                    box-shadow:0 0 0 0 rgba(124,92,246,.45);
                                    animation:rec-mic-ring 1.6s ease-out infinite; }
    @keyframes rec-mic-ring {
      from { box-shadow:0 0 0 0 rgba(124,92,246,.45); }
      to   { box-shadow:0 0 0 13px rgba(124,92,246,0); }
    }
    @media (prefers-reduced-motion: reduce) {
      .rec-compose-mic { transition:none; }
      .rec-compose-mic.is-on::after { animation:none; }
    }"""

JS = """
  // Dictation, where the browser has it to give. Firefox has no
  // SpeechRecognition at all, so the icon is left as the decoration it is
  // rather than becoming a button that cannot do what it says.
  (function () {
    var Rec = window.SpeechRecognition || window.webkitSpeechRecognition;
    var icon = document.querySelector('.rec-compose-mic');
    var field = document.querySelector('.rec-compose-input');
    var list = document.querySelector('.rec-suggest');
    if (!Rec || !icon || !field) return;

    // the markup carries a span, because a button in a browser without the
    // API would be a promise the page cannot keep
    var mic = document.createElement('button');
    mic.type = 'button';
    mic.className = icon.className + ' is-live';
    mic.setAttribute('aria-label', 'Dictate the role');
    mic.setAttribute('aria-pressed', 'false');
    mic.innerHTML = icon.innerHTML;
    icon.parentNode.replaceChild(mic, icon);

    var rec = new Rec();
    rec.continuous = true;
    rec.interimResults = true;
    rec.lang = document.documentElement.lang || 'en-US';

    var on = false;
    var base = '';

    // one row is right for a line someone types and wrong for a paragraph
    // someone says
    function grow() {
      field.style.height = 'auto';
      var cap = parseFloat(getComputedStyle(field).lineHeight) * 5;
      field.style.height = Math.min(field.scrollHeight, cap) + 'px';
      field.style.overflowY = field.scrollHeight > cap ? 'auto' : 'hidden';
    }

    function mark(state) {
      on = state;
      mic.classList.toggle('is-on', state);
      mic.setAttribute('aria-pressed', state ? 'true' : 'false');
      mic.setAttribute('aria-label', state ? 'Stop dictating' : 'Dictate the role');
    }

    function start() {
      base = field.value.replace(/\\s+$/, '');
      try {
        rec.start();
      } catch (e) {
        return;                      // already running; the end event tidies up
      }
      mark(true);
      field.focus();
      // focusing opens the example briefs, and they would sit over the words
      // as they arrive
      if (list) list.hidden = true;
    }

    function stop() {
      mark(false);
      try { rec.stop(); } catch (e) {}
    }

    mic.addEventListener('click', function () {
      if (on) stop(); else start();
    });

    rec.addEventListener('result', function (e) {
      var done = '';
      var saying = '';
      for (var i = e.resultIndex; i < e.results.length; i++) {
        var text = e.results[i][0].transcript;
        if (e.results[i].isFinal) done += text; else saying += text;
      }
      if (done) base = (base + ' ' + done.trim()).trim();
      // written rather than dispatched: an input event here reopens the
      // briefs list on every syllable
      field.value = (base + (saying ? ' ' + saying.trim() : '')).trim();
      grow();
    });

    rec.addEventListener('end', function () { mark(false); });
    rec.addEventListener('error', function () { mark(false); });

    // it should not keep listening into a page the reader has moved on from
    window.addEventListener('pagehide', function () { if (on) stop(); });
    var form = field.closest('form');
    if (form) form.addEventListener('submit', function () { if (on) stop(); });
  }());
"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-mic-ring' not in s, path + ': already has dictation'

    assert s.count(CSS_OLD) == 1, path + ': mic CSS changed'
    s = s.replace(CSS_OLD, CSS_NEW, 1)

    i = s.rindex('</script>')
    s = s[:i] + JS + s[i:]

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
