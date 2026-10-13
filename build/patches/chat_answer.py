# -*- coding: utf-8 -*-
"""Mira answers once, properly: sources, a summary, a table and next steps.

Instead of a back-and-forth of short bubbles, the window now shows what the
agent actually produces -- what it read, where each line came from, and what
you can do next. The reveal machinery is unchanged: every block is still a
turn, so they arrive in order with the typing bubble standing in for the
pause before the answer.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

ROWS = [
    ('Shortlisted', '6 of 38 applications', 'logo-8.svg', 'Careers site'),
    ('Interviews', '3 confirmed this week', 'logo-4.svg', 'Calendar'),
    ('Top match', '7 yrs Django &middot; shipped payments', 'logo-7.svg', 'Scorecard'),
    ('Time to hire', '21 days average', 'logo-3.svg', 'Weekly report'),
]
rows = '\n'.join(
    """                  <div class="rec-row">
                    <span class="rec-row-k">%s</span>
                    <span class="rec-row-v">%s</span>
                    <span class="rec-row-src"><img src="%s" alt="" loading="lazy">%s</span>
                  </div>""" % (k, v, logo, src) for k, v, logo, src in ROWS)

CHIPS = ('See the shortlist', 'Open the schedule', 'Send me the report')
chips = '\n'.join('                <button type="button">%s</button>' % c for c in CHIPS)

THREAD = """              <div class="rec-turn rec-turn--you"><p>Where are we on the Senior Backend Engineer role?</p></div>
              <div class="rec-turn rec-turn--typing"><span class="rec-dot"></span><span class="rec-dot"></span><span class="rec-dot"></span></div>
              <div class="rec-turn rec-turn--meta">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
                     stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
                Read 38 applications across 4 sources
              </div>
              <div class="rec-turn rec-turn--say"><p>Here is where the role stands this morning.</p></div>
              <div class="rec-turn rec-turn--card">
                <div class="rec-card-head">
                  <span>
                    <b>Senior Backend Engineer</b>
                    <i>Bengaluru &middot; Full-time</i>
                  </span>
                  <span class="rec-card-count">38 applications</span>
                </div>
%s
              </div>
              <div class="rec-turn rec-turn--say"><p>Three interviews are booked for this week. The rest of the shortlist is waiting on your call.</p></div>
              <div class="rec-turn rec-turn--chips">
%s
              </div>""" % (rows, chips)

m = re.search(r'            <div class="rec-thread">\n(.*?)\n            </div>\n', s, re.S)
assert m, 'thread block not found'
s = s[:m.start(1)] + THREAD + s[m.end(1):]

# ---- an Agent chip in the composer, as in the reference --------------------
old = """                <span class="rec-ask-send" aria-hidden="true">"""
new = """                <span class="rec-ask-right">
                <span class="rec-ask-agent">
                  <img src="mira-logo.svg" alt="" width="1152" height="365">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"
                       stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9.5l6 6 6-6"/></svg>
                </span>
                <span class="rec-ask-send" aria-hidden="true">"""
assert old in s, 'composer markup changed'
s = s.replace(old, new, 1)

old = """                </span>
              </div>
            </div>
          </div>
        </section>"""
new = """                </span>
                </span>
              </div>
            </div>
          </div>
        </section>"""
assert old in s, 'composer close changed'
s = s.replace(old, new, 1)

# ---- css -------------------------------------------------------------------
old = """    .rec-ask-send { width:30px; height:30px; border-radius:50%; display:grid;"""
new = """    /* an answer rather than a bubble: what was read, a table of what it found,
       and the things you would do next */
    .rec-turn--meta, .rec-turn--say, .rec-turn--card, .rec-turn--chips {
      align-self:stretch; max-width:none; padding:0; background:none; }
    .rec-turn--meta { display:flex; align-items:center; gap:9px; font-size:13.5px;
                      color:#8E97AE; }
    .rec-turn--meta svg { width:15px; height:15px; color:#A78BFA; }
    .rec-turn--say { font-size:14.5px; line-height:1.55; color:#E8EAF2; }
    .rec-turn--card { border-radius:12px; overflow:hidden;
                      box-shadow:inset 0 0 0 1px rgba(255,255,255,.08); }
    .rec-card-head { display:flex; align-items:flex-start; justify-content:space-between;
                     gap:16px; padding:14px 16px; background:rgba(255,255,255,.04); }
    .rec-card-head b { display:block; font-size:14.5px; font-weight:600; color:#F2F3F8; }
    .rec-card-head i { display:block; margin-top:2px; font-style:normal; font-size:12.5px;
                       color:#8E97AE; }
    .rec-card-count { flex:none; font-size:12.5px; color:#A78BFA; }
    .rec-row { display:grid; grid-template-columns:116px 1fr auto; align-items:center;
               gap:14px; padding:11px 16px;
               box-shadow:inset 0 1px 0 rgba(255,255,255,.06); }
    .rec-row-k { font-size:13px; color:#8E97AE; }
    .rec-row-v { font-size:13.5px; font-weight:600; color:#F2F3F8; }
    .rec-row-src { display:inline-flex; align-items:center; gap:7px; font-size:12.5px;
                   color:#9AA3B8; white-space:nowrap; }
    .rec-row-src img { width:15px; height:15px; object-fit:contain; }
    .rec-turn--chips { display:flex; flex-wrap:wrap; gap:8px; }
    .rec-turn--chips button { font-family:inherit; font-size:13px; font-weight:500;
                              color:#E8EAF2; background:rgba(255,255,255,.07);
                              border:none; border-radius:8px; padding:8px 13px;
                              cursor:pointer; transition:background .12s; }
    .rec-turn--chips button:hover { background:rgba(255,255,255,.13); }

    .rec-ask-right { display:inline-flex; align-items:center; gap:10px; }
    .rec-ask-agent { display:inline-flex; align-items:center; gap:7px; padding:5px 10px;
                     border-radius:8px; background:rgba(255,255,255,.08); color:#9AA3B8; }
    .rec-ask-agent img { height:11px; width:auto; filter:invert(1) brightness(1.7); }
    .rec-ask-agent svg { width:12px; height:12px; }
    .rec-ask-send { width:30px; height:30px; border-radius:50%; display:grid;"""
assert old in s, 'send rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('answer-style thread')
