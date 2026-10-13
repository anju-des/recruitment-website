# -*- coding: utf-8 -*-
"""The field pops in, then follows the scroll direction.

Scrolling down takes it out of the way; scrolling back up brings it in. A
placeholder section below the hero gives the page something to scroll into.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- a section to scroll into ---------------------------------------------
old = """        </section>
"""
assert s.count(old) == 1, 'hero close moved'
s = s.replace(old, old + """
        <!-- NEXT SECTION (placeholder) -->
        <section class="rec-next" aria-hidden="true"></section>
""", 1)

# ---- css -------------------------------------------------------------------
old = '    /* ---- suggestions ------'
new = """    /* ---- next section (placeholder) ------------------------------------ */
    .rec-next { min-height:100vh; }

    /* ---- the field's entrance and its scroll behaviour ------------------ */
    /* pops in once on load, then follows the scroll direction: out of the way
       going down, back again coming up */
    @keyframes rec-field-in {
      from { opacity:0; transform:translateY(18px) scale(.96); }
      to   { opacity:1; transform:none; }
    }
    .rec-compose { animation:rec-field-in .62s cubic-bezier(.22,.61,.36,1) .12s both;
                   transition:opacity .34s cubic-bezier(.22,.61,.36,1),
                              transform .34s cubic-bezier(.22,.61,.36,1); }
    .rec-compose.is-out { opacity:0; transform:translateY(-22px) scale(.94);
                          pointer-events:none; }
    @media (prefers-reduced-motion: reduce) {
      .rec-compose { animation:none; transition:none; }
      .rec-compose.is-out { opacity:1; transform:none; pointer-events:auto; }
    }

""" + old
assert old in s, 'suggestions css marker moved'
s = s.replace(old, new, 1)

# ---- script ----------------------------------------------------------------
m = re.search(r'(\n  \}\(\)\);\n)</script>\n', s)
assert m, 'suggestion script close not found'

ADD = """
  // The field follows the scroll direction: away going down, back coming up.
  (function () {
    var field = document.querySelector('.rec-compose');
    var list = document.querySelector('.rec-suggest');
    if (!field) return;
    var last = window.scrollY, ticking = false;

    function update() {
      var y = window.scrollY;
      if (y > last && y > 24) {
        field.classList.add('is-out');
        if (list) list.hidden = true;
      } else if (y < last) {
        field.classList.remove('is-out');
      }
      last = y;
      ticking = false;
    }

    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(update);
    }, { passive: true });
  }());
"""
s = s[:m.end(1)] + ADD + '</script>\n' + s[m.end():]

io.open(p, 'w', encoding='utf-8').write(s)
print('field pop + scroll behaviour + placeholder section')
