# -*- coding: utf-8 -*-
"""Google on the gate, and the walk-through line off it.

The button is the one the product's own sign-in screen uses, so the two
screens offer the same two ways in.

The line goes as asked. The flow still says what it is one screen later --
the confirmation carries "Nothing has been posted" -- so nobody reaches the
end believing a role went live or an account was made.
"""
import io
import sys

GOOGLE = (
    '<svg viewBox=\\"0 0 48 48\\" aria-hidden=\\"true\\">'
    '<path fill=\\"#FFC107\\" d=\\"M43.6 20.5h-1.9V20H24v8h11.3c-1.6 4.7-6.1 8-11.3 8-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.9 1.2 8 3.1l5.7-5.7C34.6 6.1 29.6 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z\\"/>'
    '<path fill=\\"#FF3D00\\" d=\\"M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.9 1.2 8 3.1l5.7-5.7C34.6 6.1 29.6 4 24 4 16.3 4 9.7 8.3 6.3 14.7z\\"/>'
    '<path fill=\\"#4CAF50\\" d=\\"M24 44c5.5 0 10.5-2.1 14.3-5.5l-6.6-5.6C29.6 34.6 26.9 36 24 36c-5.2 0-9.6-3.3-11.3-7.9l-6.5 5C9.6 39.6 16.2 44 24 44z\\"/>'
    '<path fill=\\"#1976D2\\" d=\\"M43.6 20.5H24v8h11.3c-.8 2.3-2.2 4.2-4.1 5.6l6.6 5.6C41.4 36.9 44 31 44 24c0-1.3-.1-2.4-.4-3.5z\\"/>'
    '</svg>'
)

OLD = """      return '<h2 class="rec-flow-q">Create your account</h2>' +
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
        'walk-through of the flow.</p>';"""

NEW = """      return '<h2 class="rec-flow-q">Create your account</h2>' +
        '<p class="rec-flow-hint">The brief is ready. Add your work email and ' +
        'Mira starts reading.</p>' +
        '<button type="button" class="rec-flow-google">@GOOGLE@' +
        'Continue with Google</button>' +
        '<div class="rec-flow-or">or</div>' +
        '<input class="rec-flow-in rec-flow-mail" type="email" ' +
        'inputmode="email" autocomplete="email" placeholder="you@company.com" ' +
        'aria-label="Work email">' +
        '<div class="rec-flow-act">' +
          '<button type="button" class="rec-flow-back">Back</button>' +
          '<button type="button" class="rec-flow-next">Create account</button>' +
        '</div>';""".replace('@GOOGLE@', GOOGLE)

OLD_WIRE = """      var mail = card.querySelector('.rec-flow-mail');
      if (mail) {"""
NEW_WIRE = """      var google = card.querySelector('.rec-flow-google');
      if (google) google.addEventListener('click', done);

      var mail = card.querySelector('.rec-flow-mail');
      if (mail) {"""

OLD_CSS = """    .rec-flow-mail { max-width:380px; margin-inline:auto; text-align:center; }"""
NEW_CSS = """    .rec-flow-mail { max-width:380px; margin-inline:auto; text-align:center; }
    /* the same two ways in the product's own sign-in screen offers */
    .rec-flow-google { width:100%; max-width:380px; box-sizing:border-box;
                       height:46px; margin-inline:auto;
                       display:inline-flex; align-items:center;
                       justify-content:center; gap:10px; cursor:pointer;
                       border:1.5px solid #DCD6EE; border-radius:10px;
                       background:#FFFFFF; font:inherit; font-size:15px;
                       font-weight:600; color:#1A1430;
                       transition:background .15s, border-color .15s; }
    .rec-flow-google:hover { background:#F7F5FE; border-color:#BCAEF0; }
    .rec-flow-google svg { width:18px; height:18px; }
    .rec-flow-or { display:flex; align-items:center; gap:12px;
                   width:100%; max-width:380px; margin:18px auto;
                   font-size:12.5px; font-weight:500; color:#8A82A8; }
    .rec-flow-or::before, .rec-flow-or::after { content:""; flex:1; height:1px;
                                                background:#E7E2F6; }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-flow-google' not in s, path + ': already has the button'
    for old, new in ((OLD, NEW), (OLD_WIRE, NEW_WIRE), (OLD_CSS, NEW_CSS)):
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert 'walk-through of the flow.</p>' not in s, path + ': note still there'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
