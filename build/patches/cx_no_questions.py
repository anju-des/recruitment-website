# -*- coding: utf-8 -*-
"""The reply is the profile, and only the profile.

"ask me instead" was doing its job too well: the live run came back with a
good profile followed by "I left out a few things I don't know" and four
numbered questions, none of it pasteable. It also opened with "Here's the
profile, using only what I know:", so the whole reply needed editing before
it could go anywhere.

"Do not guess" stays -- that is the guard against an invented headcount
travelling into a brief. What goes is the invitation to come back with
questions, replaced by an instruction to leave gaps silently and send
nothing but the profile.
"""
import io
import sys

OLD = """      'Do not guess. If you do not know something, leave it out and ask me ' +
        'instead.'
    ].join('\\n');"""

NEW = """      'Do not guess. If you do not know something, just leave it out.',
      '',
      'Reply with the profile and nothing else: no preamble, no list of what ' +
        'you left out, and no questions back.'
    ].join('\\n');"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, s.count(OLD))
    s = s.replace(OLD, NEW, 1)
    cut = s[s.index('var PROMPT'):s.index("].join('\\n');")]
    assert 'ask me' not in cut, path + ': it still invites questions'
    assert 'Do not guess' in cut, path + ': the guard went with it'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
