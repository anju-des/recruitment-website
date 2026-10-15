# -*- coding: utf-8 -*-
"""No word count.

"around 120 words" was capping an answer whose useful length depends on how
much their Claude actually knows. "Short" goes with the number -- half a
restriction is still a restriction. The shape constraints stay: prose, no
headings, two subjects, nothing invented.
"""
import io
import sys

OLD = """      'Write me a short profile I can paste in \\u2014 around 120 words, plain ' +
        'prose, no headings or bullet points. Cover these two things only, ' +
        'and only what you already know:',"""

NEW = """      'Write me a profile I can paste in \\u2014 plain prose, no headings or ' +
        'bullet points. Cover these two things only, and only what you ' +
        'already know:',"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, s.count(OLD))
    s = s.replace(OLD, NEW, 1)
    cut = s[s.index('var PROMPT'):s.index("].join('\\n');")]
    assert '120' not in cut and 'short' not in cut, path + ': a cap survives'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
