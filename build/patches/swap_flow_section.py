# -*- coding: utf-8 -*-
"""Replace the feature cards + step track with the single four-column flow."""
import io
import flow_section

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# --- markup: everything from the features section up to the FAQ ------------
start = s.index('        <!-- WHAT THE RECRUITER DOES -->')
end = s.index('        <!-- FAQ -->')
old_markup = s[start:end]
assert 'rec-features' in old_markup and 'rec-track' in old_markup
s = s[:start] + flow_section.markup() + '\n\n' + s[end:]

# --- css: the two blocks those sections owned ------------------------------
css_start = s.index('    /* ---- what the recruiter does -------')
css_end = s.index('    /* ---- faq ---')
old_css = s[css_start:css_end]
assert '.rec-feature' in old_css and '.rec-track' in old_css
s = s[:css_start] + flow_section.CSS.lstrip('\n') + s[css_end:]

# --- responsive rules that referenced the old blocks -----------------------
s = s.replace("      .rec-features { grid-template-columns:1fr; }\n",
              "      .rec-flow { grid-template-columns:1fr 1fr; gap:32px 28px; }\n"
              "      .rec-flow-head { font-size:32px; }\n", 1)
s = s.replace("      .rec-track { grid-template-columns:1fr 1fr; gap:28px 24px; }\n", "", 1)
s = s.replace("      .rec-tstep:nth-child(2)::after { display:none; }\n", "", 1)
s = s.replace("      .rec-track { grid-template-columns:1fr; }\n",
              "      .rec-flow { grid-template-columns:1fr; }\n", 1)
s = s.replace("      .rec-tstep::after { display:none !important; }\n", "", 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('flow section swapped in')
for stale in ['rec-features', 'rec-feature', 'rec-track', 'rec-tstep', 'rec-band']:
    print('  %-14s still referenced: %s' % (stale, stale in s))
