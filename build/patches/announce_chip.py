# -*- coding: utf-8 -*-
"""An announcement pill above the headline.

Two halves in one pill, the way the reference does it: what is new on the
left, the way to read about it on the right, a hairline between them.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = '          <h1>Hire the right talent, anywhere in the\n'
new = """          <a class="rec-chip" href="#mira">
            <span class="rec-chip-dot" aria-hidden="true"></span>
            Mira, your AI recruiting agent, is live
            <span class="rec-chip-rule" aria-hidden="true"></span>
            <span class="rec-chip-more">Read more<svg viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2.2" stroke-linecap="round"
              stroke-linejoin="round" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></span>
          </a>
""" + old
assert old in s, 'headline markup changed'
s = s.replace(old, new, 1)

old = '    /* ---- hero ------------------------------------------------------------ */\n'
new = """    /* ---- announcement chip ------------------------------------------- */
    .rec-chip { display:inline-flex; align-items:center; gap:10px; margin-bottom:32px;
                padding:5px 14px 5px 12px; border-radius:100px; background:var(--neutral-0);
                border:1px solid var(--border); box-shadow:0 2px 10px rgba(18,22,32,.07);
                font-size:13.5px; font-weight:500; color:var(--text-secondary);
                white-space:nowrap; transition:box-shadow .15s, transform .15s; }
    .rec-chip:hover { box-shadow:0 4px 16px rgba(18,22,32,.11); transform:translateY(-1px); }
    .rec-chip-dot { width:7px; height:7px; border-radius:50%; flex:none;
                    background:linear-gradient(135deg,#2684FF,#8B5CF6); }
    .rec-chip-rule { width:1px; height:15px; background:var(--border-strong); flex:none; }
    .rec-chip-more { display:inline-flex; align-items:center; gap:3px;
                     color:var(--text-primary); font-weight:600; }
    .rec-chip-more svg { width:13px; height:13px; }

""" + old
assert old in s, 'hero css marker moved'
s = s.replace(old, new, 1)

old = '      .rec-hero h1 { font-size:44px; letter-spacing:-0.03em; }'
new = (old + '\n'
       '      .rec-chip { font-size:12.5px; gap:8px; margin-bottom:24px;\n'
       '                  white-space:normal; text-align:left; }')
assert old in s, 'responsive h1 rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('chip added')
