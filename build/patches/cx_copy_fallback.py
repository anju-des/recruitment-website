# -*- coding: utf-8 -*-
"""A fallback that copies, rather than one that apologises.

navigator.clipboard needs the document focused and throws NotAllowedError
when it is not -- which is exactly the case this button exists for, since
it is the one people reach for when the new tab did not open. The old
fallback told them to "select it and copy" with nothing on screen to
select.

A textarea off-screen plus execCommand('copy') is deprecated and works
everywhere this page runs, so it goes second and the message goes last.
"""
import io
import sys

OLD = """      var copy = panel.querySelector('.rec-cxp-copy');
      copy.addEventListener('click', function () {
        var done = function () { copy.textContent = 'Copied'; };
        var not = function () { copy.textContent = 'Select it and copy'; };
        try {
          if (navigator.clipboard) navigator.clipboard.writeText(PROMPT)
                                     .then(done, not);
          else not();
        } catch (e) { not(); }
      });"""

NEW = """      var copy = panel.querySelector('.rec-cxp-copy');
      copy.addEventListener('click', function () {
        var done = function () { copy.textContent = 'Copied \\u2014 paste it ' +
                                 'into Claude'; };
        // the asynchronous one wants the document focused and throws when it
        // is not; the old one does not care
        var old_way = function () {
          var box = document.createElement('textarea');
          box.value = PROMPT;
          box.setAttribute('readonly', '');
          box.style.cssText = 'position:fixed;top:-1000px;opacity:0';
          document.body.appendChild(box);
          box.select();
          var won = false;
          try { won = document.execCommand('copy'); } catch (e) {}
          box.remove();
          copy.textContent = won ? 'Copied \\u2014 paste it into Claude'
                                 : 'Could not copy here';
        };
        try {
          if (navigator.clipboard) {
            navigator.clipboard.writeText(PROMPT).then(done, old_way);
          } else { old_way(); }
        } catch (e) { old_way(); }
      });"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, s.count(OLD))
    s = s.replace(OLD, NEW, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
