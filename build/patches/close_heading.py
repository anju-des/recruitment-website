# -*- coding: utf-8 -*-
"""A heading for the closing section, arriving with the light.

It is tied to the same scroll progress that lifts the sky, over a slightly
longer run, so the words come up as the page brightens rather than being
switched on at a threshold.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """        <!-- CLOSING -->
        <section class="rec-close">
        </section>"""
new = """        <!-- CLOSING -->
        <section class="rec-close">
          <h2 class="rec-close-h">Mira at every stage</h2>
        </section>"""
assert old in s, 'closing section markup changed'
s = s.replace(old, new, 1)

old = """    .rec-close { position:relative; min-height:120vh; }"""
new = """    .rec-close { position:relative; min-height:120vh; display:grid; place-items:center;
                 text-align:center; }
    /* --close-in runs 0 to 1 over the approach, so the words arrive with the
       light rather than switching on at a threshold */
    .rec-close-h { max-width:18ch; font-size:clamp(30px, 2.4vw + 14px, 58px);
                   font-weight:600; line-height:1.1; letter-spacing:-0.03em;
                   color:var(--grey-700); text-wrap:balance;
                   opacity:var(--close-in, 0);
                   transform:translateY(calc((1 - var(--close-in, 0)) * 40px)); }
    @media (prefers-reduced-motion: reduce) {
      .rec-close-h { opacity:1; transform:none; }
    }"""
assert old in s, 'closing section rule changed'
s = s.replace(old, new, 1)

old = """      var back = 0;
      if (close) {
        var ct = window.scrollY + close.getBoundingClientRect().top;
        back = (window.scrollY - (ct - window.innerHeight)) / window.innerHeight;
        back = Math.min(1, Math.max(0, back));
      }"""
new = """      var back = 0;
      if (close) {
        var ct = window.scrollY + close.getBoundingClientRect().top;
        back = (window.scrollY - (ct - window.innerHeight)) / window.innerHeight;
        back = Math.min(1, Math.max(0, back));
        // the heading takes a longer, slower run than the sky does
        var cin = (window.scrollY - (ct - window.innerHeight * 1.25))
                  / (window.innerHeight * 1.1);
        root.style.setProperty('--close-in', Math.min(1, Math.max(0, cin)).toFixed(3));
      }"""
assert old in s, 'sky back block changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('closing heading added')
