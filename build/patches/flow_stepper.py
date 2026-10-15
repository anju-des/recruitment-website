# -*- coding: utf-8 -*-
"""Three steps across the top: company details, job board, account.

It sits in the header slot the old "Step 1 of 4" counter had, which is
the right place for it and the wrong place for a counter.

Only the first step does anything. It lights when the flow opens and
ticks when the details land; the other two stay ahead of the reader,
dimmed, because nothing here builds a job board or prepares an account
yet. They read as what is coming rather than as work being done -- a
step that marked itself complete for work nobody did would be the one
thing on this screen that is not true.

Labels drop below 600px and the numbers carry it alone.
"""
import io
import sys

OLD_HEAD = """        '<div class="rec-flow-head">' +
          '<img src="mira-logo.svg" width="1152" height="365" alt="Mira">' +
          '<button type="button" class="rec-flow-x" aria-label="Close">&#215;</button>' +
        '</div>' +"""

NEW_HEAD = """        '<div class="rec-flow-head">' +
          '<img src="mira-logo.svg" width="1152" height="365" alt="Mira">' +
          '<ol class="rec-steps">' +
            ['Company details', 'Job board', 'Account']
              .map(function (s, i) {
                return '<li class="rec-step"><i>' + (i + 1) + '</i>' +
                  '<b>' + s + '</b></li>';
              }).join('') +
          '</ol>' +
          '<button type="button" class="rec-flow-x" aria-label="Close">&#215;</button>' +
        '</div>' +"""

# the setter, and the two places that call it
OLD_OPEN = """    function open() {
      brief.role = field.value.trim();"""
NEW_OPEN = """    // only the first of the three does anything yet; the others are what
    // is coming, not work being claimed
    function at_step(i, done) {
      var all = flow.querySelectorAll('.rec-step');
      for (var k = 0; k < all.length; k++) {
        all[k].classList.toggle('is-on', k === i && !done);
        all[k].classList.toggle('is-done', k < i || (k === i && done));
      }
    }

    function open() {
      brief.role = field.value.trim();"""

OLD_DRAW = """      if (at >= STEPS.length) { close(); return; }
      card.innerHTML = ask(STEPS[at]);"""
NEW_DRAW = """      if (at >= STEPS.length) { close(); return; }
      at_step(0, false);
      card.innerHTML = ask(STEPS[at]);"""

OLD_REST = """        function rest() {
          busy = '';
          finished = true;"""
NEW_REST = """        function rest() {
          busy = '';
          finished = true;
          at_step(0, true);"""

CSS = """    /* the three steps, in the header */
    .rec-steps { display:flex; align-items:center; gap:10px; margin:0;
                 padding:0; list-style:none; }
    .rec-step { display:flex; align-items:center; gap:7px; color:#A49CC0;
                font-size:12.5px; }
    .rec-step + .rec-step::before { content:""; width:22px; height:1px;
                                    background:#E2DCF4; margin-right:3px; }
    .rec-step i { font-style:normal; display:grid; place-items:center;
                  width:20px; height:20px; flex:none; border-radius:50%;
                  background:#F1EEFA; color:#9A93B8; font-size:11px;
                  font-weight:700; }
    .rec-step b { font-weight:500; }
    .rec-step.is-on { color:#1A1430; }
    .rec-step.is-on i { background:#7C5CF6; color:#FFFFFF; }
    .rec-step.is-on b { font-weight:600; }
    .rec-step.is-done { color:#6B6392; }
    .rec-step.is-done i { background:#EDE8FD; color:#5A4BD8; }
    @media (max-width:760px) {
      .rec-step b { display:none; }
      .rec-steps { gap:6px; }
      .rec-step + .rec-step::before { width:14px; }
    }
"""

CSS_ANCHOR = "    .rec-flow-x { width:36px;"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-steps' not in s, path + ': already has the stepper'
    for old, new in ((OLD_HEAD, NEW_HEAD), (OLD_OPEN, NEW_OPEN),
                     (OLD_DRAW, NEW_DRAW), (OLD_REST, NEW_REST)):
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS + CSS_ANCHOR, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
