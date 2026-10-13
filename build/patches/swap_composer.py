# -*- coding: utf-8 -*-
"""Replace the hero's search pill with the portal's composer card."""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# --- icons -----------------------------------------------------------------
old_needed = "NEEDED = ['ic-profile-2user', 'ic-user-search', 'ic-calendar-tick',\n          'ic-search-normal']"
new_needed = ("NEEDED = ['ic-profile-2user', 'ic-user-search', 'ic-calendar-tick',\n"
              "          'ic-document', 'ic-link', 'ic-star']")
assert old_needed in s, 'icon list moved'
s = s.replace(old_needed, new_needed, 1)

# --- markup ----------------------------------------------------------------
start = s.index('              <form class="rec-search"')
end = s.index('</form>', start) + len('</form>')
old_form = s[start:end]
assert 'rec-search-btn' in old_form, 'search form markup changed'

new_form = u"""              <form class="rec-compose" onsubmit="return false">
                <p class="rec-compose-greet">Good afternoon, Sarah</p>
                <input class="rec-compose-input" type="text" autocomplete="off"
                       aria-label="Describe the role you are hiring for"
                       placeholder="What role are you hiring for?">
                <div class="rec-compose-foot">
                  <div class="rec-compose-tools">
                    <button type="button"><svg viewBox="0 0 24 24"><use href="#ic-document"/></svg>JD</button>
                    <button type="button"><svg viewBox="0 0 24 24"><use href="#ic-link"/></svg>Link</button>
                    <button type="button"><svg viewBox="0 0 24 24"><use href="#ic-star"/></svg>Skills</button>
                  </div>
                  <button type="submit" class="rec-compose-post">Post role</button>
                </div>
              </form>"""
s = s[:start] + new_form + s[end:]

# --- styles ----------------------------------------------------------------
css_start = s.index('    /* ---- hero search ---')
css_end = s.index('    /* ---- posted role to signed offer')
old_css = s[css_start:css_end]
assert '.rec-search-btn' in old_css, 'hero search css changed'

new_css = u"""    /* ---- hero composer ----------------------------------------------- */
    /* the portal's own composer rather than a search pill: a card with the
       prompt on top and the actions along its floor */
    .rec-compose { max-width:900px; margin:32px auto 0; text-align:left;
                   background:var(--neutral-0); border:1px solid var(--neutral-200);
                   border-radius:12px; padding:20px 24px 0;
                   transition:border-color .15s, box-shadow .15s; }
    .rec-compose:focus-within { border-color:var(--primary-500); box-shadow:0 0 0 4px var(--primary-50); }
    .rec-compose-greet { font-size:12.5px; font-weight:500; color:var(--text-muted); }
    .rec-compose-input { width:100%; margin-top:10px; padding:0 0 20px; border:none; outline:none;
                         background:transparent; font-family:'Satoshi',sans-serif;
                         font-size:21px; font-weight:500; color:var(--text-primary); }
    .rec-compose-input::placeholder { color:var(--neutral-300); font-weight:500; }
    .rec-compose-foot { display:flex; align-items:center; justify-content:space-between; gap:16px;
                        border-top:1px solid var(--border); padding:12px 0; }
    .rec-compose-tools { display:flex; align-items:center; gap:8px; }
    .rec-compose-tools button { display:inline-flex; align-items:center; gap:7px; border:none;
                                background:none; cursor:pointer; padding:6px 10px; border-radius:8px;
                                font-family:'Satoshi',sans-serif; font-size:13.5px; font-weight:500;
                                color:var(--text-secondary); transition:background .15s; }
    .rec-compose-tools button:hover { background:var(--neutral-50); }
    .rec-compose-tools svg { width:16px; height:16px; color:var(--text-muted); }
    .rec-compose-post { flex-shrink:0; border:none; cursor:pointer; border-radius:8px;
                        background:var(--neutral-900); color:var(--neutral-0); padding:11px 20px;
                        font-family:'Satoshi',sans-serif; font-size:13.5px; font-weight:700;
                        transition:background .15s; }
    .rec-compose-post:hover { background:var(--grey-700); }
    .rec-search-hint { display:inline-flex; align-items:center; justify-content:center; gap:8px;
                       margin-top:16px; font-size:13.5px; font-weight:500; color:var(--text-secondary); }
    .rec-search-hint svg { width:16px; height:16px; color:var(--primary-500); flex-shrink:0; }
    .rec-search-hint b { font-weight:700; color:var(--primary-600); }

"""
s = s[:css_start] + new_css + s[css_end:]

# the phone rule targeted the old pill
s = s.replace("      .rec-search { flex-direction:column; align-items:stretch; gap:10px; "
              "border-radius:8px; padding:14px; }\n"
              "      .rec-search-btn { justify-content:center; }\n",
              "      .rec-compose { padding:16px 16px 0; }\n"
              "      .rec-compose-input { font-size:18px; }\n"
              "      .rec-compose-foot { flex-wrap:wrap; }\n", 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('composer swapped in')
for stale in ['rec-search ', 'rec-search-btn', 'rec-search-ic', 'ic-search-normal']:
    print('  %-16s still referenced: %s' % (stale, stale in s))
