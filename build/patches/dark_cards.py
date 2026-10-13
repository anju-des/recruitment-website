# -*- coding: utf-8 -*-
"""No light panels left inside the black windows.

The applicant card and the slot tiles were written when those two windows
were on the light base; carrying the dark modifier now, they kept painting
white strips inside a black card. Both get the dark reading the rest of the
window already had.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

anchor = "    .rec-win--dark .rec-ask-tools { color:#AEB6C8; }\n"
assert anchor in s, 'dark block tail changed'

DARK = anchor + """
    /* the applicant card: a lifted surface, not a white one */
    .rec-win--dark .rec-who { background:rgba(255,255,255,.04); }
    .rec-win--dark .rec-who-pic { color:#E7DEFF;
                                  background:linear-gradient(140deg,
                                    rgba(167,139,250,.40), rgba(124,92,246,.26)); }
    .rec-win--dark .rec-who-id b { color:#F2F3F8; }
    .rec-win--dark .rec-who-id i { color:#8E97AE; }
    .rec-win--dark .rec-who-fit { color:#C9B8FF; background:rgba(167,139,250,.16);
                                  box-shadow:inset 0 0 0 1px rgba(201,184,255,.24); }
    .rec-win--dark .rec-skills { box-shadow:inset 0 1px 0 rgba(255,255,255,.06); }
    .rec-win--dark .rec-skills span { color:#D5CDF0; background:rgba(255,255,255,.08);
                                      box-shadow:inset 0 0 0 1px rgba(255,255,255,.08); }

    /* the slot tiles, same story */
    .rec-win--dark .rec-slot { box-shadow:inset 0 0 0 1px rgba(255,255,255,.12); }
    .rec-win--dark .rec-slot b { color:#F2F3F8; }
    .rec-win--dark .rec-slot i { color:#8E97AE; }
    .rec-win--dark .rec-slot.is-pick { background:rgba(167,139,250,.18);
                                       box-shadow:inset 0 0 0 1.5px #A78BFA; }
    .rec-win--dark .rec-slot.is-pick b,
    .rec-win--dark .rec-slot.is-pick i { color:#E7DEFF; }
    .rec-win--dark .rec-meet { color:#8E97AE;
                               box-shadow:inset 0 1px 0 rgba(255,255,255,.06); }
"""
s = s.replace(anchor, DARK, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('no white panels in the black windows')
