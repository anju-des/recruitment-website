# -*- coding: utf-8 -*-
"""A PDF breaks a sentence wherever the column ended.

"Own the journey: From user flows to polished UI, ensuring every
touchpoint feels" and "seamless." are one bullet in the document and
two lines in the extraction. Left as they are, the second is a
responsibility nine characters long and a question gets built out of
it: "This role asks you to seamless."

A line that starts lowercase is the end of the line above it. That is
not always true -- but a lowercase line is never the start of a heading
or a bullet, which is all this parser reads lines for.
"""
import io

p = 'jd-parse.js'
s = io.open(p, encoding='utf-8').read()

# the file stores those regexes as real characters, not as \\u escapes, so
# both anchors here avoid escaped text entirely
EDITS = [
    ("""  function lines(text) {
    return String(text || '')""",
     """  function lines(text) {
    var out = String(text || '')"""),

    ("""      .filter(function (l) { return l.length > 0; });
  }""",
     """      .filter(function (l) { return l.length > 0; });
    return knit(out);
  }

  // a PDF breaks a sentence wherever the column ended. A line starting
  // lowercase is the end of the one above it -- it is never the start of
  // a heading or a bullet, which is all lines are read for here.
  function knit(rows) {
    var out = [];
    for (var i = 0; i < rows.length; i++) {
      if (out.length && /^[a-z]/.test(rows[i]) &&
          !/[.:;!?]$/.test(out[out.length - 1])) {
        out[out.length - 1] += ' ' + rows[i];
      } else {
        out.push(rows[i]);
      }
    }
    return out;
  }"""),
]

for old, new in EDITS:
    assert s.count(old) == 1, (old[:40], s.count(old))
    s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('wrapped lines knitted')
