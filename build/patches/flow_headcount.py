# -*- coding: utf-8 -*-
"""Headcount, when the register does not have it.

Wikidata records employees for Stripe and not for Wisemonk, which is why
one showed PEOPLE and the other did not. The company's LinkedIn page
does: "View all 65 employees", on the logged-out page, and the entity
already gave us the LinkedIn id.

It only runs when there is no figure already and there is an id to use,
so Stripe never triggers it.

The line names the source -- "counting the team on LinkedIn" -- because
a number on a company profile should say where it came from, and because
this is the one fact here that does not come from an open register.

Worth being plain about: this reads LinkedIn through r.jina.ai. The page
is public, but automated collection is against LinkedIn's terms, and
this would run for every visitor who looks a company up. That is a
decision for whoever ships it, not a technical detail.
"""
import io
import sys

EDITS = [
    ("""        var links = [];           // where else they are on the record""",
     """        var links = [];           // where else they are on the record
        var li_id = '';           // linkedin, for the headcount fallback"""),

    # keep the id when the links are built
    ("""          [['P4264', 'LinkedIn', 'https://www.linkedin.com/company/'],""",
     """          var li = one('P4264');
          if (typeof li === 'string') li_id = li;

          [['P4264', 'LinkedIn', 'https://www.linkedin.com/company/'],"""),

    # the labels call hands on to the headcount instead of laying out
    ("""              if (where.length) vals.Based = where.join(', ');
              lay_out();
            }, lay_out);""",
     """              if (where.length) vals.Based = where.join(', ');
              head_count();
            }, head_count);"""),

    ("""        function read_more() {
          if (!refs.length) { lay_out(); return; }""",
     """        // the register has no figure for plenty of companies; their own
        // LinkedIn page does
        function head_count() {
          if (vals.People || !li_id) { lay_out(); return; }
          busy = 'counting the team on LinkedIn';
          screen();
          var answered = false;
          function once(n) {
            if (answered) return;
            answered = true;
            if (n) vals.People = n;
            lay_out();
          }
          window.setTimeout(function () { once(''); }, 6000);
          window.fetch('https://r.jina.ai/https://www.linkedin.com/company/' +
                       encodeURIComponent(li_id),
                       { headers: { 'Accept': 'application/json' } })
            .then(function (r) { return r.json(); })
            .then(function (d) {
              var dat = (d && d.data) || d || {};
              var m = String(dat.content || '')
                        .match(/([\\d,]{1,12})\\s*(?:\\+\\s*)?employees/i);
              once(m ? m[1] : '');
            }, function () { once(''); });
        }

        function read_more() {
          if (!refs.length) { head_count(); return; }"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'head_count' not in s, path + ': already counts'
    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    js = s[s.rindex('<script>'):]
    assert 'linkedin.com/company/' in js, path + ': no page to read'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
