# -*- coding: utf-8 -*-
"""Claude says who and where. The rest gets looked up.

About, Size and Based were descriptions, and descriptions are what the
search is for. What is left is the four facts only the person's own Claude
reliably has: which company, its domain, their name, their role.

Website stays because it is an identifier rather than a description, and
because it is the key the logo lookup turns -- with the domain the card has
a real logo today, with only a company name it would have nothing until
something does the searching.

The parser and the card still understand about/size/based. Nothing asks for
them now, but the day a lookup fills them in they render without a change
here.
"""
import io
import sys

OLD = """    // seven lines, because the page has to read this back
    var PROMPT = [
      'I am briefing a role to Wisemonk\\'s AI recruiter, Mira. Give it the ' +
        'basics about my company and about me.',
      '',
      'Reply with exactly these seven lines and nothing else:',
      '',
      'Company:',
      'Website:',
      'About:',
      'Size:',
      'Based:',
      'Name:',
      'Role:',
      '',
      'Website is the domain on its own, like example.com. About is one or ' +
        'two sentences on what the company does and who it sells to. Size is ' +
        'roughly how many people work there. Based is where the team works ' +
        'from. Name and Role are mine.',
      '',
      'Use what you already know. If you are unsure of the website, look it ' +
        'up rather than guessing. Leave a value empty if you do not know it ' +
        'and cannot find it.',
      '',
      'No preamble, no extra lines, no questions.'
    ].join('\\n');"""

NEW = """    // four lines: who they are and which company. The rest is looked up.
    var PROMPT = [
      'I am briefing a role to Wisemonk\\'s AI recruiter, Mira. Tell it who I ' +
        'am and which company I work for.',
      '',
      'Reply with exactly these four lines and nothing else:',
      '',
      'Company:',
      'Website:',
      'Name:',
      'Role:',
      '',
      'Website is the company domain on its own, like example.com. Name and ' +
        'Role are mine.',
      '',
      'Use what you already know, and leave a value empty if you do not know ' +
        'it. Do not describe the company \\u2014 the name and the domain are ' +
        'all that is wanted.',
      '',
      'No preamble, no extra lines, no questions.'
    ].join('\\n');"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, s.count(OLD))
    s = s.replace(OLD, NEW, 1)
    cut = s[s.index('var PROMPT'):s.index(".join('\\n');")]
    for gone in ("'About:'", "'Size:'", "'Based:'"):
        assert gone not in cut, path + ': prompt still asks for ' + gone
    # the card keeps the ability to show them
    assert 'rec-co-about' in s, path + ': the card lost its about block'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
