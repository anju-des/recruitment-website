# -*- coding: utf-8 -*-
"""Type a company name and it offers the companies it can find.

The field wants a domain, which is a thing people often do not know off
hand -- they know the name. So typing a name now searches the same
register the lookup itself uses and offers what it finds, each row
carrying the domain it would use. Picking one fills the field.

Only entities with an official website are offered. A suggestion whose
domain we do not have is a suggestion that cannot be acted on, and the
whole point of the row is the domain.

Two things keep it honest under a fast typist: each search carries a
sequence number and a late reply from an earlier keystroke is dropped,
so the list can never show results for a word that has been typed past;
and anything containing a dot is treated as a domain already and gets
no suggestions at all.

Three characters before it asks, and a 320ms pause after the last
keystroke, so it is not a request per letter.
"""
import io
import sys

EDITS = [
    ("""      { key: 'website',
        q: 'Let\\'s start with your company',""",
     """      { key: 'website',
        suggest: true,
        q: 'Let\\'s start with your company',"""),

    # the list lives under the field
    ("""          '<input class="rec-flow-in" type="text" value="' + esc(val) + '"' +
          ' placeholder="' + esc(step.placeholder) + '" aria-label="' +
          esc(step.q) + '">') +""",
     """          '<input class="rec-flow-in" type="text" value="' + esc(val) + '"' +
          ' placeholder="' + esc(step.placeholder) + '" aria-label="' +
          esc(step.q) + '" autocomplete="off">' +
          (step.suggest ? '<div class="rec-sug" role="listbox" hidden></div>'
                        : '')) +"""),
]

WIRE_JS = """      var sug = card.querySelector('.rec-sug');
      if (sug && input) {
        var seq = 0;
        var hold = 0;
        var WD = 'https://www.wikidata.org/w/api.php?origin=*&format=json&';

        function shut() { sug.hidden = true; sug.innerHTML = ''; }

        function offer(rows) {
          sug.innerHTML = rows.slice(0, 4).map(function (r) {
            return '<button type="button" class="rec-sug-row" data-host="' +
              esc(r.host) + '"><b>' + esc(r.name) + '</b>' +
              (r.desc ? '<i>' + esc(r.desc) + '</i>' : '') +
              '<span>' + esc(r.host) + '</span></button>';
          }).join('');
          sug.hidden = false;
          sug.querySelectorAll('.rec-sug-row').forEach(function (row) {
            row.addEventListener('click', function () {
              input.value = row.getAttribute('data-host');
              shut();
              input.dispatchEvent(new Event('input', { bubbles: true }));
              input.focus();
            });
          });
        }

        // a late reply from an earlier keystroke must not overwrite a
        // later one, so every search carries its turn
        function search(q) {
          var mine = ++seq;
          window.fetch(WD + 'action=wbsearchentities&type=item&limit=6' +
                       '&language=en&search=' + encodeURIComponent(q))
            .then(function (r) { return r.json(); })
            .then(function (d) {
              if (mine !== seq) return;
              var hits = (d && d.search) || [];
              if (!hits.length) { shut(); return; }
              return window.fetch(WD + 'action=wbgetentities' +
                  '&props=claims|labels|descriptions&languages=en&ids=' +
                  hits.map(function (h) { return h.id; }).join('|'))
                .then(function (r) { return r.json(); })
                .then(function (e) {
                  if (mine !== seq) return;
                  var all = (e && e.entities) || {};
                  var rows = [];
                  hits.forEach(function (h) {
                    var ent = all[h.id];
                    if (!ent) return;
                    var c = ent.claims || {};
                    var w = c.P856 && c.P856[0].mainsnak.datavalue;
                    if (!w) return;          // no domain, nothing to offer
                    var host = String(w.value)
                      .replace(/^https?:\\/\\//i, '').replace(/^www\\./i, '')
                      .replace(/[\\/?#].*$/, '').toLowerCase();
                    if (!host) return;
                    rows.push({
                      host: host,
                      name: (ent.labels && ent.labels.en &&
                             ent.labels.en.value) || h.label || host,
                      desc: (ent.descriptions && ent.descriptions.en &&
                             ent.descriptions.en.value) || ''
                    });
                  });
                  if (!rows.length) { shut(); return; }
                  offer(rows);
                });
            }, shut);
        }

        input.addEventListener('input', function () {
          var q = input.value.trim();
          window.clearTimeout(hold);
          // a dot means they are typing the domain itself
          if (q.length < 3 || q.indexOf('.') > -1) { shut(); return; }
          hold = window.setTimeout(function () { search(q); }, 320);
        });
        input.addEventListener('keydown', function (e) {
          if (e.key === 'Escape') shut();
        });
      }

"""

CSS = """    /* companies offered while the name is being typed */
    .rec-sug[hidden] { display:none; }
    .rec-sug { margin-top:8px; border:1px solid #E7E2F6; border-radius:14px;
               background:#FFFFFF; overflow:hidden;
               box-shadow:0 8px 24px rgba(18,22,32,.08); }
    .rec-sug-row { display:flex; align-items:baseline; gap:10px; width:100%;
                   padding:11px 15px; border:0; border-top:1px solid #F3EFFB;
                   background:none; font:inherit; text-align:left;
                   cursor:pointer; transition:background .12s; }
    .rec-sug-row:first-child { border-top:0; }
    .rec-sug-row:hover, .rec-sug-row:focus-visible { background:#F7F5FE;
                                                     outline:none; }
    .rec-sug-row b { flex:none; font-size:14.5px; font-weight:600;
                     color:#1A1430; }
    .rec-sug-row i { min-width:0; font-style:normal; font-size:12.5px;
                     color:#8A82A8; overflow:hidden;
                     text-overflow:ellipsis; white-space:nowrap; }
    .rec-sug-row span { margin-left:auto; flex:none; font-size:12.5px;
                        color:#6B4BE8; }
"""

CSS_ANCHOR = "    /* the question reads down the same edge every later screen does */"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    # not 'rec-sug': the hero's example list is .rec-suggest
    assert 'rec-sug-row' not in s, path + ': already suggests'

    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    mark = "      var skip = card.querySelector('.rec-flow-skip');\n"
    assert s.count(mark) == 1, (path, 'wire anchor', s.count(mark))
    s = s.replace(mark, WIRE_JS + mark, 1)

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS + CSS_ANCHOR, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
