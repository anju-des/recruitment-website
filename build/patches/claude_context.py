# -*- coding: utf-8 -*-
"""Connect your Claude -- a row under the composer, and what it opens.

Not a connector, not MCP, and the copy names no mechanism: the panel says
what the connection is for and what changes because of it, and leaves how
it is wired to whoever wires it.

The one claim it does make is the permission line. A page that invites
someone to connect their company's Claude has to say who decides what gets
read, and that line is cheap to keep true whatever the implementation turns
out to be.

Its CTA opens the sign-in screen, because connecting is account-shaped --
the same dead end the rest of this walkthrough has, rather than a new one.
"""
import io
import sys

SPARK = ('<svg class="rec-cx-mark" viewBox="0 0 24 24" fill="currentColor" '
         'aria-hidden="true"><path d="M12 3c.6 4.2 1.8 5.4 6 6-4.2.6-5.4 1.8-6 '
         '6-.6-4.2-1.8-5.4-6-6 4.2-.6 5.4-1.8 6-6z"/></svg>')

ROW = """              <div class="rec-cx-row">
                <button type="button" class="rec-cx">
                  @SPARK@
                  <span class="rec-cx-say"><b>Connect your Claude</b>
                    <i>so the brief knows how you hire</i></span>
                  <svg class="rec-cx-go" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2.2" stroke-linecap="round"
                    stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>
                </button>
              </div>
""".replace('@SPARK@', SPARK)

ANCHOR = """              </form>
              </div>
              <ul class="rec-suggest" aria-label="Example roles" hidden>
"""

CSS = """
    /* ---- connect your Claude -------------------------------------------- */
    .rec-cx-row { width:100%; text-align:center; margin-top:16px; }
    .rec-cx { display:inline-flex; align-items:center; gap:10px;
              max-width:100%; padding:9px 14px 9px 13px; cursor:pointer;
              border:1px solid rgba(124,92,246,.22); border-radius:100px;
              background:rgba(124,92,246,.05); font:inherit; text-align:left;
              transition:background .15s, border-color .15s, transform .15s; }
    .rec-cx:hover { background:rgba(124,92,246,.1);
                    border-color:rgba(124,92,246,.4);
                    transform:translateY(-1px); }
    .rec-cx:focus-visible { outline:2px solid #7C5CF6; outline-offset:3px; }
    .rec-cx-mark { width:17px; height:17px; flex:none; color:#7C5CF6; }
    .rec-cx-say { min-width:0; }
    .rec-cx b { font-size:14px; font-weight:600; color:var(--text-primary); }
    .rec-cx i { font-style:normal; font-size:14px; color:var(--text-muted); }
    .rec-cx i::before { content:"\\00b7"; margin:0 8px; color:#C6BFE0; }
    .rec-cx-go { width:15px; height:15px; flex:none; color:var(--text-muted); }

    .rec-cxp[hidden] { display:none; }
    .rec-cxp { position:fixed; inset:0; z-index:270; display:grid;
               place-items:center; padding:20px;
               background:rgba(18,12,40,.44);
               -webkit-backdrop-filter:blur(3px); backdrop-filter:blur(3px);
               animation:rec-cxp-in .18s ease both; }
    @keyframes rec-cxp-in { from { opacity:0; } to { opacity:1; } }
    .rec-cxp.is-out { animation:rec-cxp-out .16s ease both; }
    @keyframes rec-cxp-out { from { opacity:1; } to { opacity:0; } }
    .rec-cxp-card { width:min(520px, 100%); max-height:calc(100vh - 40px);
                    overflow-y:auto; box-sizing:border-box;
                    padding:clamp(24px, 3.4vw, 34px); border-radius:20px;
                    background:#FFFFFF; color:#2C2545; text-align:left;
                    box-shadow:0 30px 70px rgba(20,12,48,.3); }
    .rec-cxp-top { display:flex; align-items:center; gap:10px;
                   margin-bottom:16px; }
    .rec-cxp-top .rec-cx-mark { width:20px; height:20px; }
    .rec-cxp-x { margin-left:auto; width:32px; height:32px; flex:none;
                 border:0; border-radius:50%; background:none; cursor:pointer;
                 display:grid; place-items:center; color:#8A82A8;
                 font-size:21px; line-height:1; transition:background .15s; }
    .rec-cxp-x:hover { background:#F4F1FD; color:#4B4270; }
    .rec-cxp h2 { margin:0 0 10px; font-size:clamp(20px, 1vw + 17px, 25px);
                  font-weight:700; letter-spacing:-0.015em; color:#1A1430; }
    .rec-cxp p { margin:0 0 13px; font-size:14.5px; line-height:1.6;
                 color:#4B4270; }
    .rec-cxp-gains { margin:18px 0 0; padding:0; list-style:none; }
    .rec-cxp-gains li { position:relative; padding:0 0 15px 26px;
                        font-size:14.5px; line-height:1.55; color:#4B4270; }
    .rec-cxp-gains li::before { content:""; position:absolute; left:4px;
                                top:8px; width:7px; height:7px;
                                border-radius:50%; background:#B9A8F5; }
    .rec-cxp-gains b { font-weight:600; color:#1A1430; }
    .rec-cxp-do { width:100%; height:46px; margin-top:6px; cursor:pointer;
                  border:0; border-radius:12px; font:inherit; font-size:15px;
                  font-weight:600; color:#FFFFFF;
                  background:linear-gradient(135deg, #6B4BE8, #8B5CF6);
                  transition:filter .15s; }
    .rec-cxp-do:hover { filter:brightness(0.94); }
    .rec-cxp-note { margin:14px 0 0; font-size:13px; line-height:1.55;
                    color:#8A82A8; text-align:center; }
    @media (prefers-reduced-motion: reduce) {
      .rec-cx { transition:none; }
      .rec-cx:hover { transform:none; }
      .rec-cxp, .rec-cxp.is-out { animation:none; }
    }
"""

CSS_ANCHOR = "    /* ---- Mira in the corner ---"

JS = r"""
  // What the row under the composer opens. It describes what the connection
  // is for, not how it is built -- there is nothing behind it yet, and a
  // page that names a mechanism is a page that has to be right about one.
  (function () {
    var opener = document.querySelector('.rec-cx');
    if (!opener) return;
    var panel = null;

    function close() {
      panel.classList.add('is-out');
      window.setTimeout(function () {
        panel.hidden = true;
        panel.classList.remove('is-out');
        opener.focus();
      }, 160);
    }

    function build() {
      panel = document.createElement('div');
      panel.className = 'rec-cxp';
      panel.hidden = true;
      panel.setAttribute('role', 'dialog');
      panel.setAttribute('aria-modal', 'true');
      panel.setAttribute('aria-label', 'Connect your Claude');
      panel.innerHTML =
        '<div class="rec-cxp-card">' +
          '<div class="rec-cxp-top">' +
            '<svg class="rec-cx-mark" viewBox="0 0 24 24" fill="currentColor" ' +
              'aria-hidden="true"><path d="M12 3c.6 4.2 1.8 5.4 6 6-4.2.6-5.4 ' +
              '1.8-6 6-.6-4.2-1.8-5.4-6-6 4.2-.6 5.4-1.8 6-6z"/></svg>' +
            '<button type="button" class="rec-cxp-x" aria-label="Close">' +
              '×</button>' +
          '</div>' +
          '<h2>Connect your Claude</h2>' +
          '<p>Your team already works out the hard parts of a role in Claude ' +
            '— the scorecard, the levels, what the last search got wrong. ' +
            'Connect it and Mira hires against that, instead of against a job ' +
            'title.</p>' +
          '<p>You choose what Mira can see, and you can disconnect it at any ' +
            'time.</p>' +
          '<ul class="rec-cxp-gains">' +
            '<li><b>Briefs in your words.</b> The role goes out at your levels ' +
              'and your bar, not a template’s.</li>' +
            '<li><b>Fewer questions back.</b> Mira stops asking what it could ' +
              'have read — the stack, the team shape, who the hire reports ' +
              'to.</li>' +
            '<li><b>A shortlist that fits.</b> Every application is ranked ' +
              'against your context, not a title match.</li>' +
          '</ul>' +
          '<button type="button" class="rec-cxp-do">Connect your Claude</button>' +
          '<p class="rec-cxp-note">Connecting is tied to your workspace, so ' +
            'your account comes first.</p>' +
        '</div>';
      document.body.appendChild(panel);

      panel.querySelector('.rec-cxp-x').addEventListener('click', close);
      panel.querySelector('.rec-cxp-do').addEventListener('click', function () {
        close();
        // connecting is account-shaped, so it starts where accounts start
        var login = document.querySelector('.rec-head .rec-login');
        if (login) window.setTimeout(function () { login.click(); }, 180);
      });
      panel.addEventListener('click', function (e) {
        if (e.target === panel) close();      // the ground behind the card
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && panel && !panel.hidden) close();
      });
      // the page behind is scroll-driven and should stay where it was
      panel.addEventListener('wheel', function (e) { e.preventDefault(); },
                             { passive: false });
    }

    opener.addEventListener('click', function () {
      if (!panel) build();
      panel.classList.remove('is-out');
      panel.hidden = false;
      panel.querySelector('.rec-cxp-x').focus();
    });
  }());
"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-cx' not in s, path + ': already has the row'

    assert s.count(ANCHOR) == 1, (path, 'composer anchor', s.count(ANCHOR))
    s = s.replace(ANCHOR, ANCHOR.replace(
        '              <ul class="rec-suggest"',
        ROW + '              <ul class="rec-suggest"'), 1)

    assert s.count(CSS_ANCHOR) == 1, (path, 'css anchor', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS.lstrip('\n') + '\n' + CSS_ANCHOR, 1)

    i = s.rindex('</script>')
    s = s[:i] + JS + s[i:]

    for word in ('MCP', 'connector', 'API key'):
        assert word not in s[s.index('rec-cx-row'):], path + ': ' + word
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
