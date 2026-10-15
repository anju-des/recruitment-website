# -*- coding: utf-8 -*-
"""Reopening starts at the beginning again.

build() ran once, so the card kept whatever step_two() had written into it:
open the panel a second time and it said "Now bring it back" to someone who
had not been anywhere. The first screen and its three handlers move into
render_one(), which runs on every open; the panel-level handlers stay in
build(), since replacing panel.innerHTML does not disturb listeners bound to
panel itself or to document.
"""
import io
import sys

OLD_HEAD = """      panel.setAttribute('aria-label', 'Connect your Claude');
      panel.innerHTML ="""
NEW_HEAD = """      panel.setAttribute('aria-label', 'Connect your Claude');
      document.body.appendChild(panel);

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

    // the first screen, rebuilt on every open
    function render_one() {
      panel.innerHTML ="""

OLD_TAIL = """      document.body.appendChild(panel);

      panel.querySelector('.rec-cxp-x').addEventListener('click', close);"""
NEW_TAIL = """      panel.querySelector('.rec-cxp-x').addEventListener('click', close);"""

OLD_END = """        } catch (e) { not(); }
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
      panel.classList.remove('is-out');"""
NEW_END = """        } catch (e) { not(); }
      });
    }

    opener.addEventListener('click', function () {
      if (!panel) build();
      render_one();
      panel.classList.remove('is-out');"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in ((OLD_HEAD, NEW_HEAD), (OLD_TAIL, NEW_TAIL),
                     (OLD_END, NEW_END)):
        assert s.count(old) == 1, (path, old.strip()[:50], s.count(old))
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
