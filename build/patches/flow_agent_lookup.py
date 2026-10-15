# -*- coding: utf-8 -*-
"""The lookup shows its working, and finds real details.

Every line in the panel is a call that actually happens:

  reading <domain>              the logo
  searching for <Name>          Wikidata wbsearchentities
  matching the official website P856 against the domain they typed
  reading the company details   claims, then labels for the item refs

The third line is the one that matters. A name search alone would hang
somebody else's company off a domain -- "Stripe" also returns a beetle
family and a Gremlins character -- so the entity is kept only when its
official website resolves to the same host. No match, no details, and
the card says so rather than filling in something plausible.

Wikidata because it is free, CORS-open and carries exactly the fields
asked for: employees, industry, headquarters, inception. It only knows
companies somebody has written down, so plenty of domains will come back
with nothing, and that path has to look deliberate rather than broken.

No buttons: it goes on by itself once the details have had time to be
read.
"""
import io
import sys

JS = r"""      // The lookup, shown as it happens. Every line below is a real
      // call; the third is what stops a name search attaching the wrong
      // company to a domain.
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
          'matching the official website',
          'reading the company details'
        ];
        var ran = [];
        var now = 0;
        var logo = '';
        var about = '';
        var facts = [];

        function paint() {
          card.innerHTML =
            '<h2 class="rec-flow-q is-alone">Looking up your company</h2>' +
            '<div class="rec-work" role="status" aria-live="polite">' +
              '<p class="rec-work-head"><span class="rec-work-dot"></span>' +
                'Mira is working on step ' + Math.min(now + 1, jobs.length) +
                ' of ' + jobs.length + '</p>' +
              ran.map(function (r) {
                return '<p class="rec-work-line is-done"><i>' +
                  (r.ok ? '✓' : '×') + '</i><span>' + esc(r.say) +
                  '</span></p>';
              }).join('') +
              (now < jobs.length
                ? '<p class="rec-work-line is-now"><i>›</i><span>' +
                  esc(jobs[now]) + '…</span><b></b></p>'
                : '') +
            '</div>';
        }

        // each line stays up long enough to be read, whatever the network did
        function step(ok, say, then) {
          ran.push({ ok: ok, say: say || jobs[now] });
          now++;
          paint();
          window.setTimeout(then, 420);
        }

        function give_up(why) {
          step(false, why, function () { show(); });
        }

        function show() {
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
            (about ? '<p class="rec-found-about">' + esc(about) + '</p>' : '') +
            (facts.length
              ? '<div class="rec-found-facts">' + facts.map(function (f) {
                  return '<span><i>' + esc(f[0]) + '</i><b>' + esc(f[1]) +
                    '</b></span>';
                }).join('') + '</div>'
              : '<p class="rec-found-about is-thin">No public record to ' +
                'read from. Mira will take the rest from you.</p>');
          brief.company = { name: who, site: site, about: about,
                            facts: facts };
          window.setTimeout(function () {
            if (flow && !flow.hidden) onward();
          }, facts.length ? 3200 : 2200);
        }

        function ask_json(url) {
          return window.fetch(url).then(function (r) { return r.json(); });
        }

        paint();

        // 1. the logo, straight off the domain
        var img = new Image();
        var settled = false;
        function logo_done() {
          if (settled) return;
          settled = true;
          step(true, jobs[0], hunt);
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
              step(true, jobs[1], function () { match(hits); });
            }, function () { give_up('could not reach the register'); });
        }

        // 3. and is it really them? the domain has to agree
        function match(hits) {
          var ids = hits.map(function (h) { return h.id; }).join('|');
          ask_json(API + 'action=wbgetentities&props=claims|descriptions' +
                   '&languages=en&ids=' + ids)
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
              step(true, jobs[2], function () { read(hit); });
            }, function () { give_up('could not read the register'); });
        }

        // 4. what it says about them
        function read(ent) {
          var c = ent.claims || {};
          about = (ent.descriptions && ent.descriptions.en &&
                   ent.descriptions.en.value) || '';

          function one(p) {
            return c[p] && c[p][0].mainsnak.datavalue &&
                   c[p][0].mainsnak.datavalue.value;
          }

          var staff = one('P1128');
          if (staff && staff.amount) {
            facts.push(['People',
              Number(String(staff.amount).replace('+', ''))
                .toLocaleString('en')]);
          }
          var born = one('P571');
          if (born && born.time) facts.push(['Founded', born.time.slice(1, 5)]);

          // industry and headquarters come back as item ids, so their names
          // take one more call
          var refs = [];
          ['P452', 'P159'].forEach(function (p) {
            var v = one(p);
            if (v && v.id) refs.push({ p: p, id: v.id });
          });
          if (!refs.length) { step(true, jobs[3], show); return; }

          ask_json(API + 'action=wbgetentities&props=labels&languages=en&ids=' +
                   refs.map(function (r) { return r.id; }).join('|'))
            .then(function (d) {
              var got = (d && d.entities) || {};
              refs.forEach(function (r) {
                var l = got[r.id] && got[r.id].labels && got[r.id].labels.en;
                if (!l) return;
                facts.push([r.p === 'P452' ? 'Industry' : 'Based', l.value]);
              });
              step(true, jobs[3], show);
            }, function () { step(true, jobs[3], show); });
        }
      }
"""

CSS = """
    /* the lookup, showing its working */
    .rec-work { display:inline-block; margin-top:26px; padding:16px 22px;
                border-radius:14px; background:#F6F5FC; text-align:left;
                font-family:ui-monospace, SFMono-Regular, Menlo, Consolas,
                            monospace;
                font-size:13px; line-height:1.95; color:#6B6392; }
    .rec-work-head { margin:0 0 4px; display:flex; align-items:center;
                     gap:9px; font-weight:600; color:#1A1430; }
    .rec-work-dot { width:8px; height:8px; border-radius:50%; flex:none;
                    background:#12B76A;
                    animation:rec-work-pulse 1.5s ease-in-out infinite; }
    @keyframes rec-work-pulse { 0%,100% { opacity:1 } 50% { opacity:.3 } }
    .rec-work-line { margin:0; display:flex; align-items:baseline; gap:9px; }
    .rec-work-line i { font-style:normal; flex:none; width:10px; }
    .rec-work-line.is-done { color:#9A93B8; }
    .rec-work-line.is-done i { color:#12B76A; }
    .rec-work-line.is-now { color:#1A1430; }
    .rec-work-line.is-now b { display:inline-block; width:7px; height:13px;
                              background:#1A1430; translate:0 1px;
                              animation:rec-work-blink 1s step-end infinite; }
    @keyframes rec-work-blink { 50% { opacity:0 } }

    .rec-found-about { max-width:34ch; margin:16px auto 0; font-size:14px;
                       line-height:1.55; color:var(--text-secondary); }
    .rec-found-about.is-thin { color:var(--text-muted); font-size:13.5px; }
    .rec-found-facts { display:flex; flex-wrap:wrap; justify-content:center;
                       gap:10px; margin-top:18px; }
    .rec-found-facts span { display:flex; flex-direction:column; gap:3px;
                            min-width:104px; padding:11px 16px;
                            border-radius:12px; background:#F6F4FD; }
    .rec-found-facts i { font-style:normal; font-size:11px; color:#8A82A8;
                         letter-spacing:.09em; text-transform:uppercase; }
    .rec-found-facts b { font-size:14.5px; font-weight:600; color:#1A1430; }
    @media (prefers-reduced-motion: reduce) {
      .rec-work-dot, .rec-work-line.is-now b { animation:none; }
    }
    @media (max-width:600px) {
      .rec-work { font-size:12px; padding:14px 16px; }
      .rec-found-facts span { min-width:0; flex:1 1 128px; }
    }
"""

CSS_ANCHOR = "    /* ---- Mira in the corner ---"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-work-line' not in s, path + ': already shows its working'

    a = s.index('      // What the website step does instead of going straight')
    b = s.index('      function go() {', a)
    s = s[:a] + JS + '\n' + s[b:]

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS.lstrip('\n') + '\n' + CSS_ANCHOR, 1)

    assert 'Is this you' not in s, path + ': the old question came back'
    assert 'rec-flow-back">Change' not in s, path + ': Change survives'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
