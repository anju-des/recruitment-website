# -*- coding: utf-8 -*-
"""Website in, profile out.

The step now does what it promises: the domain is looked up, and what
comes back is shown for confirmation before the brief moves on.

What is really fetched is the logo, live, from the domain -- that part is
not staged. The company name is derived from the domain, which is right
far more often than not. Everything else a profile would carry (what the
company does, how big it is) needs a server that can read the site, so
the screen does not claim to have it.

The looking-up beat waits for the image to settle but never shows for
less than 600ms or more than 4s: under that it reads as a flicker, over
it reads as broken.

"I don't have a website" skips the step rather than blocking on it. Some
companies genuinely do not have one, and a brief is still worth taking.
"""
import io
import sys

EDITS = [
    # the question, reworded around what the step now does
    ("""      { key: 'website',
        q: 'What is your company website?',
        placeholder: 'yourcompany.com',""",
     """      { key: 'website',
        q: 'Let\\'s start with your company',
        hint: 'Enter your website and Mira looks it up.',
        skip: 'I don\\'t have a website',
        placeholder: 'yourcompany.com',"""),

    # the skip, under the buttons. Anchored past the tags block, because
    # three screens build a rec-flow-act row and only ask() takes a skip.
    ("""        }).join('') + '</div>' : '') +
        '<div class="rec-flow-act">' +""",
     """        }).join('') + '</div>' : '') +
        (step.skip ? '<button type="button" class="rec-flow-skip">' +
          esc(step.skip) + '</button>' : '') +
        '<div class="rec-flow-act">' +"""),
]

LOOK_JS = """
      // What the website step does instead of going straight on: look the
      // domain up, show what came back, and let them correct it.
      function look() {
        var site = brief.website;
        card.innerHTML =
          '<h2 class="rec-flow-q is-alone">Looking up ' + esc(site) +
            '</h2>' +
          '<div class="rec-flow-spin" aria-label="Looking up" role="status">' +
            '<span></span></div>';

        var began = Date.now();
        var done_once = false;
        var logo = '';

        function settled() {
          if (done_once) return;
          done_once = true;
          // never a flicker, never a hang
          var wait = Math.max(0, 600 - (Date.now() - began));
          window.setTimeout(function () { found(site, logo); }, wait);
        }

        var img = new Image();
        img.addEventListener('load', function () {
          // a 404 from this service still decodes: it answers with a 16px
          // globe, where a real logo at sz=128 comes back 128 wide
          if (img.naturalWidth >= 64) logo = img.src;
          settled();
        });
        img.addEventListener('error', settled);
        img.src = 'https://www.google.com/s2/favicons?domain=' +
                  encodeURIComponent(site) + '&sz=128';
        window.setTimeout(settled, 4000);
      }

      function named(domain) {
        var core = String(domain).split('.')[0].replace(/[-_]+/g, ' ');
        return core.charAt(0).toUpperCase() + core.slice(1);
      }

      function found(site, logo) {
        var who = named(site);
        card.innerHTML =
          '<h2 class="rec-flow-q is-alone">Is this you?</h2>' +
          '<div class="rec-flow-found">' +
            '<span class="rec-flow-found-mark">' +
              (logo ? '<img src="' + esc(logo) + '" alt="">'
                    : esc(who.charAt(0))) +
            '</span>' +
            '<span class="rec-flow-found-say"><b>' + esc(who) + '</b>' +
              '<i>' + esc(site) + '</i></span>' +
          '</div>' +
          '<div class="rec-flow-act">' +
            '<button type="button" class="rec-flow-back">Change</button>' +
            '<button type="button" class="rec-flow-next">Yes, continue' +
              '</button>' +
          '</div>';
        card.querySelector('.rec-flow-next')
            .addEventListener('click', onward);
        card.querySelector('.rec-flow-back')
            .addEventListener('click', function () { draw(); });
      }
"""

CSS = """
    /* the website step: skip, lookup, and what came back */
    .rec-flow-skip { display:block; margin:18px auto 0; border:0; padding:2px;
                     background:none; font:inherit; font-size:13.5px;
                     color:#8A82A8; cursor:pointer;
                     text-decoration:underline; text-underline-offset:3px; }
    .rec-flow-skip:hover { color:#4B4270; }
    .rec-flow-spin { display:grid; place-items:center; margin-top:26px; }
    .rec-flow-spin span { width:26px; height:26px; border-radius:50%;
                          border:2.5px solid #E7E2F6; border-top-color:#7C5CF6;
                          animation:rec-flow-turn .8s linear infinite; }
    @keyframes rec-flow-turn { to { transform:rotate(360deg); } }
    .rec-flow-found { display:inline-flex; align-items:center; gap:13px;
                      margin-top:24px; padding:14px 20px 14px 14px;
                      border:1px solid #E7E2F6; border-radius:16px;
                      background:#FFFFFF; text-align:left; }
    .rec-flow-found-mark { flex:none; width:44px; height:44px;
                           border-radius:12px; overflow:hidden; display:grid;
                           place-items:center; color:#FFFFFF; font-size:19px;
                           font-weight:700;
                           background:linear-gradient(135deg,#8B5CF6,#2684FF); }
    .rec-flow-found-mark img { width:100%; height:100%; object-fit:cover;
                               display:block; }
    .rec-flow-found-say { display:flex; flex-direction:column; gap:2px; }
    .rec-flow-found-say b { font-size:15.5px; font-weight:700;
                            color:#1A1430; }
    .rec-flow-found-say i { font-style:normal; font-size:13px;
                            color:#8A82A8; }
    @media (prefers-reduced-motion: reduce) {
      .rec-flow-spin span { animation-duration:2.4s; }
    }
"""

CSS_ANCHOR = "    /* ---- Mira in the corner ---"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-flow-found' not in s, path + ': already looks up'

    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    # look()/found() go inside wire(), where onward and draw are in scope
    mark = "      function onward() { at++; draw(); }\n"
    assert s.count(mark) == 1, (path, 'onward', s.count(mark))
    s = s.replace(mark, mark + LOOK_JS, 1)

    # the website step confirms before it advances
    go_old = """        if (at > STEPS.length) { done(); return; }
        onward();"""
    go_new = """        if (at > STEPS.length) { done(); return; }
        if (step.key === 'website' && brief.website) { look(); return; }
        onward();"""
    assert s.count(go_old) == 1, (path, 'go', s.count(go_old))
    s = s.replace(go_old, go_new, 1)

    # and the skip has to do something
    skip_mark = """      var chips = card.querySelectorAll('.rec-flow-chip');"""
    skip_new = """      var skip = card.querySelector('.rec-flow-skip');
      if (skip) skip.addEventListener('click', function () {
        brief.website = '';
        onward();
      });

      var chips = card.querySelectorAll('.rec-flow-chip');"""
    assert s.count(skip_mark) == 1, (path, 'skip', s.count(skip_mark))
    s = s.replace(skip_mark, skip_new, 1)

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS.lstrip('\n') + '\n' + CSS_ANCHOR, 1)

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
