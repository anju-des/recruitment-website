# -*- coding: utf-8 -*-
"""The chip opens nothing after a refresh, and the chevron turns 90.

The bug is a record written by an older build. When the chip replaced
the details panel the saved record stopped carrying the rendered screen;
when the chip became a button it needed it again. A session that settled
in between has a record with a company but no screen, so the restore
brings back a chip whose only job is to open something that is not
there.

Two guards, because either alone leaves a hole: a restore now refuses a
record without a screen and clears it, so the flow starts clean rather
than restoring something broken; and the toggle will not open an empty
body whatever the record says.

The chevron points right and turns ninety degrees to point down, which
is the usual way round for a disclosure and the way asked for. It was
pointing down and turning a full half turn to point back up, which
reads as a flip rather than an opening.
"""
import io
import sys

EDITS = [
    ("""    function show_details(on) {
      var face = flow.querySelector('.rec-flow-card');""",
     """    function show_details(on) {
      // an older record can name a company without carrying its screen
      if (on && !kept_html) return;
      var face = flow.querySelector('.rec-flow-card');"""),

    ("""      if (!was || !was.who) return;""",
     """      // a record from a build that did not keep the screen cannot be
      // reopened, so it is not worth restoring
      if (!was || !was.who || !was.html) {
        try { window.sessionStorage.removeItem('wm-flow'); } catch (e) {}
        return;
      }"""),

    # a disclosure chevron points at where it will go
    ("""            '<path d="M6 9.5l6 6 6-6"/></svg>' +""",
     """            '<path d="M9 6l6 6-6 6"/></svg>' +"""),
]

OLD_CSS = """    .rec-flow:not(.is-found) .rec-done-go { transform:rotate(180deg);
                                            color:#6B4BE8; }"""
NEW_CSS = """    .rec-flow:not(.is-found) .rec-done-go { transform:rotate(90deg);
                                            color:#6B4BE8; }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert s.count(OLD_CSS) == 1, (path, 'chevron css', s.count(OLD_CSS))
    s = s.replace(OLD_CSS, NEW_CSS, 1)
    js = s[s.rindex('<script>'):]
    assert 'rotate(180deg)' not in s[s.index('.rec-done-go'):
                                     s.index('.rec-step i')], \
        path + ': the half turn survives'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
