# -*- coding: utf-8 -*-
"""One step, appearing when there is something to report.

Three changes that are one idea: the rail is a record of work, not a
promise of screens.

* Job board and Account go. They were two dimmed rows holding the left
  of the screen for pages that do not exist.
* The rail is not drawn on the question screen at all. It appears when
  the lookup starts -- which is also what keeps the spinner on step one
  worth having -- and stays once the step is done.
* The details play out full size in the middle, then fold into a small
  card under the step: logo and company name, nothing else. A finished
  step does not need to keep its working out on screen, and the body is
  left clear for whatever comes next.

The refresh record changes shape with it. It kept the rendered details
card; it now keeps the three things the chip needs, because the screen
that HTML described is no longer the screen a restore should land on.
"""
import io
import sys

EDITS = [
    ("""          ['Company details', 'Job board', 'Account']""",
     """          ['Company details']"""),

    # one renderer, used by the settle and by the restore
    ("""    // the step is working, not merely current
    function step_busy(i) {
      at_step(i, false);""",
     """    // what a finished lookup leaves behind in the rail
    function put_mini(who, logo) {
      var rail = flow.querySelector('.rec-steps');
      var mini = rail.querySelector('.rec-done-card');
      if (!mini) {
        mini = document.createElement('li');
        mini.className = 'rec-done-card';
        rail.appendChild(mini);
      }
      mini.innerHTML =
        '<span class="rec-done-mark">' +
          (logo ? '<img src="' + esc(logo) + '" alt="">'
                : esc(String(who || '?').charAt(0))) +
        '</span><b>' + esc(who) + '</b>';
    }

    // the step is working, not merely current. The rail is only drawn
    // from here on: before this there is nothing to report.
    function step_busy(i) {
      flow.classList.add('is-working');
      at_step(i, false);"""),

    # the question screen has no rail
    ("""      if (at >= STEPS.length) { close(); return; }
      flow.classList.remove('is-found');""",
     """      if (at >= STEPS.length) { close(); return; }
      flow.classList.remove('is-found');
      flow.classList.remove('is-working');"""),

    # keep what the chip needs, not what the panel showed
    ("""              window.sessionStorage.setItem('wm-flow', JSON.stringify({
                role: brief.role, website: brief.website,
                html: card.innerHTML
              }));""",
     """              window.sessionStorage.setItem('wm-flow', JSON.stringify({
                role: brief.role, website: brief.website,
                who: who, logo: logo
              }));"""),

    # settling folds the panel away into the rail
    ("""          window.setTimeout(function () {
            if (flow && !flow.hidden) flow.classList.add('is-found');
          }, 1600);""",
     """          window.setTimeout(function () {
            if (!flow || flow.hidden) return;
            flow.classList.add('is-found');
            put_mini(who, logo);
            card.innerHTML = '';
          }, 1600);"""),

    # and a restore lands on that same settled screen
    ("""      at_step(0, true);
      flow.classList.add('is-found');
      flow.querySelector('.rec-flow-bar span')
          .style.setProperty('--at', '100%');
      var card = flow.querySelector('.rec-flow-card');
      card.innerHTML = was.html;
      // the only control the found screen can carry
      var again = card.querySelector('.rec-flow-back');
      if (again) again.addEventListener('click', function () { draw(); });""",
     """      at_step(0, true);
      flow.classList.add('is-found');
      flow.querySelector('.rec-flow-bar span')
          .style.setProperty('--at', '100%');
      flow.querySelector('.rec-flow-card').innerHTML = '';
      put_mini(was.who, was.logo);"""),

    ("""      if (!was || !was.html) return;""",
     """      if (!was || !was.who) return;"""),

    # the rail starts hidden and is shown by state
    ("""    .rec-steps { flex:none; display:flex; flex-direction:column;""",
     """    .rec-steps { flex:none; display:none; flex-direction:column;"""),
]

CSS = """    /* the rail is a record of work: nothing to show until there is */
    .rec-flow.is-working .rec-steps,
    .rec-flow.is-found .rec-steps { display:flex; }

    /* what the finished step keeps: the company, and nothing else */
    .rec-done-card { display:flex; align-items:center; gap:9px;
                     margin:2px 0 0 30px; padding:9px 12px; max-width:100%;
                     box-sizing:border-box; border-radius:12px;
                     border:1px solid #ECE7F9; background:#FFFFFF;
                     box-shadow:0 1px 8px rgba(18,22,32,.05);
                     animation:rec-mini-in .32s ease both; }
    @keyframes rec-mini-in { from { opacity:0; transform:translateY(-4px); }
                             to { opacity:1; transform:none; } }
    .rec-done-mark { flex:none; width:22px; height:22px; border-radius:7px;
                     overflow:hidden; display:grid; place-items:center;
                     background:linear-gradient(135deg,#8B5CF6,#2684FF);
                     color:#FFFFFF; font-size:11px; font-weight:700; }
    .rec-done-mark img { width:100%; height:100%; object-fit:cover;
                         display:block; }
    .rec-done-card b { min-width:0; font-size:13px; font-weight:600;
                       color:#1A1430; white-space:nowrap; overflow:hidden;
                       text-overflow:ellipsis; }
    @media (prefers-reduced-motion: reduce) {
      .rec-done-card { animation:none; }
    }
"""

CSS_ANCHOR = "    .rec-step i { font-style:normal;"

OLD_MQ = """      .rec-steps { width:100%; flex-direction:row; align-items:center;
                   padding:12px 18px; }"""
NEW_MQ = """      .rec-steps { width:100%; flex-direction:row; align-items:center;
                   flex-wrap:wrap; padding:12px 18px; }
      .rec-done-card { margin:0 0 0 10px; }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-done-card' not in s, path + ': already folds away'
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS + CSS_ANCHOR, 1)
    assert s.count(OLD_MQ) == 1, (path, 'mq', s.count(OLD_MQ))
    s = s.replace(OLD_MQ, NEW_MQ, 1)
    js = s[s.rindex('<script>'):]
    assert 'Job board' not in js, path + ': a hidden step survives'
    assert 'was.html' not in js, path + ': the old restore survives'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
