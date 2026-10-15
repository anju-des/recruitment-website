# -*- coding: utf-8 -*-
"""Two fixes: a shadowed name, and suggestions that are companies.

The restore declared `var kept` for the raw JSON string, shadowing the
flow's `kept` map of screens. So `kept[2] = screens[2]` set a property
on a string and vanished without a word, and the Account row came back
clickable with nothing behind it. The chips survived only because
put_mini assigns from outside that scope. The local is `raw` now.

And the suggestions were offering Australia and Stribro for "stri".
Wikidata will match anything with an official website, and a country
has one. A company is better identified by what it carries: an industry
(P452), a legal name (P1448), or an entry in a company directory
(Crunchbase P2088, LinkedIn P4264). Anything with none of those is not
what this field is asking for.

Also quicker: 200ms after the last keystroke instead of 320, and five
candidates instead of six.
"""
import io
import sys

EDITS = [
    ("""      var kept;
      try { kept = window.sessionStorage.getItem('wm-flow'); } catch (e) { return; }
      if (!kept) return;
      var was;
      try { was = JSON.parse(kept); } catch (e) { return; }""",
     """      // not `kept`: that name holds the map of screens one scope out
      var raw;
      try { raw = window.sessionStorage.getItem('wm-flow'); } catch (e) { return; }
      if (!raw) return;
      var was;
      try { was = JSON.parse(raw); } catch (e) { return; }"""),

    # only offer things that look like companies
    ("""                    var c = ent.claims || {};
                    var w = c.P856 && c.P856[0].mainsnak.datavalue;
                    if (!w) return;          // no domain, nothing to offer""",
     """                    var c = ent.claims || {};
                    var w = c.P856 && c.P856[0].mainsnak.datavalue;
                    if (!w) return;          // no domain, nothing to offer
                    // a country has a website too: ask for something only a
                    // company carries
                    if (!(c.P452 || c.P1448 || c.P2088 || c.P4264)) return;"""),

    ("""          hold = window.setTimeout(function () { search(q); }, 320);""",
     """          hold = window.setTimeout(function () { search(q); }, 200);"""),

    ("""          window.fetch(WD + 'action=wbsearchentities&type=item&limit=6' +""",
     """          window.fetch(WD + 'action=wbsearchentities&type=item&limit=5' +"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    js = s[s.rindex('<script>'):]
    assert 'var kept;' not in js, path + ': the shadow survives'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
