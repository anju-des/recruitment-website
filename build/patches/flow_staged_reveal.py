# -*- coding: utf-8 -*-
"""The company arrives in three parts, each pause covering a real fetch.

  company card      who it is -- after the domain has been matched
  . thinking        reading the write-up
  about paragraph   Wikipedia's own summary, or the one-line description
  . thinking        reading industry and location
  the details       founded, industry, based, people

The second pause buys something it did not have before: Wikidata's
description is a single clause ("employer of record company in India"),
while the Wikipedia summary for a company that has an article is a real
paragraph. Entities carry an enwiki sitelink when one exists, so the
entity call now asks for it and the fetch only happens when there is
something to fetch. No article, and the line says it looked and the
one-liner stands in.

Both waits have a 520ms floor for the same reason the step lines do: the
work is often faster than the eye, and a line that flashes reads as
decoration rather than as something that happened.

The panel is three steps now instead of four. The fourth used to be
"reading the company details", which is exactly the work that moved onto
this screen.
"""
import io
import sys

JS = r"""      // The lookup, shown as it happens. Every line is a real call; the
      // match is what stops a name search attaching the wrong company to
      // a domain.
      function named(domain) {
        var core = String(domain).split('.')[0].replace(/[-_]+/g, ' ');
        return core.charAt(0).toUpperCase() + core.slice(1);
      }

      function host(w) {
        return String(w || '').trim()
          .replace(/^https?:\/\//i, '').replace(/^www\./i, '')
          .replace(/[\/?#].*$/, '').toLowerCase();
      }

      function look() {
        var site = brief.website;
        var who = named(site);
        var API = 'https://www.wikidata.org/w/api.php?origin=*&format=json&';
        var jobs = [
          'reading ' + site,
          'searching for ' + who,
          'matching the official website'
        ];
        var ran = [];
        var now = 0;
        var stopped = false;
        var logo = '';
        var brief_line = '';      // wikidata's one clause
        var article = '';         // the enwiki title, when there is one
        var refs = [];            // item ids whose names need a second call
        var got = { about: '', facts: null };
        var busy = '';
        var base = [];            // facts already in hand from the claims

        function panel() {
          card.innerHTML =
            '<h2 class="rec-flow-q is-alone">Looking up your company</h2>' +
            '<div class="rec-work" role="status" aria-live="polite">' +
              '<p class="rec-work-head"><span class="rec-work-dot' +
                (stopped ? ' is-off' : '') + '"></span>' +
                (stopped ? 'Mira finished looking'
                         : 'Mira is working on step ' +
                           Math.min(now + 1, jobs.length) + ' of ' +
                           jobs.length) + '</p>' +
              ran.map(function (r) {
                return '<p class="rec-work-line is-done"><i>✓</i><span>' +
                  esc(r.say) + '</span></p>';
              }).join('') +
              (!stopped && now < jobs.length
                ? '<p class="rec-work-line is-now"><i>›</i><span>' +
                  esc(jobs[now]) + '…</span><b></b></p>'
                : '') +
            '</div>';
        }

        function step(say, then) {
          ran.push({ say: say || jobs[now] });
          now++;
          panel();
          window.setTimeout(then, 420);
        }

        function give_up(why) {
          ran.push({ say: why });
          stopped = true;
          panel();
          window.setTimeout(function () { stage(); }, 760);
        }

        // ---- the found screen, filled in in three parts ----------------
        function screen() {
          card.innerHTML =
            '<h2 class="rec-flow-q is-alone">Found your company</h2>' +
            '<div class="rec-flow-found">' +
              '<span class="rec-flow-found-mark">' +
                (logo ? '<img src="' + esc(logo) + '" alt="">'
                      : esc(who.charAt(0))) +
              '</span>' +
              '<span class="rec-flow-found-say"><b>' + esc(who) + '</b>' +
                '<i>' + esc(site) + '</i></span>' +
            '</div>' +
            (got.about
              ? '<p class="rec-found-about">' + esc(got.about) + '</p>' : '') +
            (got.facts && got.facts.length
              ? '<div class="rec-found-facts">' + got.facts.map(function (f) {
                  return '<span><i>' + esc(f[0]) + '</i><b>' + esc(f[1]) +
                    '</b></span>';
                }).join('') + '</div>'
              : '') +
            (busy
              ? '<p class="rec-tell"><i>›</i><span>' + esc(busy) +
                '…</span><b></b></p>'
              : '') +
            (!busy && !got.about && !(got.facts && got.facts.length)
              ? '<p class="rec-found-about is-thin">No public record to ' +
                'read from. Mira will take the rest from you.</p>'
              : '');
        }

        function rest() {
          busy = '';
          screen();
          flow.querySelector('.rec-flow-bar span')
              .style.setProperty('--at', '100%');
        }

        // part one: who. then two real fetches, each behind its own line.
        function stage() {
          screen();
          window.setTimeout(function () {
            busy = article ? 'reading about ' + who
                           : 'looking for a write-up';
            screen();
            window.setTimeout(read_about, 520);
          }, 620);
        }

        function read_about() {
          function then(text) {
            got.about = text || brief_line;
            if (!refs.length && !base.length) { rest(); return; }
            busy = 'reading industry and location';
            screen();
            window.setTimeout(read_more, 520);
          }
          if (!article) { then(''); return; }
          ask_json('https://en.wikipedia.org/api/rest_v1/page/summary/' +
                   encodeURIComponent(article))
            .then(function (d) { then((d && d.extract) || ''); },
                  function () { then(''); });
        }

        function read_more() {
          got.facts = base.slice();
          if (!refs.length) { rest(); return; }
          ask_json(API + 'action=wbgetentities&props=labels&languages=en&ids=' +
                   refs.map(function (r) { return r.id; }).join('|'))
            .then(function (d) {
              var all = (d && d.entities) || {};
              refs.forEach(function (r) {
                var l = all[r.id] && all[r.id].labels && all[r.id].labels.en;
                if (l) {
                  got.facts.push([r.p === 'P452' ? 'Industry' : 'Based',
                                  l.value]);
                }
              });
              rest();
            }, rest);
        }

        function ask_json(url) {
          return window.fetch(url).then(function (r) { return r.json(); });
        }

        panel();

        // 1. the logo, straight off the domain
        var img = new Image();
        var settled = false;
        function logo_done() {
          if (settled) return;
          settled = true;
          step(jobs[0], hunt);
        }
        img.addEventListener('load', function () {
          if (img.naturalWidth >= 64) logo = img.src;
          logo_done();
        });
        img.addEventListener('error', logo_done);
        img.src = 'https://www.google.com/s2/favicons?domain=' +
                  encodeURIComponent(site) + '&sz=128';
        window.setTimeout(logo_done, 3000);

        // 2. who might this be
        function hunt() {
          ask_json(API + 'action=wbsearchentities&type=item&limit=5' +
                   '&language=en&search=' + encodeURIComponent(who))
            .then(function (d) {
              var hits = (d && d.search) || [];
              if (!hits.length) { give_up('no company by that name'); return; }
              step(jobs[1], function () { match(hits); });
            }, function () { give_up('could not reach the register'); });
        }

        // 3. and is it really them? the domain has to agree
        function match(hits) {
          var ids = hits.map(function (h) { return h.id; }).join('|');
          ask_json(API + 'action=wbgetentities&sitefilter=enwiki' +
                   '&props=claims|descriptions|sitelinks&languages=en&ids=' +
                   ids)
            .then(function (d) {
              var all = (d && d.entities) || {};
              var hit = null;
              Object.keys(all).forEach(function (id) {
                if (hit) return;
                var c = (all[id] && all[id].claims) || {};
                var w = c.P856 && c.P856[0].mainsnak.datavalue;
                if (w && host(w.value) === site) hit = all[id];
              });
              if (!hit) { give_up('no public record for ' + site); return; }
              keep_it(hit);
              step(jobs[2], stage);
            }, function () { give_up('could not read the register'); });
        }

        // what the entity gives us without another call
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
          ['P452', 'P159'].forEach(function (p) {
            var v = one(p);
            if (v && v.id) refs.push({ p: p, id: v.id });
          });
        }
      }

"""

CSS = """
    /* the thinking line between the parts of the profile */
    .rec-tell { display:flex; align-items:baseline; justify-content:center;
                gap:9px; margin:18px 0 0;
                font-family:ui-monospace, SFMono-Regular, Menlo, Consolas,
                            monospace;
                font-size:13px; color:#1A1430; }
    .rec-tell i { font-style:normal; color:#7C5CF6; }
    .rec-tell b { display:inline-block; width:7px; height:13px;
                  background:#1A1430; translate:0 1px;
                  animation:rec-work-blink 1s step-end infinite; }
    @media (prefers-reduced-motion: reduce) {
      .rec-tell b { animation:none; }
    }
"""

CSS_ANCHOR = "    /* ---- Mira in the corner ---"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-tell' not in s, path + ': already staged'

    a = s.index('      // The lookup, shown as it happens')
    b = s.index('      function go() {', a)
    s = s[:a] + JS + s[b:]

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS.lstrip('\n') + '\n' + CSS_ANCHOR, 1)

    js = s[s.rindex('<script>'):]
    assert 'wikipedia.org/api/rest_v1' in js, path + ': no write-up fetch'
    assert 'sitefilter=enwiki' in js, path + ': the sitelink is not requested'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
