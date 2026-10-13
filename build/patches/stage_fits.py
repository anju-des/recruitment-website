# -*- coding: utf-8 -*-
"""Make the pinned stage block fit a short screen, and clear the header.

On a wide, short viewport the block came out taller than the screen, so the
panel ran off the bottom, and because the whole thing is vertically centred
the line at the top slid under the sticky header. Every vertical measure in
it is now viewport-relative with a floor, and the top padding starts below
the header rather than at the top of the frame.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """                     /* the taller panel left the pinned frame with no slack;
                        this keeps it inside the screen on shorter ones too */
                     padding-block:clamp(44px, 7vh, 90px);"""
new = """                     /* the top clears the sticky header, since the block is
                        centred and would otherwise tuck the line under it */
                     padding-top:clamp(96px, 10vh, 124px);
                     padding-bottom:clamp(36px, 6vh, 90px);"""
assert old in s, 'pin padding changed'
s = s.replace(old, new, 1)

old = """    .rec-stage-rail { display:flex; justify-content:space-between; gap:10px;
                      margin-top:38px; }"""
new = """    .rec-stage-rail { display:flex; justify-content:space-between; gap:10px;
                      margin-top:clamp(22px, 3.2vh, 38px); }"""
assert old in s, 'rail rule changed'
s = s.replace(old, new, 1)

old = """    .rec-stage-ruler { position:relative; height:14px; margin-top:16px;"""
new = """    .rec-stage-ruler { position:relative; height:14px;
                       margin-top:clamp(10px, 1.8vh, 16px);"""
assert old in s, 'ruler rule changed'
s = s.replace(old, new, 1)

alt = """                            margin-top:28px; border-radius:22px; overflow:hidden;
                            min-height:min(548px, 60vh);"""
new = """                            margin-top:clamp(18px, 2.6vh, 28px);
                            border-radius:22px; overflow:hidden;
                            /* short screens get a shorter panel, so the block
                               as a whole still fits inside the pin */
                            min-height:min(548px, 52vh);"""
assert alt in s, 'pane rule changed'
s = s.replace(alt, new, 1)

old = """    .rec-stage-text { display:flex; flex-direction:column; justify-content:space-between;
                      gap:40px; padding:44px 42px; }"""
new = """    .rec-stage-text { display:flex; flex-direction:column; justify-content:space-between;
                      gap:clamp(18px, 3vh, 40px);
                      padding:clamp(26px, 4.4vh, 44px) clamp(26px, 2.6vw, 42px); }"""
assert old in s, 'text column rule changed'
s = s.replace(old, new, 1)

old = """      .rec-stage-pin { position:static; min-height:0; padding-block:0;
                       opacity:1; transform:none; }"""
new = """      .rec-stage-pin { position:static; min-height:0; padding:0;
                       opacity:1; transform:none; }"""
assert old in s, 'responsive pin rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('the block fits, and clears the header')
