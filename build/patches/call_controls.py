# -*- coding: utf-8 -*-
"""Call controls under the tiles, and the panels really are equal now.

The fixed pane height was being overruled: a grid item's automatic minimum
size is its content, so the screening pane's row grew to 497 while the
others sat at 468 and the overflow was simply clipped. min-height:0 on the
items lets the row take the height it was given.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- the heights were being overruled by min-content -----------------------
old = """    .rec-stage-pane { display:none; }"""
new = """    .rec-stage-pane { display:none; }
    /* without this a grid item cannot shrink below its own content, and the
       pane's fixed height is quietly ignored */
    .rec-stage-pane.is-on > * { min-height:0; min-width:0; }"""
assert old in s, 'pane rule changed'
s = s.replace(old, new, 1)

# ---- the control bar -------------------------------------------------------
def ic(body):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true">%s</svg>' % body)

CAM = ic('<rect x="3" y="6" width="12.5" height="12" rx="2.5"/>'
         '<path d="M15.5 10.5L21 7.5v9l-5.5-3z"/>')
MIC = ic('<rect x="9" y="3" width="6" height="11" rx="3"/>'
         '<path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>')
SPK = ic('<path d="M4 9.5h3.5L12 5.5v13L7.5 14.5H4z"/>'
         '<path d="M16 9.5a4 4 0 0 1 0 5M18.6 7a7.5 7.5 0 0 1 0 10"/>')
END = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
       '<path d="M6.6 10.8a15.5 15.5 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 '
       '11.4 11.4 0 0 0 3.6.58 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 '
       '1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>')

BAR = """                    <div class="rec-call-bar">
                      <span class="rec-call-rec">Recording</span>
                      <span class="rec-call-btn">%s</span>
                      <span class="rec-call-btn">%s</span>
                      <span class="rec-call-btn">%s</span>
                      <span class="rec-call-btn rec-call-btn--end">%s</span>
                    </div>
""" % (CAM, MIC, SPK, END)

old = """                    </div>
                  </div>

                  <div class="rec-call-side">"""
assert old in s, 'call markup changed'
s = s.replace(old, """                    </div>
""" + BAR + """                  </div>

                  <div class="rec-call-side">""", 1)

old = """    .rec-call-vids { display:grid; grid-template-rows:minmax(0, 1fr) auto; gap:9px; }"""
new = """    .rec-call-vids { display:grid; grid-template-rows:minmax(0, 1fr) auto auto;
                     gap:9px; }
    /* the controls a call actually has, under the tiles */
    .rec-call-bar { display:flex; align-items:center; justify-content:center;
                    gap:7px; border-radius:100px; padding:5px 7px;
                    background:#17122B; }
    .rec-call-rec { display:inline-flex; align-items:center; gap:6px;
                    margin-right:3px; font-size:10.5px; font-weight:500;
                    color:#E7E3F5; background:rgba(255,255,255,.10);
                    border-radius:100px; padding:4px 10px; }
    .rec-call-rec::before { content:""; width:6px; height:6px; border-radius:50%;
                            background:#F04438; }
    .rec-call-btn { width:26px; height:26px; border-radius:50%; display:grid;
                    place-items:center; color:#D5CDF0;
                    background:rgba(255,255,255,.10); }
    .rec-call-btn svg { width:13px; height:13px; }
    .rec-call-btn--end { color:#FFFFFF; background:#F04438; }"""
assert old in s, 'vids grid rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('controls added, heights levelled')
