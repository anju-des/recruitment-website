# -*- coding: utf-8 -*-
"""The closing words arrive as three lines, one at a time.

Same shape as the statement section near the top of the page -- a line per
scroll band -- so the end rhymes with the beginning rather than inventing a
new behaviour for its last screen.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """            <p class="rec-say-last">
              Mira is a new generation of recruiting agent.
              <span>It does the work of hiring, not just the record of it. And
                it knows where its job ends and yours begins.</span>
            </p>"""
new = """            <p class="rec-say-last">
              <span class="rec-last-line">Mira is a new generation of recruiting agent.</span>
              <span class="rec-last-line">It does the work of hiring, not just the record of it.</span>
              <span class="rec-last-line">And it knows where its job ends and yours begins.</span>
            </p>"""
assert old in s, 'closing markup changed'
s = s.replace(old, new, 1)

start = s.index('    /* the words arrive where the mark was */')
end = s.index('    /* ---- suggestions ------', start)
old = s[start:end]
assert 'rec-say-last' in old, 'closing styles changed'

new = """    /* the words arrive where the mark was, a line at a time */
    .rec-say-last { position:absolute; left:50%; top:50%; translate:-50% -50%;
                    width:min(88vw, 780px); margin:0; text-align:center;
                    display:flex; flex-direction:column; gap:12px; }
    .rec-last-line { display:block; color:#FFFFFF; text-wrap:balance;
                     font-size:clamp(18px, 1.05vw + 10px, 26px); font-weight:600;
                     line-height:1.38; letter-spacing:-0.02em;
                     opacity:var(--ln, 0);
                     transform:translateY(calc((1 - var(--ln, 0)) * 20px)); }
    .rec-last-line:nth-child(1) { --ln:var(--s1, 0); }
    .rec-last-line:nth-child(2) { --ln:var(--s2, 0); }
    /* the last one is the quiet half of the thought */
    .rec-last-line:nth-child(3) { --ln:var(--s3, 0); color:#A79FC8;
                                  font-weight:500; }
    @media (prefers-reduced-motion: reduce) {
      .rec-last-line { transform:none; }
    }

"""
s = s[:start] + new + s[end:]

old = """      .rec-say-last { position:static; translate:none; opacity:1; transform:none;
                      width:auto; }"""
new = """      .rec-say-last { position:static; translate:none; width:auto; }
      .rec-last-line { opacity:1; transform:none; }"""
assert old in s, 'responsive closing rule changed'
s = s.replace(old, new, 1)

old = """        // and then the line, starting only once the mark has fully gone
        root.style.setProperty('--say',
          Math.min(1, Math.max(0, (q - 0.66) / 0.24)).toFixed(3));"""
new = """        // and then the lines, one at a time, once the mark has fully gone
        var line = function (a, b) {
          return Math.min(1, Math.max(0, (q - a) / (b - a))).toFixed(3);
        };
        root.style.setProperty('--s1', line(0.64, 0.75));
        root.style.setProperty('--s2', line(0.76, 0.86));
        root.style.setProperty('--s3', line(0.87, 0.96));"""
assert old in s, 'say band changed'
s = s.replace(old, new, 1)

# `--say-out` and `rec-turn--say` are other things entirely; only the closing
# block's own variable should be gone
assert "setProperty('--say'" not in s, 'the --say setter is left'
assert 'var(--say,' not in s, 'a var(--say) reference is left'
io.open(p, 'w', encoding='utf-8').write(s)
print('three lines, one at a time')
