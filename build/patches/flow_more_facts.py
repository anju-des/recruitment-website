# -*- coding: utf-8 -*-
"""Read the whole record, not four fields of it.

Wisemonk's entity carried more than was being shown: its legal name
(Storypeach Technologies Private Limited), what it is (business), and
its LinkedIn and Crunchbase ids. Four properties were being read out of
ten.

Now read: founded, people, type, industry, where, legal form, founder,
chief executive, parent, legal name -- and LinkedIn, Crunchbase and X as
links. Whatever the entity has is shown; whatever it lacks is simply
absent, in a fixed order so two companies never lay out differently for
the same facts.

The item references all resolve in the one call they always did, so the
extra fields cost no extra round trip. The property ids were checked
against Wikidata rather than guessed -- P2088 is Crunchbase, P4264 is
LinkedIn, P31 is "instance of" -- because a mislabelled fact is worse
than a missing one.
"""
import io
import sys

OLD_LINE = """            busy = 'reading industry and location';"""
NEW_LINE = """            busy = 'reading the rest of the record';"""

OLD_VARS = """        var refs = [];            // item ids whose names need a second call"""
NEW_VARS = """        var refs = [];            // item ids whose names need a second call
        var vals = {};            // label -> value, filled from both calls
        var links = [];           // where else they are on the record

        // one order, so two companies never lay out differently
        var ORDER = ['Founded', 'People', 'Type', 'Industry', 'Based',
                     'Legal form', 'Founder', 'CEO', 'Parent', 'Legal name'];"""

OLD_BASE = """        var base = [];            // facts already in hand from the claims"""
NEW_BASE = ""

OLD_SCREEN_FACTS = """            (got.facts && got.facts.length
              ? '<div class="rec-found-facts">' + got.facts.map(function (f) {
                  return '<span><i>' + esc(f[0]) + '</i><b>' + esc(f[1]) +
                    '</b></span>';
                }).join('') + '</div>'
              : '') +"""
NEW_SCREEN_FACTS = """            (got.facts && got.facts.length
              ? '<div class="rec-found-facts">' + got.facts.map(function (f) {
                  return '<span><i>' + esc(f[0]) + '</i><b>' + esc(f[1]) +
                    '</b></span>';
                }).join('') + '</div>'
              : '') +
            (got.facts && links.length
              ? '<div class="rec-found-links">' + links.map(function (l) {
                  return '<a href="' + esc(l[1]) + '" target="_blank" ' +
                    'rel="noreferrer noopener">' + esc(l[0]) + '</a>';
                }).join('') + '</div>'
              : '') +"""

OLD_READ_MORE = """        function read_more() {
          got.facts = base.slice();
          if (!refs.length) { rest(); return; }
          ask_json(API + 'action=wbgetentities&props=labels&languages=en&ids=' +
                   refs.map(function (r) { return r.id; }).join('|'))
            .then(function (d) {
              var all = (d && d.entities) || {};
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
              rest();
            }, rest);
        }"""

NEW_READ_MORE = """        function lay_out() {
          got.facts = ORDER.filter(function (k) { return vals[k]; })
                           .map(function (k) { return [k, vals[k]]; });
          rest();
        }

        function read_more() {
          if (!refs.length) { lay_out(); return; }
          ask_json(API + 'action=wbgetentities&props=labels&languages=en&ids=' +
                   refs.map(function (r) { return r.id; }).join('|'))
            .then(function (d) {
              var all = (d && d.entities) || {};
              var by = {};
              refs.forEach(function (r) {
                var l = all[r.id] && all[r.id].labels && all[r.id].labels.en;
                if (l) by[r.p] = (by[r.p] ? by[r.p] + ', ' : '') + l.value;
              });
              if (by.P31) vals.Type = by.P31;
              if (by.P452) vals.Industry = by.P452;
              if (by.P1454) vals['Legal form'] = by.P1454;
              if (by.P112) vals.Founder = by.P112;
              if (by.P169) vals.CEO = by.P169;
              if (by.P749) vals.Parent = by.P749;
              // the city and its country are one answer, not two facts
              var where = [by.P159, by.P17].filter(function (v, i, a) {
                return v && a.indexOf(v) === i;
              });
              if (where.length) vals.Based = where.join(', ');
              lay_out();
            }, lay_out);
        }"""

OLD_KEEP = """        // what the entity gives us without another call
        function keep_it(ent) {
          var c = ent.claims || {};
          brief_line = (ent.descriptions && ent.descriptions.en &&
                        ent.descriptions.en.value) || '';
          article = (ent.sitelinks && ent.sitelinks.enwiki &&
                     ent.sitelinks.enwiki.title) || '';

          function one(p) {
            return c[p] && c[p][0].mainsnak.datavalue &&
                   c[p][0].mainsnak.datavalue.value;
          }

          var born = one('P571');
          if (born && born.time) base.push(['Founded', born.time.slice(1, 5)]);
          var staff = one('P1128');
          if (staff && staff.amount) {
            base.push(['People',
              Number(String(staff.amount).replace('+', ''))
                .toLocaleString('en')]);
          }
          ['P452', 'P159', 'P17'].forEach(function (p) {
            var v = one(p);
            if (v && v.id) refs.push({ p: p, id: v.id });
          });
        }"""

NEW_KEEP = """        // what the entity gives us without another call
        function keep_it(ent) {
          var c = ent.claims || {};
          brief_line = (ent.descriptions && ent.descriptions.en &&
                        ent.descriptions.en.value) || '';
          article = (ent.sitelinks && ent.sitelinks.enwiki &&
                     ent.sitelinks.enwiki.title) || '';

          function one(p) {
            return c[p] && c[p][0].mainsnak.datavalue &&
                   c[p][0].mainsnak.datavalue.value;
          }

          var born = one('P571');
          if (born && born.time) vals.Founded = born.time.slice(1, 5);
          var staff = one('P1128');
          if (staff && staff.amount) {
            vals.People = Number(String(staff.amount).replace('+', ''))
                            .toLocaleString('en');
          }
          var legal = one('P1448');
          if (legal && legal.text) vals['Legal name'] = legal.text;

          // names of referenced items arrive in the one call that follows
          ['P452', 'P159', 'P17', 'P31', 'P1454', 'P112', 'P169',
           'P749'].forEach(function (p) {
            (c[p] || []).slice(0, 2).forEach(function (claim) {
              var v = claim.mainsnak.datavalue &&
                      claim.mainsnak.datavalue.value;
              if (v && v.id) refs.push({ p: p, id: v.id });
            });
          });

          // and where else the record puts them
          [['P4264', 'LinkedIn', 'https://www.linkedin.com/company/'],
           ['P2088', 'Crunchbase', 'https://www.crunchbase.com/organization/'],
           ['P2002', 'X', 'https://x.com/']].forEach(function (l) {
            var v = one(l[0]);
            if (typeof v === 'string' && v) links.push([l[1], l[2] + v]);
          });
        }"""

CSS = """    .rec-found-links { display:flex; flex-wrap:wrap; justify-content:center;
                       gap:8px; margin-top:14px; }
    .rec-found-links a { padding:6px 13px; border-radius:100px;
                         border:1px solid #E7E2F6; background:#FFFFFF;
                         font-size:12.5px; color:#6B4BE8;
                         text-decoration:none;
                         transition:background .15s, border-color .15s; }
    .rec-found-links a:hover { background:#F7F5FE; border-color:#BCAEF0; }
"""

CSS_ANCHOR = "    .rec-found-facts { display:flex;"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-found-links' not in s, path + ': already widened'
    for old, new in ((OLD_LINE, NEW_LINE), (OLD_VARS, NEW_VARS),
                     (OLD_SCREEN_FACTS, NEW_SCREEN_FACTS),
                     (OLD_READ_MORE, NEW_READ_MORE), (OLD_KEEP, NEW_KEEP)):
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    assert s.count(OLD_BASE + '\n') == 1, (path, 'base', s.count(OLD_BASE))
    s = s.replace(OLD_BASE + '\n', '', 1)

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS + CSS_ANCHOR, 1)

    js = s[s.rindex('<script>'):]
    # not "var base": the dictation code has one of its own
    for gone in ('base.slice(', 'base.push('):
        assert gone not in js, path + ': ' + gone + ' is still there'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
