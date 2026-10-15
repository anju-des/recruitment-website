# -*- coding: utf-8 -*-
"""Budget, skills and the publish screen all go.

What is left is the website and its lookup, then the account, then the
tick: the brief is one question and what Mira finds from it.

Removed outright: the two step definitions, review() and the title()
helper only it used, and money()/said()/rail() with the band they read,
which existed for the budget rail. Routing moves down one -- the slot
that held the review now holds the account screen, and go() finishes
from there.

Kept on purpose: the chip and tag machinery in ask(), ready() and
wire(), and brief.skills with it. Those paths are generic, no step
reaches them now, and cutting them would be a rewrite of the step
renderer rather than the removal of two questions. Same for the rail and
chip rules in the stylesheet, which change nothing on screen.
"""
import io
import sys

EDITS = [
    ("""      { key: 'salary',
        q: 'What is the budget?',
        range: { min: 20, max: 300, step: 5 } },
""", ""),

    ("""      { key: 'skills',
        q: 'What must they be good at?',
        chipsOnly: true,
        multi: true,
        chips: ['Python', 'Django', 'Go', 'Node.js', 'TypeScript', 'React', 'PostgreSQL', 'AWS', 'Kubernetes', 'System design', 'Figma', 'Design systems', 'User research', 'Product strategy', 'SQL', 'Machine learning'] }
""", ""),

    ("""    var brief = { role: '', website: '', salary: '', skills: [] };
    var band = { from: 90, to: 120 };   // thousands a year""",
     """    var brief = { role: '', website: '', skills: [] };"""),

    ("""      brief.website = '';
      brief.salary = '';
      brief.skills = [];""",
     """      brief.website = '';
      brief.skills = [];"""),

    ("""      card.innerHTML = at < STEPS.length ? ask(STEPS[at])
                     : at === STEPS.length ? review() : signup();""",
     """      card.innerHTML = at < STEPS.length ? ask(STEPS[at]) : signup();"""),

    ("""        if (at < STEPS.length) {
          if (step.range) brief[step.key] = said(step.range);
          else if (step.multi) { /* already in brief.skills */ }
          else if (!step.tags && input) {
            brief[step.key] = step.tidy ? step.tidy(input.value)
                                        : input.value.trim();
          }
        }
        if (at > STEPS.length) { done(); return; }""",
     """        if (at < STEPS.length && !step.multi && !step.tags && input) {
          brief[step.key] = step.tidy ? step.tidy(input.value)
                                      : input.value.trim();
        }
        if (at >= STEPS.length) { done(); return; }"""),

    # ready() asked the rail for a value that no longer exists
    ("""        var has = step.range ? true
                :""", """        var has ="""),
]

# whole functions nothing calls now, cut between their own anchors
CUTS = [
    ("    function money(n, top) {", "    // The title, not the sentence:"),
    ("    // The title, not the sentence:", "    function signup() {"),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    for start, stop in CUTS:
        a = s.index(start)
        b = s.index(stop, a + len(start))
        s = s[:a] + s[b:]

    for gone in ('function review(', 'function rail(', 'function money(',
                 'function said(', 'function title(', 'brief.salary',
                 'What is the budget'):
        assert gone not in s, path + ': ' + gone + ' survives'
    for kept in ('function signup(', 'function done(', 'function look('):
        assert kept in s, path + ': ' + kept + ' went too'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
