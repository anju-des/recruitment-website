# -*- coding: utf-8 -*-
"""Publish asks for an account first.

It sits after the review rather than as a fifth question, and carries no step
counter: the three questions are the brief, and this is the gate in front of
it.

The screen says plainly that nothing is sent. People type real addresses into
boxes like this one, and this page has nowhere to send them.
"""
import io
import sys

EDITS = [
    # the review hands on to the gate, and the gate hands on to the tick
    ("""      function go() {
        if (at < STEPS.length) {
          if (step.range) brief[step.key] = said(step.range);
          else if (step.multi) { /* already in brief.skills */ }
          else if (!step.tags && input) brief[step.key] = input.value.trim();
          if (next && next.disabled) return;
        }
        if (at >= STEPS.length) { done(); return; }
        onward();
      }""",
     """      function go() {
        // hoisted: every screen's forward button is gated the same way
        if (next && next.disabled) return;
        if (at < STEPS.length) {
          if (step.range) brief[step.key] = said(step.range);
          else if (step.multi) { /* already in brief.skills */ }
          else if (!step.tags && input) brief[step.key] = input.value.trim();
        }
        if (at > STEPS.length) { done(); return; }
        onward();
      }"""),

    ("""      card.innerHTML = at < STEPS.length ? ask(STEPS[at]) : review();""",
     """      card.innerHTML = at < STEPS.length ? ask(STEPS[at])
                     : at === STEPS.length ? review() : signup();"""),

    ("""      flow.querySelector('.rec-flow-step').textContent =
        'Step ' + Math.min(at + 1, total) + ' of ' + total;
      flow.querySelector('.rec-flow-bar span').style.setProperty(
        '--at', Math.round((at + 1) / total * 100) + '%');""",
     """      // the gate is not one of the questions, so it takes no number
      flow.querySelector('.rec-flow-step').textContent =
        at > STEPS.length ? '' : 'Step ' + (at + 1) + ' of ' + total;
      flow.querySelector('.rec-flow-bar span').style.setProperty(
        '--at', Math.round(Math.min(at + 1, total) / total * 100) + '%');"""),

    ("""    function done() {""",
     """    function signup() {
      return '<h2 class="rec-flow-q">Create your account</h2>' +
        '<p class="rec-flow-hint">The brief is ready. Add your work email and ' +
        'Mira starts reading.</p>' +
        '<input class="rec-flow-in rec-flow-mail" type="email" ' +
        'inputmode="email" autocomplete="email" placeholder="you@company.com" ' +
        'aria-label="Work email">' +
        '<div class="rec-flow-act">' +
          '<button type="button" class="rec-flow-back">Back</button>' +
          '<button type="button" class="rec-flow-next">Create account</button>' +
        '</div>' +
        '<p class="rec-flow-note">Nothing is sent anywhere. This is a ' +
        'walk-through of the flow.</p>';
    }

    function done() {"""),

    # the address box, and the button it governs
    ("""      var chips = card.querySelectorAll('.rec-flow-chip');""",
     """      var mail = card.querySelector('.rec-flow-mail');
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

      var chips = card.querySelectorAll('.rec-flow-chip');"""),

    ("""    .rec-flow-chips { display:flex; flex-wrap:wrap; gap:9px; margin-top:14px;""",
     """    .rec-flow-mail { max-width:380px; margin-inline:auto; text-align:center; }
    .rec-flow-chips { display:flex; flex-wrap:wrap; gap:9px; margin-top:14px;"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-flow-mail' not in s, path + ': already has the gate'
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
