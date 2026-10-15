# -*- coding: utf-8 -*-
"""Two things only: the company, and the person asking.

The prompt was also fishing for the team, the stack and how they hire. It
asks for the company and the user now, and says so twice -- "these two
things only" and "only what you already know" -- because a model handed a
list will happily fill in a fifth item nobody asked for.

The panel follows it down. It was promising briefs written "at your levels
and your bar" from a prompt that no longer asks about levels or bars, and
offering to let people "choose what Mira can see and disconnect at any
time" for a connection that does not exist: this is one chat, one paste,
nothing held. Saying that plainly is both truer and more reassuring than a
consent line for a thing with no state.

The copy block is spliced between two anchors rather than matched whole --
the file carries real em-dashes and curly quotes where the patch that wrote
it used escapes, so an exact match of the old text is not reliable.
"""
import io
import sys

OLD_PROMPT = """    var PROMPT = [
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

NEW_PROMPT = """    var PROMPT = [
      'I am briefing a role to Wisemonk\\'s AI recruiter, Mira, and it works ' +
        'better when it knows who it is hiring for.',
      '',
      'Write me a short profile I can paste in \\u2014 around 120 words, plain ' +
        'prose, no headings or bullet points. Cover these two things only, ' +
        'and only what you already know:',
      '',
      '- the company: what we do, what we sell and who we sell it to, roughly ' +
        'how big we are, and where the team works from',
      '- me: my name, my role, and what I am responsible for here',
      '',
      'Nothing else \\u2014 no hiring advice, no role description, no ' +
        'suggestions.',
      '',
      'Do not guess. If you do not know something, leave it out and ask me ' +
        'instead.'
    ].join('\\n');"""

OPEN = "'<h2>Connect your Claude</h2>' +\n"
SHUT = "          '</ul>' +\n"

NEW_COPY = u"""          '<p>Your Claude already knows your company — what you build, ' +
            'who buys it, how big the team is, where everyone sits. Bring ' +
            'that across and Mira writes the role for your company instead ' +
            'of for a job title.</p>' +
          '<p>Nothing is connected and nothing is stored. Claude writes it, ' +
            'you read it, and you decide what to paste.</p>' +
          '<ul class="rec-cxp-gains">' +
            '<li><b>A role that sounds like you.</b> The brief carries what ' +
              'your company actually does, not a template’s version of ' +
              'it.</li>' +
            '<li><b>Fewer questions back.</b> Mira stops asking what it could ' +
              'have read — what you build, how big you are, where the ' +
              'team works.</li>' +
            '<li><b>Candidates get the real pitch.</b> Your company goes out ' +
              'with the role, in your words.</li>' +
"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()

    assert s.count(OLD_PROMPT) == 1, (path, 'prompt', s.count(OLD_PROMPT))
    s = s.replace(OLD_PROMPT, NEW_PROMPT, 1)

    assert s.count(OPEN) == 1, (path, 'heading anchor', s.count(OPEN))
    a = s.index(OPEN) + len(OPEN)
    assert s.count(SHUT, a) >= 1, path + ': no list close after the heading'
    b = s.index(SHUT, a)
    s = s[:a] + NEW_COPY + s[b:]

    cut = s[s.index('var PROMPT'):s.index("].join('\\n');")]
    for gone in ('the stack', 'levels', 'last search'):
        assert gone not in cut, path + ': prompt still asks for ' + gone
    assert 'disconnect it at any' not in s, path + ': old consent line left'
    assert 'your levels' not in s, path + ': old bullet left'

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
