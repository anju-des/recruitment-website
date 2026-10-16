# -*- coding: utf-8 -*-
"""Three things the first run of the parser got wrong.

The hiring sentence ran on, so "a Content Writer to join our marketing
team in Pune" became the title. A title stops where the sentence starts
doing something else.

Two locations were missed: the location line a job board puts under the
title, and the "in Pune" at the end of that same hiring sentence.

And "Create prototypes" is prototyping, which a literal phrase list does
not know.
"""
import io

p = 'jd-parse.js'
s = io.open(p, encoding='utf-8').read()


def sub(old, new):
    global s
    assert s.count(old) == 1, (old[:60], s.count(old))
    s = s.replace(old, new, 1)


sub("""  function clean_title(s) {
    return tidy(s)
      .replace(/^(?:a|an)\\s+/i, '')""",
    """  function clean_title(s) {
    return tidy(s)
      // "Content Writer to join our marketing team in Pune" is a sentence
      // with a title at the front of it
      .replace(/\\s+(?:to|for|who|that|with|in|at|based|joining|reporting)\\s+.*$/i, '')
      .replace(/^(?:a|an)\\s+/i, '')""")

sub("""  function place(text) {
    var said = first(text, [""",
    """  function place(text, ls) {
    // "Bengaluru, Karnataka, India - Remote" near the top is a location
    // line, which is how a job board writes one
    for (var i = 0; ls && i < Math.min(ls.length, 6); i++) {
      var l = tidy(ls[i])
        .replace(/\\s*[-\\u2013\\u2014|]\\s*(?:remote|hybrid|on-?site).*$/i, '');
      if (l.length <= 60 && l.split(',').length >= 2 &&
          /^[A-Z][A-Za-z.'-]+(?:\\s+[A-Z][A-Za-z.'-]+)?(?:\\s*,\\s*[A-Z][A-Za-z.'-]+(?:\\s+[A-Z][A-Za-z.'-]+)?){1,3}$/.test(l)) {
        return tidy(l.split(',')[0]);
      }
    }

    var said = first(text, [""")

sub("""      /\\boffice\\s+is\\s+(?:conveniently\\s+)?located\\s+at\\s+([^.\\n]{4,80})/im
    ]);""",
    """      /\\boffice\\s+is\\s+(?:conveniently\\s+)?located\\s+at\\s+([^.\\n]{4,80})/im,
      // "...to join our marketing team in Pune."
      /\\b(?:join|team|role|position|office)\\b[^.\\n]{0,40}?\\bin\\s+([A-Z][a-z]{2,}(?:\\s+[A-Z][a-z]+){0,2})\\b/m
    ]);""")

sub("      place: place(flat),", "      place: place(flat, ls),")

sub("    'design systems', 'user research', 'prototyping', 'wireframing',",
    "    'design systems', 'user research', 'prototyp(?:e|es|ing)', 'wireframing',")

sub("""      if (new RegExp('\\\\b' + p.replace(/\\//g, '\\\\/') + '\\\\b', 'i').test(text)) {
        add(p.replace(/^./, function (c) { return c.toUpperCase(); }));
      }""",
    """      if (new RegExp('\\\\b' + p.replace(/\\//g, '\\\\/') + '\\\\b', 'i').test(text)) {
        // the pattern is not the name: "prototyp(?:e|es|ing)" is "Prototyping"
        add(p.replace(/\\(\\?:[^)]*\\)/, 'ing')
             .replace(/^./, function (c) { return c.toUpperCase(); }));
      }""")

io.open(p, 'w', encoding='utf-8').write(s)
print('parser updated')
