# -*- coding: utf-8 -*-
"""Carrying on past the first window brings two more alongside it.

The row is pinned to the middle of the screen while it assembles: the first
window slides left out of the centre and the other two arrive one after the
other, so you end up looking at the three things Mira does without the page
having moved on.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- markup: wrap the window in a pinned row -------------------------------
old = '        <section class="rec-chat-sec">\n          <div class="rec-win">'
new = """        <section class="rec-chat-sec">
          <div class="rec-wins-pin">
          <div class="rec-wins">
          <div class="rec-win">"""
assert old in s, 'chat section opening changed'
s = s.replace(old, new, 1)

BAR = """            <div class="rec-win-bar">
              <img class="rec-win-logo" src="mira-logo.svg" width="1152" height="365" alt="Mira">
              <span class="rec-win-dots" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                     stroke-linecap="round"><path d="M5 12h14"/></svg>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                     stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
              </span>
            </div>
"""

WIN2 = """          <div class="rec-win rec-win--side rec-win--2">
%s            <div class="rec-side-body">
              <p class="rec-side-k">Interview confirmed</p>
              <p class="rec-side-h">Ananya Rao &middot; Senior Backend Engineer</p>
              <p class="rec-side-t">Tomorrow, 11:00 &ndash; 11:45 IST</p>
              <div class="rec-side-who">
                <span>Panel</span><b>You, Dev lead</b>
              </div>
              <div class="rec-side-who">
                <span>Scorecard</span><b>Sent to both</b>
              </div>
              <button type="button" class="rec-side-btn">Join from calendar</button>
            </div>
          </div>
""" % BAR

WIN3 = """          <div class="rec-win rec-win--side rec-win--3">
%s            <div class="rec-side-body">
              <p class="rec-side-k">This month</p>
              <p class="rec-side-h">Three roles closed</p>
              <div class="rec-side-stat"><b>21</b><span>days to hire, average</span></div>
              <div class="rec-side-stat"><b>112</b><span>applications read</span></div>
              <div class="rec-side-stat"><b>0</b><span>paid until someone joined</span></div>
              <button type="button" class="rec-side-btn">Open the report</button>
            </div>
          </div>
""" % BAR

old = """            </div>
          </div>
        </section>"""
new = """            </div>
          </div>
%s%s          </div>
          </div>
        </section>""" % (WIN2, WIN3)
assert old in s, 'chat section close changed'
s = s.replace(old, new, 1)

# ---- css -------------------------------------------------------------------
old = """    .rec-chat-sec { min-height:110vh; display:grid; place-items:center; }
    .rec-win { width:min(720px, 100%); border-radius:16px; overflow:hidden;"""
new = """    /* tall enough to hold the row still while the three assemble */
    .rec-chat-sec { position:relative; min-height:230vh; }
    .rec-wins-pin { position:sticky; top:0; height:100vh; display:grid; place-items:center; }
    /* --row runs 0 to 1 past the first window: at 0 that window is centred,
       at 1 the whole row is */
    .rec-wins { display:flex; align-items:flex-start; gap:22px;
                transform:translateX(calc((1 - var(--row, 0)) * 352px)); }
    .rec-win { flex:none; width:540px; border-radius:16px; overflow:hidden;"""
assert old in s, 'chat section rules changed'
s = s.replace(old, new, 1)

old = """    .rec-ask-send { width:30px; height:30px; border-radius:50%; display:grid;"""
new = """    /* the two that arrive later */
    .rec-win--side { width:330px; opacity:0; transform:translateY(26px); }
    .rec-win--2 { opacity:var(--win2, 0);
                  transform:translateY(calc((1 - var(--win2, 0)) * 26px)); }
    .rec-win--3 { opacity:var(--win3, 0);
                  transform:translateY(calc((1 - var(--win3, 0)) * 26px)); }
    .rec-side-body { padding:18px; }
    .rec-side-k { font-size:12px; font-weight:600; letter-spacing:.04em;
                  text-transform:uppercase; color:#A78BFA; }
    .rec-side-h { margin-top:8px; font-size:15px; font-weight:600; line-height:1.4;
                  color:#F2F3F8; }
    .rec-side-t { margin-top:4px; font-size:13.5px; color:#9AA3B8; }
    .rec-side-who { display:flex; justify-content:space-between; gap:12px; margin-top:12px;
                    padding-top:12px; font-size:13px; color:#8E97AE;
                    box-shadow:inset 0 1px 0 rgba(255,255,255,.07); }
    .rec-side-who b { font-weight:600; color:#E8EAF2; }
    .rec-side-stat { display:flex; align-items:baseline; gap:9px; margin-top:12px; }
    .rec-side-stat b { font-size:22px; font-weight:600; color:#F2F3F8; }
    .rec-side-stat span { font-size:13px; color:#8E97AE; }
    .rec-side-btn { width:100%; margin-top:18px; padding:10px 14px; border:none;
                    border-radius:9px; font-family:inherit; font-size:13.5px;
                    font-weight:600; color:#E8EAF2; background:rgba(255,255,255,.09);
                    cursor:pointer; transition:background .12s; }
    .rec-side-btn:hover { background:rgba(255,255,255,.15); }

    .rec-ask-send { width:30px; height:30px; border-radius:50%; display:grid;"""
assert old in s, 'send rule changed'
s = s.replace(old, new, 1)

old = """      .rec-win { width:100%; }"""
new = """      /* no room for a row of three: they stack and stay put */
      .rec-chat-sec { min-height:0; padding-block:60px; }
      .rec-wins-pin { position:static; height:auto; }
      .rec-wins { flex-direction:column; align-items:stretch; transform:none; }
      .rec-win { width:100%; }
      .rec-win--side { width:100%; opacity:1; transform:none; }"""
assert old in s, 'responsive window rule changed'
s = s.replace(old, new, 1)

# ---- script ----------------------------------------------------------------
old = """          root.style.setProperty('--fall-o',
            Math.min(1, Math.max(0, (1 - f) / 0.2)).toFixed(3));"""
new = """          root.style.setProperty('--fall-o',
            Math.min(1, Math.max(0, (1 - f) / 0.2)).toFixed(3));

          // past the window, the row assembles: it slides left and the other
          // two arrive, one after the other
          var row = (window.scrollY - winLanding) / 760;
          row = Math.min(1, Math.max(0, row));
          root.style.setProperty('--row', row.toFixed(4));
          root.style.setProperty('--win2',
            Math.min(1, Math.max(0, (row - 0.12) / 0.34)).toFixed(3));
          root.style.setProperty('--win3',
            Math.min(1, Math.max(0, (row - 0.5) / 0.34)).toFixed(3));"""
assert old in s, 'fall opacity assignment changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('three windows in a pinned row')
