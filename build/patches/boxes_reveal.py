# -*- coding: utf-8 -*-
"""The boxes wait until the statement is in view, then fade in one after
another.

They were visible from the moment the section entered the screen -- drifting
around on the violet, a long way above the text they belong to. Now they are
tied to the same moment the statement is, so they arrive with it and read as
one group.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """    .rec-box { position:absolute; margin:-55px 0 0 -75px; width:150px; height:110px;
               border-radius:16px; background:rgba(255,255,255,0.045);
               border:1px solid rgba(255,255,255,0.075);
               -webkit-backdrop-filter:blur(6px); backdrop-filter:blur(6px);
               animation:rec-box-float 9s ease-in-out infinite; }
    /* depth: the far ones are softer, dimmer and a touch smaller */
    .rec-box--d1 { opacity:.7; filter:blur(2px); transform:scale(.94);
                   animation-duration:11s; animation-delay:-3s; }
    .rec-box--d2 { opacity:.45; filter:blur(4px); transform:scale(.88);
                   animation-duration:13s; animation-delay:-6s; }"""
new = """    .rec-box { position:absolute; margin:-55px 0 0 -75px; width:150px; height:110px;
               border-radius:16px; background:rgba(255,255,255,0.045);
               border:1px solid rgba(255,255,255,0.075);
               -webkit-backdrop-filter:blur(6px); backdrop-filter:blur(6px);
               animation:rec-box-float 9s ease-in-out infinite;
               opacity:0; transition:opacity .9s ease; }
    /* depth: the far ones are softer, dimmer and a touch smaller */
    .rec-box--d1 { filter:blur(2px); transform:scale(.94);
                   animation-duration:11s; animation-delay:-3s; }
    .rec-box--d2 { filter:blur(4px); transform:scale(.88);
                   animation-duration:13s; animation-delay:-6s; }
    /* they arrive with the statement, a beat apart, each to its own depth */
    .rec-next.is-in .rec-box { opacity:1; }
    .rec-next.is-in .rec-box--d1 { opacity:.7; }
    .rec-next.is-in .rec-box--d2 { opacity:.45; }
    .rec-next.is-in .rec-box:nth-child(2) { transition-delay:.08s; }
    .rec-next.is-in .rec-box:nth-child(3) { transition-delay:.16s; }
    .rec-next.is-in .rec-box:nth-child(4) { transition-delay:.24s; }
    .rec-next.is-in .rec-box:nth-child(5) { transition-delay:.32s; }
    .rec-next.is-in .rec-box:nth-child(6) { transition-delay:.40s; }
    .rec-next.is-in .rec-box:nth-child(7) { transition-delay:.48s; }
    .rec-next.is-in .rec-box:nth-child(8) { transition-delay:.56s; }"""
assert old in s, 'box css changed'
s = s.replace(old, new, 1)

old = """        if (e.intersectionRatio >= 0.95) say.classList.add('rec-in');
        else if (!e.isIntersecting) say.classList.remove('rec-in');"""
new = """        var section = say.closest('.rec-next');
        if (e.intersectionRatio >= 0.95) {
          say.classList.add('rec-in');
          if (section) section.classList.add('is-in');
        } else if (!e.isIntersecting) {
          say.classList.remove('rec-in');
          if (section) section.classList.remove('is-in');
        }"""
assert old in s, 'statement observer changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('boxes arrive with the statement')
