# -*- coding: utf-8 -*-
"""The brief asks for the company website first.

It goes first because it is the only question about the company rather
than the role, and because it is the one answer everything else can be
looked up from.

Two small general additions rather than a special case for this step:

* `looks` -- a pattern the answer has to match before Continue lights up.
  Length alone would accept "yes", and a website that is not a website is
  worth nothing to a lookup.
* `tidy` -- run over the answer on the way into the brief, so
  "https://www.example.com/careers/" is stored and shown as
  "example.com/careers".

Both are optional and the other three steps are untouched.
"""
import io
import sys

EDITS = [
    # the question itself, ahead of the role questions
    ("""    var STEPS = [
      { key: 'location',""",
     """    var STEPS = [
      { key: 'website',
        q: 'What is your company website?',
        placeholder: 'yourcompany.com',
        looks: /[a-z0-9][a-z0-9-]*\\.[a-z]{2,}/i,
        tidy: function (v) {
          return String(v).trim()
            .replace(/^https?:\\/\\//i, '').replace(/^www\\./i, '')
            .replace(/\\/+$/, '');
        } },
      { key: 'location',"""),

    ("""    var brief = { role: '', location: '', salary: '', skills: [] };""",
     """    var brief = { role: '', website: '', location: '', salary: '',
                  skills: [] };"""),

    ("""      brief.role = field.value.trim();
      brief.location = '';""",
     """      brief.role = field.value.trim();
      brief.website = '';
      brief.location = '';"""),

    # Continue waits for something that could actually be a website
    ("""                : (input ? input.value.trim().length > 0
                         : !!brief[step.key]);""",
     """                : (input ? (step.looks
                              ? step.looks.test(input.value.trim())
                              : input.value.trim().length > 0)
                         : !!brief[step.key]);"""),

    ("""          else if (!step.tags && input) brief[step.key] = input.value.trim();""",
     """          else if (!step.tags && input) {
            brief[step.key] = step.tidy ? step.tidy(input.value)
                                        : input.value.trim();
          }"""),

    ("""      var facts = [
        ['Where', brief.location],""",
     """      var facts = [
        ['Website', brief.website],
        ['Where', brief.location],"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert "key: 'website'" not in s, path + ': already asks'
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
