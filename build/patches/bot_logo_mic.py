# -*- coding: utf-8 -*-
"""The full wordmark in the bubble's header, and a mic beside its send.

The header carried the mark plus the word set in the page's own type, which
is a lockup rebuilt by hand next to a real one. Use the logo.

The mic is the hero composer's mic, not a second one: that dictation was
written as an IIFE bound to one pair of elements, so it becomes a function
the bubble can call for its own field when it builds. Nothing about the
behaviour changes -- the same restart-on-pause, the same refusal to become a
button in a browser with no SpeechRecognition to back it.
"""
import io
import sys

EDITS = [
    # ---- the dictation becomes something the bubble can ask for -----------
    ("""  (function () {
    var Rec = window.SpeechRecognition || window.webkitSpeechRecognition;
    var icon = document.querySelector('.rec-compose-mic');
    var field = document.querySelector('.rec-compose-input');
    var list = document.querySelector('.rec-suggest');
    if (!Rec || !icon || !field) return;""",
     """  // Shared, because the bubble's composer wants exactly this and is built
  // too late to be found from here. `what` finishes the button's label.
  window.recDictate = function (icon, field, list, what) {
    var Rec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!Rec || !icon || !field) return;"""),

    ("""    var form = field.closest('form');
    if (form) form.addEventListener('submit', function () { if (on) stop(); });
  }());""",
     """    var form = field.closest('form');
    if (form) form.addEventListener('submit', function () { if (on) stop(); });
  };

  // the hero's composer, wired at load; the bubble wires its own on open
  window.recDictate(document.querySelector('.rec-compose-mic'),
                    document.querySelector('.rec-compose-input'),
                    document.querySelector('.rec-suggest'), 'the role');"""),

    ("""    mic.setAttribute('aria-label', 'Dictate the role');""",
     """    mic.setAttribute('aria-label', 'Dictate ' + what);"""),

    ("""      mic.setAttribute('aria-label', state ? 'Stop dictating' : 'Dictate the role');""",
     """      mic.setAttribute('aria-label',
                       state ? 'Stop dictating' : 'Dictate ' + what);"""),

    # a one-line field has no height to grow
    ("""    function grow() {
      field.style.height = 'auto';""",
     """    function grow() {
      if (field.tagName !== 'TEXTAREA') return;
      field.style.height = 'auto';"""),

    # ---- the wordmark ------------------------------------------------------
    ("""          '<img src="mira-mark.svg" alt="" width="412" height="300">' +
          '<b>Mira</b><i>Usually replies instantly</i>' +""",
     """          '<img src="mira-logo.svg" alt="Mira" width="1152" height="365">' +
          '<i>Usually replies instantly</i>' +"""),

    ("""    .rec-bot-head img { width:22px; height:auto; display:block; }
    .rec-bot-head b { font-size:14.5px; font-weight:600; color:#1A1430; }""",
     """    .rec-bot-head img { height:21px; width:auto; display:block; }"""),

    # ---- the mic, left of send --------------------------------------------
    ("""          '<button type="submit" class="rec-bot-send" aria-label="Send">' +""",
     """          '<span class="rec-bot-mic" aria-hidden="true">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
              'stroke-width="1.9" stroke-linecap="round" ' +
              'stroke-linejoin="round" aria-hidden="true">' +
              '<rect x="9" y="3" width="6" height="11" rx="3"/>' +
              '<path d="M5.5 11.5a6.5 6.5 0 0 0 13 0"/>' +
              '<path d="M12 18v3"/></svg>' +
          '</span>' +
          '<button type="submit" class="rec-bot-send" aria-label="Send">' +"""),

    ("""      panel.querySelector('.rec-bot-say').addEventListener('submit', function (e) {
        e.preventDefault();
        send(field.value);
      });""",
     """      panel.querySelector('.rec-bot-say').addEventListener('submit', function (e) {
        e.preventDefault();
        send(field.value);
      });
      // the same dictation the hero has; a span if the browser cannot
      if (window.recDictate) {
        window.recDictate(panel.querySelector('.rec-bot-mic'), field, null,
                          'your question');
      }"""),

    ("""    .rec-bot-send { flex:none; width:34px; height:34px; border-radius:50%;""",
     """    .rec-bot-mic { flex:none; width:32px; height:32px; border-radius:50%;
                   position:relative; display:grid; place-items:center;
                   border:0; padding:0; background:none; color:#A49CC0;
                   transition:background .15s, color .15s; }
    .rec-bot-mic svg { width:17px; height:17px; display:block; }
    .rec-bot-mic.is-live { cursor:pointer; }
    .rec-bot-mic.is-live:hover { background:#F4F1FD; color:#6B6392; }
    .rec-bot-mic.is-live:focus-visible { outline:2px solid #7C5CF6;
                                         outline-offset:2px; }
    .rec-bot-mic.is-on { color:#FFFFFF; background:#7C5CF6; }
    .rec-bot-mic.is-on:hover { color:#FFFFFF; background:#6B4BE8; }
    .rec-bot-mic.is-on::after { content:""; position:absolute; inset:0;
                                border-radius:50%;
                                border:2px solid rgba(124,92,246,.5);
                                animation:rec-mic-ring 1.6s ease-out infinite; }
    .rec-bot-send { flex:none; width:34px; height:34px; border-radius:50%;"""),

    ("""      .rec-bot-open { transition:none; }
      .rec-bot-open:hover { transform:none; }""",
     """      .rec-bot-open { transition:none; }
      .rec-bot-open:hover { transform:none; }
      .rec-bot-mic { transition:none; }
      .rec-bot-mic.is-on::after { animation:none; }"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-bot-mic' not in s, path + ': already has the bubble mic'
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:50], s.count(old))
        s = s.replace(old, new, 1)
    assert 'Dictate the role' not in s, path + ': a fixed label is left'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
