# -*- coding: utf-8 -*-
"""Skills become a stack of chips you pick from, several at a time.

The typed-and-Entered tag is gone with the field it lived in. A chip here
toggles rather than answering, so this step keeps its Continue: picking one
is not the same as being finished picking.

Focus is put back on the chip that was just toggled after the redraw.
Without that, every pick would throw a keyboard user back to the first chip
in the stack.
"""
import io
import sys

SKILLS = [
    'Python', 'Django', 'Go', 'Node.js', 'TypeScript', 'React',
    'PostgreSQL', 'AWS', 'Kubernetes', 'System design',
    'Figma', 'Design systems', 'User research', 'Product strategy',
    'SQL', 'Machine learning',
]

EDITS = [
    ("""      { key: 'skills',
        q: 'What must they be good at?',
        hint: 'Add a few. Every application is scored against these as it arrives.',
        placeholder: 'Type a skill and press Enter',
        tags: true }""",
     """      { key: 'skills',
        q: 'What must they be good at?',
        hint: 'Pick as many as apply. Every application is scored against them.',
        chipsOnly: true,
        multi: true,
        chips: [%s] }""" % ', '.join("'" + s + "'" for s in SKILLS)),

    # a chip in a multi step shows whether it is among the chosen
    ("""        (step.chips ? '<div class="rec-flow-chips">' + step.chips.map(function (c) {
          return '<button type="button" class="rec-flow-chip' +
            (brief[step.key] === c ? ' is-on' : '') + '">' + esc(c) + '</button>';
        }).join('') + '</div>' : '') +""",
     """        (step.chips ? '<div class="rec-flow-chips">' + step.chips.map(function (c) {
          var picked = step.multi ? brief.skills.indexOf(c) > -1
                                  : brief[step.key] === c;
          return '<button type="button" class="rec-flow-chip' +
            (picked ? ' is-on' : '') + '">' + esc(c) + '</button>';
        }).join('') + '</div>' : '') +"""),

    ("""        var has = step.range ? true
                : step.tags ? brief.skills.length > 0""",
     """        var has = step.range ? true
                : (step.multi || step.tags) ? brief.skills.length > 0"""),

    ("""        if (at < STEPS.length) {
          if (step.range) brief[step.key] = said(step.range);
          else if (!step.tags && input) brief[step.key] = input.value.trim();""",
     """        if (at < STEPS.length) {
          if (step.range) brief[step.key] = said(step.range);
          else if (step.multi) { /* already in brief.skills */ }
          else if (!step.tags && input) brief[step.key] = input.value.trim();"""),

    ("""      var chips = card.querySelectorAll('.rec-flow-chip');
      chips.forEach(function (chip) {
        chip.addEventListener('click', function () {
          brief[step.key] = chip.textContent;
          if (input) { input.value = chip.textContent; draw(); return; }
          // nothing left to confirm on a chips-only step: the choice is the
          // answer, so it carries straight on
          onward();
        });
      });
      if (!input && chips.length) {
        (card.querySelector('.rec-flow-chip.is-on') || chips[0]).focus();
      }""",
     """      var chips = card.querySelectorAll('.rec-flow-chip');
      chips.forEach(function (chip) {
        chip.addEventListener('click', function () {
          var label = chip.textContent;
          if (step.multi) {
            var i = brief.skills.indexOf(label);
            if (i > -1) brief.skills.splice(i, 1); else brief.skills.push(label);
            draw();
            // back onto the chip just toggled: without this every pick throws
            // a keyboard user to the top of the stack
            [].slice.call(flow.querySelectorAll('.rec-flow-chip'))
              .forEach(function (c) { if (c.textContent === label) c.focus(); });
            return;
          }
          brief[step.key] = label;
          if (input) { input.value = label; draw(); return; }
          // nothing left to confirm on a single-choice step: the choice is the
          // answer, so it carries straight on
          onward();
        });
      });
      if (!input && !step.multi && chips.length) {
        (card.querySelector('.rec-flow-chip.is-on') || chips[0]).focus();
      }"""),

    # the stack wants a little more room between rows than a line of three
    ("""    .rec-flow-chips { display:flex; flex-wrap:wrap; gap:9px; margin-top:14px; }""",
     """    .rec-flow-chips { display:flex; flex-wrap:wrap; gap:9px; margin-top:14px;
                      max-width:640px; }"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert "multi: true" not in s, path + ': already a stack'
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:44], s.count(old))
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
