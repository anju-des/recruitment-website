# -*- coding: utf-8 -*-
"""The account screen goes.

The flow is now the website, its lookup, and the tick: one question and
what Mira finds from it.

draw() takes over the ending. It used to hand anything past the last step
to signup(); with that gone it calls done() itself, which also means the
skip reaches the end the same way a filled-in website does.

The handlers for the Google button and the email field go with the screen
-- unlike the chip machinery kept last time, these were written for this
one screen and generalise to nothing.
"""
import io
import sys

EDITS = [
    ("""      card.innerHTML = at < STEPS.length ? ask(STEPS[at]) : signup();
      wire(card);""",
     """      if (at >= STEPS.length) { done(); return; }
      card.innerHTML = ask(STEPS[at]);
      wire(card);"""),

    ("""      var google = card.querySelector('.rec-flow-google');
      if (google) google.addEventListener('click', done);

      var mail = card.querySelector('.rec-flow-mail');
      if (mail) {
        var looksLikeAddress = function () {
          next.disabled =
            !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{2,}$/.test(mail.value.trim());
        };
        mail.addEventListener('input', looksLikeAddress);
        mail.addEventListener('keydown', function (e) {
          if (e.key === 'Enter') { e.preventDefault(); go(); }
        });
        looksLikeAddress();
        mail.focus();
      }

""", ""),
]

CUT = ("    function signup() {", "    function done() {")


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    a = s.index(CUT[0])
    b = s.index(CUT[1], a)
    s = s[:a] + s[b:]

    # only the script matters; the stylesheet keeps its now-unused rules
    js = s[s.rindex('<script>'):]
    for gone in ('function signup(', 'rec-flow-mail', 'rec-flow-google',
                 'Create your account'):
        assert gone not in js, path + ': ' + gone + ' survives in the script'
    assert 'function done(' in s, path + ': the ending went too'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
