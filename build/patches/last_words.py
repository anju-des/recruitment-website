# -*- coding: utf-8 -*-
"""A line about Mira, once the loop has gone.

The section had no scroll left after the unwind, so it grows by a screen and
everything that already existed is fed a sub-progress that finishes at 62%.
The rest of the scroll belongs to the words, which come up in the same place
the mark left.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """            <img class="rec-orb-mark\""""
if old in s:
    raise SystemExit('unexpected markup')

old = """            </span>
          </div>
        </section>"""
new = """            </span>

            <p class="rec-say-last">
              Mira is a new generation of recruiting agent.
              <span>It reads every application the day it lands, books the panel
                around the time people have, chases the scorecard while the
                interview is fresh and drafts the offer off your band &mdash; so
                the hour you spend hiring is the hour only you can spend.</span>
            </p>
          </div>
        </section>"""
assert old in s, 'orb pin markup changed'
s = s.replace(old, new, 1)

CSS = """    /* the words arrive where the mark was */
    .rec-say-last { position:absolute; left:50%; top:50%; translate:-50% -50%;
                    width:min(88vw, 760px); margin:0; text-align:center;
                    color:#FFFFFF; font-size:clamp(20px, 1.3vw + 11px, 30px);
                    font-weight:600; line-height:1.3; letter-spacing:-0.02em;
                    text-wrap:balance;
                    opacity:var(--say, 0);
                    transform:translateY(calc((1 - var(--say, 0)) * 26px)); }
    .rec-say-last span { display:block; margin-top:14px; max-width:52ch;
                         margin-inline:auto; color:#A79FC8; font-size:15px;
                         font-weight:400; line-height:1.65;
                         letter-spacing:normal; }
    @media (prefers-reduced-motion: reduce) {
      .rec-say-last { transform:none; }
    }

"""
anchor = "    /* ---- suggestions ------"
assert anchor in s, 'suggestions block missing'
s = s.replace(anchor, CSS + anchor, 1)

old = """      .rec-orb-pin { position:static; height:auto; padding-block:84px; }"""
new = """      .rec-orb-pin { position:static; height:auto; padding-block:84px; gap:40px; }
      .rec-say-last { position:static; translate:none; opacity:1; transform:none;
                      width:auto; }"""
assert old in s, 'responsive orb rule changed'
s = s.replace(old, new, 1)

# ---- a screen more scroll, and the old sequence packed into the first part --
old = """    .rec-rest { position:relative; min-height:200vh; }"""
new = """    .rec-rest { position:relative; min-height:300vh; }"""
assert old in s, 'rest section rule changed'
s = s.replace(old, new, 1)

old = """        var q = Math.min(1, Math.max(0, (window.scrollY - rt) / rspan));
        root.style.setProperty('--orb', q.toFixed(3));"""
new = """        var q = Math.min(1, Math.max(0, (window.scrollY - rt) / rspan));
        // the light, the mark and the unwind all play out over the first part;
        // what is left of the scroll belongs to the words
        var e = Math.min(1, q / 0.62);
        root.style.setProperty('--orb', e.toFixed(3));"""
assert old in s, 'orb progress changed'
s = s.replace(old, new, 1)

for a, b in [
    ("Math.min(1, Math.max(0, (q - 0.22) / 0.44)).toFixed(3));",
     "Math.min(1, Math.max(0, (e - 0.22) / 0.44)).toFixed(3));"),
    ("Math.min(1, Math.max(0, (q - 0.58) / 0.18)).toFixed(3));",
     "Math.min(1, Math.max(0, (e - 0.58) / 0.18)).toFixed(3));"),
    ("(1 - Math.min(1, Math.max(0, (q - 0.78) / 0.22))).toFixed(3));",
     "(1 - Math.min(1, Math.max(0, (e - 0.78) / 0.22))).toFixed(3));"),
    ("(1 - Math.min(1, Math.max(0, (q - 0.78) / 0.10))).toFixed(3));",
     "(1 - Math.min(1, Math.max(0, (e - 0.78) / 0.10))).toFixed(3));"),
    ("Math.min(1, Math.max(0, (q - 0.93) / 0.07)).toFixed(3));",
     "Math.min(1, Math.max(0, (e - 0.93) / 0.07)).toFixed(3));"),
]:
    assert a in s, 'band changed: ' + a[:40]
    s = s.replace(a, b, 1)

old = """        root.style.setProperty('--gone',
          Math.min(1, Math.max(0, (e - 0.93) / 0.07)).toFixed(3));"""
new = """        root.style.setProperty('--gone',
          Math.min(1, Math.max(0, (e - 0.93) / 0.07)).toFixed(3));
        // and then the line, starting only once the mark has fully gone
        root.style.setProperty('--say',
          Math.min(1, Math.max(0, (q - 0.66) / 0.24)).toFixed(3));"""
assert old in s, 'gone band changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('the last words')
