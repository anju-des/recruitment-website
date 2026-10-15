# -*- coding: utf-8 -*-
"""Connect opens their Claude with the question already typed.

No account, no connector: claude.ai/new?q=... lands them in a fresh chat
with the prompt in the box. They send it, Claude writes the profile, they
bring it back and paste it in with the role. The whole loop needs nothing
from us, which is why it can ship.

The prompt tells Claude not to guess. A hiring profile is going to be read
as fact by whoever picks up the role, and an invented headcount or an
invented stack would travel a long way before anyone caught it.

The panel then says plainly that nothing was sent anywhere, because that is
true and because "connect your Claude" is the kind of phrase that makes
people wonder.
"""
import io
import sys

MARK = ("'<svg class=\"rec-cx-mark\" viewBox=\"0 0 24 24\" fill=\"currentColor\" ' +\n"
        "          'aria-hidden=\"true\"><path d=\"M12 3c.6 4.2 1.8 5.4 6 6-4.2.6-5.4 ' +\n"
        "          '1.8-6 6-.6-4.2-1.8-5.4-6-6 4.2-.6 5.4-1.8 6-6z\"/></svg>'")

CONSTS = """    // what we put in their box. "Do not guess" is load-bearing: this text
    // comes back as a hiring profile and gets read as fact.
    var PROMPT = [
      'I am briefing a role to Wisemonk\\'s AI recruiter, Mira, and it works',
      'better when it knows how we hire.',
      '',
      'Write me a short hiring profile I can paste in \\u2014 around 150 words,',
      'plain prose, no headings or bullet points. Cover what you already know',
      'about:',
      '',
      '- the company: what we do, roughly how big we are, where the team works',
      '- the team this hire would join, and the stack they would work in',
      '- how we hire: the levels we use, what we hold the bar on, what the',
      '  last search got wrong',
      '- me: my name and what I do here',
      '',
      'Do not guess. If you do not know something, leave it out and ask me',
      'instead.'
    ].join('\\n');
    var ASK_URL = 'https://claude.ai/new?q=' + encodeURIComponent(PROMPT);

    var opener = document.querySelector('.rec-cx');"""

EDITS = [
    ("""    var opener = document.querySelector('.rec-cx');""", CONSTS),

    # the call to action, and the line under it
    ("""          '<button type="button" class="rec-cxp-do">Connect your Claude</button>' +
          '<p class="rec-cxp-note">Connecting is tied to your workspace, so ' +
            'your account comes first.</p>' +""",
     """          '<button type="button" class="rec-cxp-do">Open it in Claude</button>' +
          '<button type="button" class="rec-cxp-copy">or copy the prompt' +
            '</button>' +"""),

    # what the call to action does
    ("""      panel.querySelector('.rec-cxp-do').addEventListener('click', function () {
        close();
        // connecting is account-shaped, so it starts where accounts start
        var login = document.querySelector('.rec-head .rec-login');
        if (login) window.setTimeout(function () { login.click(); }, 180);
      });""",
     """      panel.querySelector('.rec-cxp-do').addEventListener('click', function () {
        window.open(ASK_URL, '_blank', 'noopener');
        step_two();
      });

      var copy = panel.querySelector('.rec-cxp-copy');
      copy.addEventListener('click', function () {
        var done = function () { copy.textContent = 'Copied'; };
        var not = function () { copy.textContent = 'Select it and copy'; };
        try {
          if (navigator.clipboard) navigator.clipboard.writeText(PROMPT)
                                     .then(done, not);
          else not();
        } catch (e) { not(); }
      });"""),

    # the screen after it, and the way back to the role
    ("""    function close() {
      panel.classList.add('is-out');
      window.setTimeout(function () {
        panel.hidden = true;
        panel.classList.remove('is-out');
        opener.focus();
      }, 160);
    }""",
     """    function close() {
      panel.classList.add('is-out');
      window.setTimeout(function () {
        panel.hidden = true;
        panel.classList.remove('is-out');
        opener.focus();
      }, 160);
    }

    function step_two() {
      var card = panel.querySelector('.rec-cxp-card');
      card.innerHTML =
        '<div class="rec-cxp-top">' + @MARK@ +
          '<button type="button" class="rec-cxp-x" aria-label="Close">' +
            '\\u00d7</button>' +
        '</div>' +
        '<h2>Now bring it back</h2>' +
        '<p>Claude is writing your hiring profile in the tab that just ' +
          'opened. Send the message, then paste what comes back into the box ' +
          'here, along with the role.</p>' +
        '<p>Nothing was sent anywhere. It goes from your Claude to your ' +
          'clipboard to this page, and no further until you post the role.</p>' +
        '<button type="button" class="rec-cxp-do rec-cxp-back">Back to the ' +
          'brief</button>';
      card.querySelector('.rec-cxp-x').addEventListener('click', close);
      card.querySelector('.rec-cxp-back').addEventListener('click', function () {
        close();
        var field = document.querySelector('.rec-compose-input');
        if (field) window.setTimeout(function () { field.focus(); }, 200);
      });
      card.focus();
    }""".replace('@MARK@', MARK)),

    # the line under the button is gone; so is its rule
    ("""    .rec-cxp-note { margin:14px 0 0; font-size:13px; line-height:1.55;
                    color:#8A82A8; text-align:center; }""",
     """    .rec-cxp-copy { display:block; width:100%; margin-top:9px; padding:4px;
                    border:0; background:none; cursor:pointer; font:inherit;
                    font-size:13px; color:#8A82A8; text-align:center; }
    .rec-cxp-copy:hover { color:#5A4BD8; }"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'ASK_URL' not in s, path + ': already deep-links'
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:50], s.count(old))
        s = s.replace(old, new, 1)
    assert 'rec-cxp-note' not in s, path + ': the old line survives'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
