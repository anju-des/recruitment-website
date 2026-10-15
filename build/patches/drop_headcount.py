# -*- coding: utf-8 -*-
"""The LinkedIn headcount goes; the reader will not serve it.

It worked when it was built -- "View all 65 employees" off the public
page -- and now returns, on every attempt:

    403 AbuseAlleviationError
    "Anonymous access to domain www.linkedin..."

r.jina.ai refuses LinkedIn without authentication. Site reads still
return 200, so this is LinkedIn specifically, and it is the service
answering the question that was flagged when this went in rather than a
transient failure to retry around.

What is left behind without it is worse than nothing: a line that says
"counting the team on LinkedIn" on every lookup where Wikidata has no
figure, which is most of them, followed by no figure.

Companies Wikidata records employees for -- Stripe, 2,500 -- still show
People, because that was never this path.
"""
import io
import sys

EDITS = [
    ("""        var links = [];           // where else they are on the record
        var li_id = '';           // linkedin, for the headcount fallback""",
     """        var links = [];           // where else they are on the record"""),

    ("""          var li = one('P4264');
          if (typeof li === 'string') li_id = li;

          [['P4264', 'LinkedIn', 'https://www.linkedin.com/company/'],""",
     """          [['P4264', 'LinkedIn', 'https://www.linkedin.com/company/'],"""),

    ("""              if (where.length) vals.Based = where.join(', ');
              head_count();
            }, head_count);""",
     """              if (where.length) vals.Based = where.join(', ');
              lay_out();
            }, lay_out);"""),

    ("""        function read_more() {
          if (!refs.length) { head_count(); return; }""",
     """        function read_more() {
          if (!refs.length) { lay_out(); return; }"""),
]

CUT = ("""        // the register has no figure for plenty of companies; their own
        // LinkedIn page does
        function head_count() {""", """        function read_more() {""")


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    a = s.index(CUT[0])
    b = s.index(CUT[1], a)
    s = s[:a] + s[b:]

    js = s[s.rindex('<script>'):]
    for gone in ('head_count', 'counting the team', 'li_id'):
        assert gone not in js, path + ': ' + gone + ' survives'
    # the links row keeps its LinkedIn entry; only the scrape goes
    assert 'linkedin.com/company/' in js, path + ': the link went too'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
