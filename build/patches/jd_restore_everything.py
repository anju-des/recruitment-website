# -*- coding: utf-8 -*-
"""A refresh brings back the screen, and all of the panel.

Two things were wrong, both of them the record being behind what the
screen had grown into.

The middle came back empty. The restore was written when a refresh
landed you on a tucked-away flow with the cards in the rail, which was
fine when the last thing you had seen was a company card. The last
thing you have seen now is a screen you were editing, so it opens that
screen.

And the panel came back with only its rounds, because rounds were the
only part of the role the record kept. It keeps the whole of it now --
the questions, the pay and what it was read from, the team, which tab
was showing -- along with the job description itself, so every section
is still there and the tab still works.

The one thing that cannot survive is the file: a File is not JSON, so
"Open the original" is gone after a refresh. The text it was read from
is kept, which is what every other part of this screen was built out of
anyway, and the link simply is not offered rather than offered broken.
"""
import io
import sys

EDITS = [
    # the record keeps the whole role, and the document
    ("""          people: company.people || '', rounds: role.rounds,
          screens: kept""",
     """          people: company.people || '',
          // the whole of it: a panel that comes back with one section is
          // worse than one that comes back empty
          rs: role, jd: jd, jd_name: jd_name,
          screens: kept"""),

    # and the restore puts all of it back
    ("""      if (was.rounds) role.rounds = was.rounds;
      if (was.role) role.title = String(was.role).split(',')[0].trim();
      rail_draw();
      at_step(last, true);""",
     """      if (was.jd) { jd = was.jd; jd_name = was.jd_name || ''; }
      if (was.rs) {
        for (var key in was.rs) {
          if (Object.prototype.hasOwnProperty.call(was.rs, key)) {
            role[key] = was.rs[key];
          }
        }
      }
      // the file itself is not JSON, so there is no original to open
      jd_file = null;
      jd_url = '';
      if (!role.title) role.title = String(was.role || '').split(',')[0].trim();
      rail_draw();
      at_step(last, true);
      // the last thing seen was a screen being edited, not a tucked rail
      if (screens[2]) {
        kept[2] = role_html();
        show_details(2, true);
      }"""),

    # a restored screen has no file behind it
    ("""      var link = '';
      if (jd_file) {""",
     """      var link = '';
      if (jd_file) {   // a refresh leaves the text without the file"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rs: role' not in s, path + ': already keeps all of it'

    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    assert 'rounds: role.rounds,' not in s, path + ': the old field survives'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
