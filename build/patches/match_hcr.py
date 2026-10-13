# -*- coding: utf-8 -*-
"""Match the hero composer to the real one in Recruitment-frontend.

Values copied from src/components/HomeCreateRole.css and the icon paths from
HomeCreateRole.tsx. Those are the recruit portal's own identity colours (slate
neutrals, near-black button) which are deliberately NOT the Wisemonk portal
palette -- so the ui-check will flag them here. Kept verbatim because the ask
was for the same field, not an equivalent one.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---------------------------------------------------------------- markup
start = s.index('              <form class="rec-compose"')
end = s.index('</form>', start) + len('</form>')
old = s[start:end]
assert 'rec-compose-post' in old, 'composer markup changed'

ICONS = {
    'jd': ('<path d="M14 3v4a1 1 0 0 0 1 1h4"/>'
           '<path d="M17 21H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7l5 5v11a2 2 0 0 1-2 2z"/>'),
    'link': ('<path d="M10 13a5 5 0 0 0 7.07 0l1.93-1.93a5 5 0 0 0-7.07-7.07L10.5 5.5"/>'
             '<path d="M14 11a5 5 0 0 0-7.07 0L5 12.93a5 5 0 0 0 7.07 7.07L13.5 18.5"/>'),
    'skills': ('<path d="M12 2.5l2.9 5.9 6.5.95-4.7 4.58 1.11 6.47L12 17.9l-5.81 '
               '3.06L7.3 14.5 2.6 9.9l6.5-.95L12 2.5z"/>'),
}
SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
       'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>')

new = u"""              <form class="rec-compose" onsubmit="return false">
                <p class="rec-compose-greet">Good afternoon</p>
                <div class="rec-compose-headrow">
                  <textarea class="rec-compose-input" rows="1"
                            aria-label="Describe the role, paste a link, or add skills"
                            placeholder="What role are you hiring for, Sarah?"></textarea>
                </div>
                <div class="rec-compose-foot">
                  <div class="rec-compose-tools">
                    <button type="button">%s JD</button>
                    <button type="button">%s Link</button>
                    <button type="button">%s Skills</button>
                  </div>
                  <button type="submit" class="rec-compose-post">Post role</button>
                </div>
              </form>""" % (SVG % ICONS['jd'], SVG % ICONS['link'], SVG % ICONS['skills'])
s = s[:start] + new + s[end:]

# ---------------------------------------------------------------- styles
css_start = s.index('    /* ---- hero composer ---')
css_end = s.index('    /* ---- posted role to signed offer')
assert css_end > css_start

new_css = u"""    /* ---- hero composer ----------------------------------------------- */
    /* Values lifted from Recruitment-frontend/src/components/HomeCreateRole.css
       so this is the portal's own field, not a lookalike. Those are the recruit
       portal's identity colours (slate + near-black), which the Wisemonk palette
       check will flag -- the two design systems are separate by design. */
    .rec-compose { max-width:900px; margin:32px auto 0; text-align:left;
                   background:#ffffff; border:none; border-radius:14px;
                   padding:14px 18px 12px; box-shadow:0 8px 28px rgba(37,99,235,0.12); }
    .rec-compose-greet { font-size:13px; font-weight:500; color:#94a3b8; margin-bottom:10px; }
    .rec-compose-headrow { display:flex; align-items:center; gap:12px; margin-bottom:30px; }
    .rec-compose-input { flex:1; min-width:0; border:none; outline:none; resize:none;
                         background:transparent; font-family:'Satoshi',sans-serif;
                         font-size:20px; font-weight:500; line-height:1.35; color:#1e293b;
                         letter-spacing:-0.01em; padding:0; margin:0; overflow:hidden; }
    .rec-compose-input::placeholder { color:#94a3b8; font-weight:500; opacity:1; }
    .rec-compose-foot { display:flex; align-items:center; justify-content:space-between;
                        gap:16px; border-top:1px solid #eef0f4; padding-top:12px; }
    .rec-compose-tools { display:flex; align-items:center; gap:6px; }
    .rec-compose-tools button { display:inline-flex; align-items:center; gap:7px;
                                background:transparent; border:none; cursor:pointer;
                                color:#475569; font-family:'Satoshi',sans-serif; font-size:14px;
                                font-weight:500; padding:7px 11px; border-radius:9px;
                                transition:background .12s, color .12s; }
    .rec-compose-tools button:hover { background:#f1f5f9; color:#1e293b; }
    .rec-compose-tools svg { width:16px; height:16px; }
    .rec-compose-post { flex:none; background:#0f172a; color:#ffffff; border:none; cursor:pointer;
                        font-family:'Satoshi',sans-serif; font-size:14px; font-weight:600;
                        padding:10px 22px; border-radius:8px; transition:background .12s; }
    .rec-compose-post:hover { background:#1e293b; }
    .rec-search-hint { display:inline-flex; align-items:center; justify-content:center; gap:8px;
                       margin-top:16px; font-size:13.5px; font-weight:500; color:var(--text-secondary); }
    .rec-search-hint svg { width:16px; height:16px; color:var(--primary-500); flex-shrink:0; }
    .rec-search-hint b { font-weight:700; color:var(--primary-600); }

"""
s = s[:css_start] + new_css + s[css_end:]

# the repo stacks the toolbar under 640px
s = s.replace("      .rec-compose { padding:16px 16px 0; }\n"
              "      .rec-compose-input { font-size:18px; }\n"
              "      .rec-compose-foot { flex-wrap:wrap; }\n",
              "      .rec-compose-foot { flex-direction:column; align-items:stretch; }\n"
              "      .rec-compose-post { width:100%; }\n", 1)

# the sprite icons it used are no longer referenced
s = s.replace("NEEDED = ['ic-document', 'ic-link', 'ic-star']",
              "NEEDED = []  # the composer carries the portal's own inline icons", 1)
s = s.replace("assert symbols, 'expected to add icons'\n", "", 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('composer matched to the repo')
