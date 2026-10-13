# -*- coding: utf-8 -*-
"""Example briefs that appear under the field once someone starts typing.

They filter as you type and fill the field when picked, so the list is a
shortcut rather than decoration. Nothing shows on an empty field: the page at
rest is still just the headline and the field.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

SUGGESTIONS = [
    'Senior backend engineer, Python + Django, 4+ years, remote India',
    'Product designer, B2B SaaS, Figma + design systems, 3+ years',
    'Customer success manager, US-hours overlap, SaaS, 2+ years',
    'Full-stack engineer, React + Node, mid-level, fast-paced startup',
    'Finance analyst, India payroll + compliance, 3+ years',
]
rows = '\n'.join(
    '                  <li><button type="button">%s</button></li>' % t
    for t in SUGGESTIONS)

old = '              </form>\n'
new = """              </form>
              <ul class="rec-suggest" aria-label="Example roles" hidden>
%s
              </ul>
""" % rows
assert s.count(old) == 1, 'form close moved'
s = s.replace(old, new, 1)

old = '    /* ---- landing layout ---------------------------------------------- */\n'
new = """    /* ---- suggestions --------------------------------------------------- */
    /* sits under the field, same width, and only while there is something
       to match against */
    .rec-suggest { width:100%; max-width:820px; margin:10px auto 0; list-style:none;
                   background:var(--neutral-0); border:1px solid var(--border);
                   border-radius:14px; box-shadow:0 8px 28px rgba(18,22,32,.08);
                   overflow:hidden; text-align:left; }
    .rec-suggest li + li { border-top:1px solid var(--border); }
    .rec-suggest button { display:block; width:100%; text-align:left; cursor:pointer;
                          background:transparent; border:none; padding:13px 18px;
                          font-family:inherit; font-size:15px; font-weight:400;
                          line-height:1.4; color:var(--text-secondary);
                          transition:background .12s, color .12s; }
    .rec-suggest button:hover, .rec-suggest button:focus-visible {
      background:var(--primary-50); color:var(--text-primary); }

""" + old
assert old in s, 'landing layout marker moved'
s = s.replace(old, new, 1)

SCRIPT = """
<script>
  // The example briefs under the field: filtered by what has been typed,
  // hidden when the field is empty, and they fill the field when picked.
  (function () {
    var input = document.querySelector('.rec-compose-input');
    var list = document.querySelector('.rec-suggest');
    if (!input || !list) return;
    var options = [].slice.call(list.querySelectorAll('button'));

    function sync() {
      var q = input.value.trim().toLowerCase();
      var shown = 0;
      options.forEach(function (b) {
        var hit = q.length > 0 && b.textContent.toLowerCase().indexOf(q) > -1;
        b.parentNode.hidden = !hit;
        if (hit) shown++;
      });
      list.hidden = shown === 0;
    }

    input.addEventListener('input', sync);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') list.hidden = true;
    });
    options.forEach(function (b) {
      b.addEventListener('click', function () {
        input.value = b.textContent.trim();
        list.hidden = true;
        input.focus();
      });
    });
  }());
</script>
"""
assert '\n</body>' in s, 'body close missing'
s = s.replace('\n</body>', SCRIPT + '</body>', 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('suggestions added')
