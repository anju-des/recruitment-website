# -*- coding: utf-8 -*-
"""The window gets the logo, a violet glow, and a conversation worth reading.

The exchange now covers the three things a client actually asks Mira for: the
state of the pipeline, the interview schedule, and the monthly report.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- the logo in place of the name -----------------------------------------
old = '              <span class="rec-win-name">Mira</span>'
new = ('              <img class="rec-win-logo" src="mira-logo.svg" width="1152" height="365"'
       ' alt="Mira">')
assert old in s, 'window name markup changed'
s = s.replace(old, new, 1)

old = "    .rec-win-name { font-size:13.5px; font-weight:600; color:#E8EAF2; }"
new = ("    /* the logo is a dark mark, so it is inverted to sit on the dark bar */\n"
       "    .rec-win-logo { height:18px; width:auto; display:block;\n"
       "                    filter:invert(1) brightness(1.7); }")
assert old in s, 'window name rule changed'
s = s.replace(old, new, 1)

# ---- a violet glow ---------------------------------------------------------
old = """               box-shadow:0 30px 70px rgba(0,0,0,.45), inset 0 0 0 1px rgba(255,255,255,.07); }"""
new = """               box-shadow:0 24px 80px rgba(167,139,250,.22), 0 0 46px rgba(139,92,246,.14),
                          0 30px 70px rgba(0,0,0,.40), inset 0 0 0 1px rgba(255,255,255,.08); }"""
assert old in s, 'window shadow changed'
s = s.replace(old, new, 1)

# ---- the conversation ------------------------------------------------------
TURNS = [
    ('you', 'Where are we on the backend role?'),
    ('typing', None),
    ('mira', 'Pipeline&rsquo;s ready &mdash; 38 applications read, 6 shortlisted.'),
    ('you', 'Set up the interviews.'),
    ('typing', None),
    ('mira', 'Scheduled: Tue 11:00, Wed 15:30, Fri 10:00. Invites are out and all three have confirmed.'),
    ('you', 'And the monthly report?'),
    ('typing', None),
    ('mira', 'In your inbox. Three roles closed this month, 21 days average to hire.'),
]

def turn(kind, text):
    if kind == 'typing':
        return ('              <div class="rec-turn rec-turn--typing">'
                '<span class="rec-dot"></span><span class="rec-dot"></span>'
                '<span class="rec-dot"></span></div>')
    return ('              <div class="rec-turn rec-turn--%s"><p>%s</p></div>' % (kind, text))

m = re.search(r'            <div class="rec-thread">\n(.*?)\n            </div>\n', s, re.S)
assert m, 'thread block not found'
s = s[:m.start(1)] + '\n'.join(turn(k, t) for k, t in TURNS) + s[m.end(1):]

io.open(p, 'w', encoding='utf-8').write(s)
print('logo, glow and a fuller conversation')
