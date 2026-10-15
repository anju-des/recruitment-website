# -*- coding: utf-8 -*-
"""A miss stops the flow instead of carrying on without a company.

Finding nothing still ticked step one, filed a chip for a company that
was never found, and started step two -- which then built a job board
for it, header, listing and all. Every one of those says the lookup
worked.

The settle is now the success path only. On a miss the step stays
current rather than done, nothing is tucked, nothing is saved for a
restore, and step two does not begin: the screen keeps its "Try another
website" and waits.

A missed lookup is also not worth restoring, so the record is only
written when there is something in it.
"""
import io
import sys

OLD = """        function rest() {
          busy = '';
          finished = true;
          at_step(0, true);
          // let it be read at full size before it becomes a card
          window.setTimeout(function () {
            if (!flow || flow.hidden) return;
            found = { who: who, logo: logo, based: vals.Based || '' };
            flow.classList.add('is-found');
            open_i = null;
            put_mini(0, who, logo, card.innerHTML);
            card.innerHTML = '';
            step_busy(1);          // no dead "2" in the gap
            window.setTimeout(board, 700);
          }, 1600);
          window.setTimeout(function () {
            try {
              window.sessionStorage.setItem('wm-flow', JSON.stringify({
                role: brief.role, website: brief.website,
                who: who, logo: logo, html: card.innerHTML
              }));
            } catch (e) {}
          }, 0);
          screen();
          flow.querySelector('.rec-flow-bar span')
              .style.setProperty('--at', '100%');
        }"""

NEW = """        function rest() {
          busy = '';
          finished = true;
          var nothing = !got.about && !(got.facts && got.facts.length);

          // a miss leaves the step current, not done: there is no company
          at_step(0, !nothing);
          screen();

          if (nothing) return;

          flow.querySelector('.rec-flow-bar span')
              .style.setProperty('--at', '100%');

          // let it be read at full size before it becomes a card
          window.setTimeout(function () {
            if (!flow || flow.hidden) return;
            found = { who: who, logo: logo, based: vals.Based || '' };
            flow.classList.add('is-found');
            open_i = null;
            put_mini(0, who, logo, card.innerHTML);
            card.innerHTML = '';
            step_busy(1);          // no dead "2" in the gap
            window.setTimeout(board, 700);
          }, 1600);

          window.setTimeout(function () {
            try {
              window.sessionStorage.setItem('wm-flow', JSON.stringify({
                role: brief.role, website: brief.website,
                who: who, logo: logo, html: card.innerHTML
              }));
            } catch (e) {}
          }, 0);
        }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, s.count(OLD))
    s = s.replace(OLD, NEW, 1)
    js = s[s.rindex('<script>'):]
    assert 'if (nothing) return;' in js, path + ': the guard did not land'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
