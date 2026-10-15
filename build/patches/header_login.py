# -*- coding: utf-8 -*-
"""Log in opens the product's own sign-in screen.

Lifted from Recruitment-frontend: src/routes/Login.tsx for the markup and the
.login-* block of src/routes/Auth.css for the styling, with public/
login-graphic.html and public/mira.svg copied in beside the page. The right
panel is that same self-contained asset in the same iframe, so the two
screens cannot drift apart over a repaint of one of them.

What is dropped is the part this page cannot honour: the magic-link state
machine, the Google credential handler, the "check your inbox" screen. Every
way forward -- the Google button, Sign in, Sign up -- goes to
talent.wisemonk.io/login, where those things actually work. A marketing page
that collected an address and sent nothing would be worse than one that does
not ask.

The rules are scoped under .rec-auth. The header's own "Log in" anchor is
already called .rec-login, so the overlay could not take that name.
"""
import io
import sys

GOOGLE_SVG = (
    '<svg viewBox="0 0 48 48" aria-hidden="true">'
    '<path fill="#FFC107" d="M43.6 20.5h-1.9V20H24v8h11.3c-1.6 4.7-6.1 8-11.3 8-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.9 1.2 8 3.1l5.7-5.7C34.6 6.1 29.6 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/>'
    '<path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.9 1.2 8 3.1l5.7-5.7C34.6 6.1 29.6 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/>'
    '<path fill="#4CAF50" d="M24 44c5.5 0 10.5-2.1 14.3-5.5l-6.6-5.6C29.6 34.6 26.9 36 24 36c-5.2 0-9.6-3.3-11.3-7.9l-6.5 5C9.6 39.6 16.2 44 24 44z"/>'
    '<path fill="#1976D2" d="M43.6 20.5H24v8h11.3c-.8 2.3-2.2 4.2-4.1 5.6l6.6 5.6C41.4 36.9 44 31 44 24c0-1.3-.1-2.4-.4-3.5z"/>'
    '</svg>'
)

CSS = """
    /* ---- sign in ------------------------------------------------------------ */
    /* The product's own screen, lifted from Recruitment-frontend: Login.tsx for
       the markup, the .login-* block of Auth.css for these rules, and
       public/login-graphic.html in the same iframe on the right, so the two
       cannot drift apart. Scoped under .rec-auth -- the header's own link is
       already .rec-login and could not lend its name. */
    .rec-auth[hidden] { display:none; }
    .rec-auth { position:fixed; inset:0; z-index:300; background:var(--neutral-0);
                color:var(--text-primary); text-align:left;
                --border-strong:#DDE1E9;
                animation:rec-auth-in .22s ease both; }
    @keyframes rec-auth-in { from { opacity:0; } to { opacity:1; } }
    .rec-auth.is-out { animation:rec-auth-out .18s ease both; }
    @keyframes rec-auth-out { from { opacity:1; } to { opacity:0; } }
    .rec-auth .login-shell { width:100%; height:100%; display:grid;
                             grid-template-columns:minmax(0, 1fr) minmax(0, 1.05fr);
                             background:var(--neutral-0); overflow:hidden; }
    .rec-auth .login-left { position:relative; display:flex; flex-direction:column;
                            padding:28px 40px 24px; }
    .rec-auth .login-form-wrap { margin:auto; width:100%; max-width:340px; }
    .rec-auth .login-mira { height:46px; width:auto; display:block;
                            margin-bottom:20px; }
    .rec-auth .login-title { font-size:26px; font-weight:700;
                             letter-spacing:-0.4px; color:var(--text-primary);
                             margin:0 0 6px; }
    .rec-auth .login-sub { font-size:14px; color:var(--text-muted);
                           margin:0 0 26px; line-height:1.5; }
    .rec-auth .login-form { display:flex; flex-direction:column; gap:8px; }
    .rec-auth .login-input { position:relative; display:flex; align-items:center; }
    .rec-auth .login-input input {
      width:100%; box-sizing:border-box; padding:12px 14px;
      background:var(--neutral-0); border:1.5px solid var(--border-strong);
      border-radius:10px; font-family:inherit; font-size:16px; font-weight:500;
      color:var(--text-primary); outline:none;
      transition:padding .18s ease, border-color .15s, box-shadow .15s; }
    .rec-auth .login-input input:focus { border-color:var(--primary-500);
                                         box-shadow:0 0 0 4px var(--primary-50); }
    /* the label sits as a placeholder until the field has focus or a value,
       then shrinks and rises while the field grows to make room */
    .rec-auth .login-float label {
      position:absolute; left:15px; top:50%; transform:translateY(-50%);
      color:var(--neutral-400); font-size:14px; font-weight:200;
      pointer-events:none;
      transition:top .18s ease, transform .18s ease, font-size .18s ease,
                 color .18s ease, font-weight .18s ease; }
    .rec-auth .login-float input:focus,
    .rec-auth .login-float input:not(:placeholder-shown) { padding:27px 14px 7px; }
    .rec-auth .login-float input:focus + label,
    .rec-auth .login-float input:not(:placeholder-shown) + label {
      top:8px; transform:translateY(0); font-size:11px; font-weight:500;
      color:var(--primary-600); }
    .rec-auth .login-primary {
      margin-top:6px; width:100%; height:46px; border:none; border-radius:10px;
      display:inline-flex; align-items:center; justify-content:center; gap:8px;
      background:linear-gradient(120deg, #2440E6 0%, #5A4BD8 58%, #7C63DC 100%);
      color:#fff; font-family:inherit; font-size:15px; font-weight:600;
      cursor:pointer; transition:filter .15s; }
    .rec-auth .login-primary:hover { filter:brightness(0.94); }
    .rec-auth .login-primary-arrow { width:17px; height:17px; flex:none;
      opacity:0; transform:translateX(-6px);
      transition:opacity .18s, transform .18s; }
    .rec-auth .login-primary:hover .login-primary-arrow { opacity:1;
                                                          transform:translateX(0); }
    .rec-auth .login-divider { display:flex; align-items:center; gap:12px;
                               margin:20px 0; font-size:12.5px; font-weight:500;
                               color:var(--text-muted); }
    .rec-auth .login-divider::before,
    .rec-auth .login-divider::after { content:""; flex:1; height:1px;
                                      background:var(--border); }
    .rec-auth .login-google-btn {
      width:100%; box-sizing:border-box; height:46px; display:inline-flex;
      align-items:center; justify-content:center; gap:10px; text-decoration:none;
      border:1.5px solid var(--border-strong); border-radius:10px;
      background:var(--neutral-0); font-family:inherit; font-size:15px;
      font-weight:600; color:var(--text-primary); cursor:pointer;
      transition:background .15s, border-color .15s; }
    .rec-auth .login-google-btn:hover { background:var(--neutral-50);
                                        border-color:var(--neutral-400); }
    .rec-auth .login-google-btn svg { width:18px; height:18px; }
    .rec-auth .login-switch { margin:16px 0 0; font-size:13.5px;
                              color:var(--text-muted); }
    .rec-auth .login-switch-link { font-weight:700; color:var(--primary-600);
                                   text-decoration:none; }
    .rec-auth .login-switch-link:hover { text-decoration:underline; }
    .rec-auth .login-foot { margin-top:24px; text-align:center; font-size:12px;
                            color:var(--text-muted); }
    .rec-auth .login-legal { margin:0; line-height:1.5; }
    .rec-auth .login-legal a { color:var(--text-primary); font-weight:600;
                               text-decoration:none; }
    .rec-auth .login-legal a:hover { text-decoration:underline; }
    .rec-auth .login-right { position:relative; overflow:hidden; display:block;
                             margin:14px 14px 14px 0; border-radius:22px;
                             background:linear-gradient(142deg, #F6F9FF 0%,
                               #FAF8FE 52%, #F8F5FD 100%); }
    .rec-auth .lr-frame { display:block; width:100%; height:100%; border:0; }
    /* a route needs no way out; an overlay does */
    .rec-auth-x { position:absolute; top:22px; right:26px; width:36px;
                  height:36px; border-radius:50%; border:0; display:grid;
                  place-items:center; cursor:pointer; background:#F2EFFB;
                  color:#4E4470; font-size:19px; line-height:1;
                  font-family:inherit; transition:background .15s; }
    .rec-auth-x:hover { background:#E6E0F7; }
    /* below tablet the panel goes and the form takes the width */
    @media (max-width:920px) {
      .rec-auth .login-shell { grid-template-columns:1fr; }
      .rec-auth .login-right { display:none; }
      .rec-auth .login-left { padding:24px 22px 20px; }
    }
    @media (prefers-reduced-motion: reduce) {
      .rec-auth, .rec-auth.is-out { animation:none; }
      .rec-auth .login-primary-arrow { transition:none; }
    }
"""

JS = r"""
  // Log in opens the product's own sign-in screen, lifted from
  // Recruitment-frontend. What this page cannot honour -- the magic link, the
  // Google credential, the "check your inbox" screen -- is dropped, and every
  // way forward goes to the real one. Collecting an address here and sending
  // nothing would be worse than not asking.
  (function () {
    var opener = document.querySelector('.rec-head .rec-login');
    if (!opener) return;
    var APP = 'https://talent.wisemonk.io/login';
    var panel = null;

    function build() {
      panel = document.createElement('div');
      panel.className = 'rec-auth';
      panel.hidden = true;
      panel.setAttribute('role', 'dialog');
      panel.setAttribute('aria-modal', 'true');
      panel.setAttribute('aria-label', 'Sign in');
      panel.innerHTML =
        '<div class="login-shell">' +
          '<div class="login-left">' +
            '<button type="button" class="rec-auth-x" aria-label="Close">&#215;</button>' +
            '<div class="login-form-wrap">' +
              '<img class="login-mira" src="mira-mark.svg" alt="Mira" ' +
                'width="412" height="300">' +
              '<h1 class="login-title">Welcome to Wisemonk</h1>' +
              '<p class="login-sub">Sign in or create your account to hire ' +
                'with Mira AI.</p>' +
              '<a class="login-google-btn" href="' + APP + '">' + '@GOOGLE@' +
                'Continue with Google</a>' +
              '<div class="login-divider">or</div>' +
              '<form class="login-form">' +
                '<div class="login-input login-float">' +
                  '<input id="rec-auth-email" type="email" autocomplete="email" ' +
                    'placeholder=" ">' +
                  '<label for="rec-auth-email">Enter your email address</label>' +
                '</div>' +
                '<button type="submit" class="login-primary"><span>Sign in</span>' +
                  '<svg class="login-primary-arrow" viewBox="0 0 24 24" fill="none" ' +
                    'stroke="currentColor" stroke-width="2" stroke-linecap="round" ' +
                    'stroke-linejoin="round" aria-hidden="true">' +
                    '<line x1="5" y1="12" x2="19" y2="12"/>' +
                    '<polyline points="12 5 19 12 12 19"/></svg></button>' +
              '</form>' +
              '<p class="login-switch">Don\'t have an account? ' +
                '<a class="login-switch-link" href="' + APP + '">Sign up</a></p>' +
            '</div>' +
            '<div class="login-foot"><p class="login-legal">By continuing, you ' +
              'agree to our <a href="https://www.wisemonk.io/terms" ' +
              'target="_blank" rel="noreferrer">Terms &amp; Conditions</a> and ' +
              '<a href="https://www.wisemonk.io/privacy" target="_blank" ' +
              'rel="noreferrer">Privacy Policy</a>.</p></div>' +
          '</div>' +
          '<aside class="login-right" aria-hidden="true">' +
            '<iframe class="lr-frame" src="login-graphic.html" title="" ' +
              'tabindex="-1" loading="lazy"></iframe>' +
          '</aside>' +
        '</div>';
      document.body.appendChild(panel);

      panel.querySelector('.rec-auth-x').addEventListener('click', close);
      panel.querySelector('.login-form').addEventListener('submit', function (e) {
        e.preventDefault();
        window.location.href = APP;
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && panel && !panel.hidden) close();
      });
      // the page behind is scroll-driven and should stay where it was
      panel.addEventListener('wheel', function (e) { e.preventDefault(); },
                             { passive: false });
    }

    function close() {
      panel.classList.add('is-out');
      window.setTimeout(function () {
        panel.hidden = true;
        panel.classList.remove('is-out');
      }, 180);
      opener.focus();
    }

    opener.addEventListener('click', function (e) {
      e.preventDefault();
      if (!panel) build();
      panel.classList.remove('is-out');
      panel.hidden = false;
      panel.querySelector('#rec-auth-email').focus();
    });
  }());
""".replace('@GOOGLE@', "'" + GOOGLE_SVG.replace("'", "\\'") + "' + ")

CSS_MARK = "    /* ---- suggestions ------"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-auth' not in s, path + ': already has the sign-in screen'

    assert s.count(CSS_MARK) == 1, path + ': suggestions marker changed'
    s = s.replace(CSS_MARK, CSS.lstrip('\n') + '\n' + CSS_MARK, 1)

    i = s.rindex('</script>')
    s = s[:i] + JS + s[i:]

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
