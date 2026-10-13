# -*- coding: utf-8 -*-
"""The stage section turns light, and the sky rises into it.

The dark passage now ends at the windows: from there the ramp climbs back
out through violet to a pale ground, and everything in the stage section --
line, tabs, ruler, panel -- is restated for that ground. The art surface
was already light, so it stops being the one bright thing on a dark page
and becomes part of a light one.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- the last leg goes up, not further down --------------------------------
old = """               [2.5, [26, 14, 56]], [3, [42, 22, 89]]];"""
new = """               [2.5, [72, 58, 134]], [3, [239, 234, 255]]];"""
assert old in s, 'sky top ramp changed'
s = s.replace(old, new, 1)

old = """                [2.5, [10, 5, 24]], [3, [20, 10, 46]]];"""
new = """                [2.5, [54, 40, 108]], [3, [255, 255, 255]]];"""
assert old in s, 'sky foot ramp changed'
s = s.replace(old, new, 1)

old = """      // it darkens once now and never comes back up
      var lit = Math.min(1, t);"""
new = """      // dark from the chat through the windows, then light again for the stages
      var lit = t <= 1 ? t : (t <= 2 ? 1 : Math.max(0, 3 - t));"""
assert old in s, 'glass alpha helper changed'
s = s.replace(old, new, 1)

old = "        head.classList.toggle('is-night', t > 0.5);"
new = "        head.classList.toggle('is-night', t > 0.5 && t < 2.6);"
assert old in s, 'header night toggle changed'
s = s.replace(old, new, 1)

# ---- the section, restated for a pale ground -------------------------------
subs = [
    ("""    .rec-stage-top { margin:0; text-align:center; color:#FFFFFF;""",
     """    .rec-stage-top { margin:0; text-align:center; color:#191231;"""),

    ("""    .rec-stage-top span { color:#8D83B8; }""",
     """    .rec-stage-top span { color:#8F86AE; }"""),

    ("""                     border:none; background:none; padding:4px 2px; color:#8D83B8;
                     transition:color .2s; }""",
     """                     border:none; background:none; padding:4px 2px; color:#6E6690;
                     transition:color .2s; }"""),

    ("""    .rec-stage-tab svg { width:16px; height:16px; flex:none; opacity:.75; }
    .rec-stage-tab:hover { color:#D8D1F2; }
    .rec-stage-tab.is-on { color:#FFFFFF; font-weight:600; }
    .rec-stage-tab.is-on svg { opacity:1; color:#C9B8FF; }""",
     """    .rec-stage-tab svg { width:16px; height:16px; flex:none; opacity:.7; }
    .rec-stage-tab:hover { color:#3B3263; }
    .rec-stage-tab.is-on { color:#191231; font-weight:600; }
    .rec-stage-tab.is-on svg { opacity:1; color:#7C5CF6; }"""),

    ("""                       background-image:repeating-linear-gradient(90deg,
                         rgba(255,255,255,.17) 0 1px, transparent 1px 12px);""",
     """                       background-image:repeating-linear-gradient(90deg,
                         rgba(25,18,49,.20) 0 1px, transparent 1px 12px);"""),

    ("""                      left:var(--mark, 4%); background:#FFFFFF; border-radius:2px;""",
     """                      left:var(--mark, 4%); background:#191231; border-radius:2px;"""),

    ("""                            background:rgba(255,255,255,.035);
                            box-shadow:inset 0 0 0 1px rgba(255,255,255,.11); }""",
     """                            background:#FFFFFF;
                            box-shadow:inset 0 0 0 1px rgba(25,18,49,.10),
                                       0 26px 60px rgba(60,40,120,.10); }"""),

    ("""    .rec-stage-h { margin:0; max-width:15ch; color:#FFFFFF;""",
     """    .rec-stage-h { margin:0; max-width:15ch; color:#191231;"""),

    ("""    .rec-stage-p { margin:0; max-width:40ch; color:#A79FC8;""",
     """    .rec-stage-p { margin:0; max-width:40ch; color:#5F5880;"""),
]
for old, new in subs:
    assert old in s, 'rule changed: ' + old.strip().split('{')[0]
    s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('the stages run light')
