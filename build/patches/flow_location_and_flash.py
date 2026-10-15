# -*- coding: utf-8 -*-
"""Location gets its country, and the empty screen stops crying failure.

Headquarters (P159) was already being read -- "Bengaluru", "San
Francisco". Country (P17) is now read with it and the two are shown as
one place, "Bengaluru, India", because a city and its country are one
answer to "where are they", not two facts. Deduped, so a city-state does
not come back as "Singapore, Singapore". A company with only a country
on record now gets a location where it used to get none.

Separately: the empty screen and the finished-with-nothing screen were
the same state -- no about, no facts, nothing in progress -- so the
company card appeared carrying "No public record to read from" a second
before the first fetch started. A flag set in rest() tells them apart.
"""
import io
import sys

EDITS = [
    ("""        var busy = '';""",
     """        var busy = '';
        var finished = false;"""),

    ("""            (!busy && !got.about && !(got.facts && got.facts.length)""",
     """            (finished && !got.about && !(got.facts && got.facts.length)"""),

    ("""        function rest() {
          busy = '';""",
     """        function rest() {
          busy = '';
          finished = true;"""),

    # country rides along with the headquarters
    ("""          ['P452', 'P159'].forEach(function (p) {""",
     """          ['P452', 'P159', 'P17'].forEach(function (p) {"""),

    ("""              var all = (d && d.entities) || {};
              refs.forEach(function (r) {
                var l = all[r.id] && all[r.id].labels && all[r.id].labels.en;
                if (l) {
                  got.facts.push([r.p === 'P452' ? 'Industry' : 'Based',
                                  l.value]);
                }
              });
              rest();""",
     """              var all = (d && d.entities) || {};
              var by = {};
              refs.forEach(function (r) {
                var l = all[r.id] && all[r.id].labels && all[r.id].labels.en;
                if (l) by[r.p] = l.value;
              });
              if (by.P452) got.facts.push(['Industry', by.P452]);
              // the city and its country are one answer, not two facts
              var where = [by.P159, by.P17].filter(function (v, i, a) {
                return v && a.indexOf(v) === i;
              });
              if (where.length) got.facts.push(['Based', where.join(', ')]);
              rest();"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    js = s[s.rindex('<script>'):]
    assert "'P17'" in js, path + ': country is not asked for'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
