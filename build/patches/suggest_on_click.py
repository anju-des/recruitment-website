# -*- coding: utf-8 -*-
"""Open the suggestions on click, not only on the first keystroke.

Clicking or tabbing into the field shows the whole list; typing narrows it.
It closes on Escape or on a click anywhere outside -- and because the list
closes on outside pointerdown rather than on blur, a click that lands on a
suggestion still registers.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

m = re.search(r'\n<script>\n  // The example briefs.*?</script>\n', s, re.S)
assert m, 'suggestion script not found'

SCRIPT = """
<script>
  // The example briefs under the field: open on focus or click, narrowed by
  // whatever has been typed, and they fill the field when picked.
  (function () {
    var input = document.querySelector('.rec-compose-input');
    var list = document.querySelector('.rec-suggest');
    if (!input || !list) return;
    var options = [].slice.call(list.querySelectorAll('button'));

    function open() {
      var q = input.value.trim().toLowerCase();
      var shown = 0;
      options.forEach(function (b) {
        var hit = q.length === 0 || b.textContent.toLowerCase().indexOf(q) > -1;
        b.parentNode.hidden = !hit;
        if (hit) shown++;
      });
      list.hidden = shown === 0;
    }

    function close() { list.hidden = true; }

    input.addEventListener('focus', open);
    input.addEventListener('click', open);
    input.addEventListener('input', open);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { close(); }
    });

    // closing on outside pointerdown rather than on blur keeps a click that
    // lands on a suggestion alive long enough to register
    document.addEventListener('pointerdown', function (e) {
      if (!list.contains(e.target) && e.target !== input) close();
    });

    options.forEach(function (b) {
      b.addEventListener('click', function () {
        input.value = b.textContent.trim();
        close();
        input.focus();
      });
    });
  }());
"""
s = s[:m.start()] + SCRIPT + '</script>\n' + s[m.end():]

io.open(p, 'w', encoding='utf-8').write(s)
print('suggestions now open on click')
