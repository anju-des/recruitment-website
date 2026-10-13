# -*- coding: utf-8 -*-
"""Eight empty glass boxes floating around the statement.

Their coordinates are centres, not corners, so a box near an edge cannot
push itself out of the field. All eight sit outside the corridor the text
occupies: either well above/below it, or hard to one side.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# centre x%, centre y%, depth (0 = nearest)
BOXES = [
    (9, 14, 0), (26, 26, 1), (52, 12, 1), (74, 22, 2),
    (8, 62, 0), (30, 80, 2), (58, 86, 1), (84, 72, 0),
]
tiles = '\n'.join(
    '            <div class="rec-box rec-box--d%d" style="left:%d%%; top:%d%%"></div>'
    % (d, x, y) for x, y, d in BOXES)

old = """          <p class="rec-say">"""
new = """          <div class="rec-boxes" aria-hidden="true">
%s
          </div>
          <p class="rec-say">""" % tiles
assert old in s, 'statement markup changed'
s = s.replace(old, new, 1)

old = """    .rec-next { min-height:160vh; display:grid; place-items:center; }"""
new = """    .rec-next { position:relative; min-height:160vh; display:grid; place-items:center;
                overflow:hidden; }
    /* the field is centred on the same point as the text, so the boxes always
       sit around it whatever the screen size */
    .rec-boxes { position:absolute; left:50%; top:50%; translate:-50% -50%;
                 width:min(1200px, 92vw); height:620px; pointer-events:none; }
    /* left/top are each box's centre: the negative margins pull it back by
       half its size, which keeps percentage placement off the edges */
    .rec-box { position:absolute; margin:-55px 0 0 -75px; width:150px; height:110px;
               border-radius:16px; background:rgba(255,255,255,0.045);
               border:1px solid rgba(255,255,255,0.075);
               -webkit-backdrop-filter:blur(6px); backdrop-filter:blur(6px);
               animation:rec-box-float 9s ease-in-out infinite; }
    /* depth: the far ones are softer, dimmer and a touch smaller */
    .rec-box--d1 { opacity:.7; filter:blur(2px); transform:scale(.94);
                   animation-duration:11s; animation-delay:-3s; }
    .rec-box--d2 { opacity:.45; filter:blur(4px); transform:scale(.88);
                   animation-duration:13s; animation-delay:-6s; }
    @keyframes rec-box-float {
      0%, 100% { translate:0 0; }
      50%      { translate:0 -14px; }
    }
    @media (prefers-reduced-motion: reduce) { .rec-box { animation:none; } }
    .rec-say { position:relative; z-index:1; }"""
assert old in s, 'next section rule changed'
s = s.replace(old, new, 1)

old = """      .rec-say { font-size:24px; max-width:30ch; }"""
new = """      .rec-say { font-size:24px; max-width:30ch; }
      /* no room to float anything around the text at this width */
      .rec-boxes { display:none; }"""
assert old in s, 'responsive statement rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('eight glass boxes added')
