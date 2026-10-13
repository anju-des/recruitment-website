# -*- coding: utf-8 -*-
"""Keep the tiles clear of the copy and inside the panel.

Measured at 1009px: three tiles sat on top of the heading and the right-most
one hung 3px past the edge. Two changes fix both for good:

  * coordinates now mean the tile's CENTRE (negative margins of half its box),
    so a tile at 92% can't push its right edge out of the panel;
  * the field is inset 16px, and every centre is placed outside the corridor
    the copy occupies -- either in the top/bottom bands or hard to one side.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# label -> (centre x%, centre y%). The copy box is 560px wide and sits in the
# middle: a tile centre is only safe inside x 14-86% if it is also above 19%
# or below 81%.
MOVES = [
    ('left:8%; top:6%',   'left:10%; top:16%'),   # Gmail
    ('left:16%; top:34%', 'left:7%; top:48%'),    # Outlook   (far left)
    ('left:30%; top:66%', 'left:14%; top:84%'),   # Calendar  (bottom band)
    ('left:44%; top:2%',  'left:34%; top:14%'),   # Meet      (top band)
    ('left:58%; top:74%', 'left:46%; top:88%'),   # Slack     (bottom band)
    ('left:70%; top:28%', 'left:64%; top:13%'),   # Drive     (top band)
    ('left:80%; top:60%', 'left:72%; top:86%'),   # Fireflies (bottom band)
    ('left:88%; top:10%', 'left:92%; top:50%'),   # Zoho Sign (far right)
    ('left:50%; top:40%', 'left:89%; top:15%'),   # Claude MCP -- was dead
                                                  # centre, behind the text
]
for old, new in MOVES:
    assert s.count(old) == 1, 'tile coordinate not found once: ' + old
    s = s.replace(old, new, 1)

old = '    .rec-tiles { position:absolute; inset:0; }\n'
new = ('    /* inset, so a tile at the far edge still has room to breathe */\n'
       '    .rec-tiles { position:absolute; inset:16px; }\n')
assert old in s, 'tiles box rule changed'
s = s.replace(old, new, 1)

old = """    .rec-tile { position:absolute; display:flex; flex-direction:column; align-items:center;
                justify-content:center; gap:8px; width:124px; height:92px; border-radius:14px;"""
new = """    /* left/top are the tile's CENTRE: the negative margins pull the box back
       by half its size, which keeps percentage placement off the edges. */
    .rec-tile { position:absolute; margin:-46px 0 0 -62px;
                display:flex; flex-direction:column; align-items:center;
                justify-content:center; gap:8px; width:124px; height:92px; border-radius:14px;"""
assert old in s, 'tile rule changed'
s = s.replace(old, new, 1)

old = """      .rec-tile { position:static !important; left:auto !important; top:auto !important;
                  width:108px; height:84px; filter:none; opacity:1; transform:none;"""
new = """      .rec-tile { position:static !important; left:auto !important; top:auto !important;
                  margin:0; width:108px; height:84px; filter:none; opacity:1; transform:none;"""
assert old in s, 'responsive tile rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('tiles re-placed around the copy')
