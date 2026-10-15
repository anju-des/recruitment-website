# -*- coding: utf-8 -*-
"""Paragraphs, not a hard-wrapped column.

The array was one source line per visual line, so every newline in it
landed in their Claude as a real newline and the prompt arrived wrapped
mid-sentence. Each paragraph is one string now; only the blank lines and
the four bullets break.
"""
import io
import sys

OLD = """    var PROMPT = [
      'I am briefing a role to Wisemonk\\'s AI recruiter, Mira, and it works',
      'better when it knows how we hire.',
      '',
      'Write me a short hiring profile I can paste in \\u2014 around 150 words,',
      'plain prose, no headings or bullet points. Cover what you already know',
      'about:',
      '',
      '- the company: what we do, roughly how big we are, where the team works',
      '- the team this hire would join, and the stack they would work in',
      '- how we hire: the levels we use, what we hold the bar on, what the',
      '  last search got wrong',
      '- me: my name and what I do here',
      '',
      'Do not guess. If you do not know something, leave it out and ask me',
      'instead.'
    ].join('\\n');"""

NEW = """    var PROMPT = [
      'I am briefing a role to Wisemonk\\'s AI recruiter, Mira, and it works ' +
        'better when it knows how we hire.',
      '',
      'Write me a short hiring profile I can paste in \\u2014 around 150 words, ' +
        'plain prose, no headings or bullet points. Cover what you already ' +
        'know about:',
      '',
      '- the company: what we do, roughly how big we are, where the team works',
      '- the team this hire would join, and the stack they would work in',
      '- how we hire: the levels we use, what we hold the bar on, what the ' +
        'last search got wrong',
      '- me: my name and what I do here',
      '',
      'Do not guess. If you do not know something, leave it out and ask me ' +
        'instead.'
    ].join('\\n');"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, s.count(OLD))
    s = s.replace(OLD, NEW, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
