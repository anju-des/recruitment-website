# -*- coding: utf-8 -*-
"""Push the section modules into the builder.

Each CSS block is bounded by the NEXT section's comment, not by the FAQ one --
using the FAQ as a universal end marker silently swallowed every block in
between. Every substitution asserts, because a silent no-op here looks like
success and then reverts on the next regeneration.
"""
import io
import flow_section
import promises_section
import stats_section
import pricing_section

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

FAQ = '    /* ---- faq ---'

# css blocks in page order: marker, module, the section it must stop before
BLOCKS = [
    ('    /* ---- posted role to signed offer', flow_section),
    ('    /* ---- mira ai scores', promises_section),
    ('    /* ---- behind the product', stats_section),
    ('    /* ---- plans ---', pricing_section),
]


def insert_section(text, module, css_marker, responsive_after=None):
    """Add a section's markup before the FAQ and its css before the faq rules."""
    anchor = '        <!-- FAQ -->'
    assert anchor in text, 'faq anchor missing'
    text = text.replace(anchor, module.markup() + '\n\n' + anchor, 1)
    assert FAQ in text, 'faq css marker missing'
    text = text.replace(FAQ, module.CSS.lstrip('\n') + FAQ, 1)
    if responsive_after:
        for rule, extra in responsive_after:
            assert rule in text, 'responsive anchor missing'
            text = text.replace(rule, rule + extra, 1)
    return text


if 'rec-promise' not in s:
    s = insert_section(s, promises_section, '    /* ---- mira ai scores', [
        ('      .rec-flow { grid-template-columns:1fr 1fr; gap:32px 28px; }\n',
         promises_section.RESPONSIVE),
        ('      .rec-flow { grid-template-columns:1fr; }\n',
         promises_section.RESPONSIVE_SM),
    ])

if 'rec-stats' not in s:
    s = insert_section(s, stats_section, '    /* ---- behind the product', [
        (promises_section.RESPONSIVE, stats_section.RESPONSIVE),
        (promises_section.RESPONSIVE_SM, stats_section.RESPONSIVE_SM),
    ])

if '<!-- PLANS -->' not in s:
    s = insert_section(s, pricing_section, '    /* ---- plans ---', [
        (stats_section.RESPONSIVE, pricing_section.RESPONSIVE),
    ])

# now refresh every css block in place, each bounded by the next one
for i, (marker, module) in enumerate(BLOCKS):
    assert marker in s, 'missing css marker: ' + marker
    end_marker = BLOCKS[i + 1][0] if i + 1 < len(BLOCKS) else FAQ
    assert end_marker in s, 'missing end marker: ' + end_marker
    a, b = s.index(marker), s.index(end_marker)
    assert b > a, 'css blocks out of order at ' + marker
    s = s[:a] + module.CSS.lstrip('\n') + s[b:]

# The stats band needs the deeper primary steps the page has not carried.
# Look for the DEFINITION, not the name -- the band's css mentions the token
# via var(), which made an earlier guard think it was already defined.
if '--primary-800:#09449A' not in s:
    anchor = '"--primary-400:#72ABFF; --primary-500:#2684FF;", 1)'
    assert anchor in s, 'token anchor moved'
    s = s.replace(
        anchor,
        '"--primary-400:#72ABFF; --primary-500:#2684FF; "\n'
        '    "--primary-700:#1059BD; --primary-800:#09449A; --primary-900:#03307A;", 1)',
        1)

io.open(p, 'w', encoding='utf-8').write(s)
print('sections applied')
for needle, want in [('font-size:26px', True), ('rec-promise', True),
                     ('rec-stats', True), ('--primary-800', True),
                     ('font-size:44px', True)]:
    print('  %-18s present=%s' % (needle, needle in s))
