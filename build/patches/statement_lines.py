# -*- coding: utf-8 -*-
"""The statement arrives a line at a time.

Each line is its own element so it can carry its own delay. The hidden start
state is added by script, so without JS the three lines are simply there.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """          <p class="rec-say">
            <strong>Mira reads every CV so you don&rsquo;t have to.</strong>
            It goes through all of them and picks out<br>
            the people who fit your role.
          </p>"""
new = """          <p class="rec-say">
            <span class="rec-line rec-line--lead">Mira reads every CV so you don&rsquo;t have to.</span>
            <span class="rec-line">It goes through all of them and picks out</span>
            <span class="rec-line">the people who fit your role.</span>
          </p>"""
assert old in s, 'statement markup changed'
s = s.replace(old, new, 1)

old = """    .rec-say strong { display:block; font-weight:600; color:#FFFFFF; }"""
new = """    .rec-line { display:block; }
    .rec-line--lead { font-weight:600; color:#FFFFFF; }
    /* each line waits its turn; the start state is added by script so the
       text is simply present if that never runs */
    .rec-say.rec-anim .rec-line { opacity:0; transform:translateY(16px); }
    .rec-say.rec-in .rec-line { animation:rec-line-in .75s cubic-bezier(.22,.61,.36,1) both; }
    .rec-say.rec-in .rec-line:nth-child(2) { animation-delay:.22s; }
    .rec-say.rec-in .rec-line:nth-child(3) { animation-delay:.44s; }
    @keyframes rec-line-in {
      from { opacity:0; transform:translateY(16px); }
      to   { opacity:1; transform:none; }
    }
    @media (prefers-reduced-motion: reduce) {
      .rec-say.rec-anim .rec-line { opacity:1; transform:none; }
      .rec-say.rec-in .rec-line { animation:none; }
    }"""
assert old in s, 'statement css changed'
s = s.replace(old, new, 1)

m = re.search(r'(\n  \}\(\)\);\n)</script>\n', s)
assert m, 'script close not found'

ADD = """
  // The statement arrives a line at a time, once, when it is well in view.
  (function () {
    var say = document.querySelector('.rec-say');
    if (!say || !('IntersectionObserver' in window)) return;
    say.classList.add('rec-anim');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        say.classList.add('rec-in');
        io.disconnect();
      });
    }, { threshold: 0.6 });
    io.observe(say);
  }());
"""
s = s[:m.end(1)] + ADD + '</script>\n' + s[m.end():]

io.open(p, 'w', encoding='utf-8').write(s)
print('lines reveal one by one')
