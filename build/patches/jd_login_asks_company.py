# -*- coding: utf-8 -*-
"""Log in asks which company first, when it does not already know.

Pressing it used to go straight to an email field. It opens the company
question now -- the same screen the no-JD path uses -- so the page
knows who is signing in before it asks how, and the lookup, the career
site and the role all happen on the way to the account.

When the company is already known, because this session has run the
flow, there is nothing to ask and it goes straight to the sign-in.
Asking twice for something already on screen is how a flow starts
feeling like paperwork.

The sign-in panel needed a way to be opened that is not "click the Log
in link", since that link now leads back into the flow -- the account
screen's own button would have gone round in a circle. The auth panel
hands out recAuthOpen for exactly that, and the flow hands back
recAskCompany, which answers whether it took the click.
"""
import io
import sys

# --- the auth panel: one way in that is not the link ------------------

AUTH_EDITS = [
    ("""    opener.addEventListener('click', function (e) {
      e.preventDefault();
      if (!panel) build();
      panel.classList.remove('is-out');
      panel.hidden = false;
      panel.querySelector('#rec-auth-email').focus();
      try {
        window.history.pushState({ recAuth: 1 }, '', '#login');
      } catch (err) {}
    });""",

     """    // opened by the account screen at the end of the flow, which cannot
    // click the link any more: that leads back into the flow
    function show_panel() {
      if (!panel) build();
      panel.classList.remove('is-out');
      panel.hidden = false;
      panel.querySelector('#rec-auth-email').focus();
      try {
        window.history.pushState({ recAuth: 1 }, '', '#login');
      } catch (err) {}
    }
    window.recAuthOpen = show_panel;

    opener.addEventListener('click', function (e) {
      e.preventDefault();
      // the flow asks which company first, unless it already knows
      if (window.recAskCompany && window.recAskCompany()) return;
      show_panel();
    });"""),
]

# --- the flow: it answers for that click ------------------------------

FLOW_EDITS = [
    ("""    // the account screen's one action, defined where a reopen can find it
    function open_account() {
      close();
      var login = document.querySelector('.rec-head .rec-login');
      if (login) window.setTimeout(function () { login.click(); }, 200);
    }""",

     """    // the account screen's one action, defined where a reopen can find it
    function open_account() {
      close();
      window.setTimeout(function () {
        if (window.recAuthOpen) window.recAuthOpen();
      }, 200);
    }

    // Log in asks this first: true means the flow took the click, which
    // it does whenever the company is still unknown
    window.recAskCompany = function () {
      if (company && company.who) return false;
      if (flow && !flow.hidden) return false;
      open();
      return true;
    };"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'recAskCompany' not in s, path + ': already asks'

    for old, new in FLOW_EDITS + AUTH_EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    assert "login.click()" not in s, path + ': something still clicks the link'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
