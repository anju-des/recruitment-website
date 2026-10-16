# -*- coding: utf-8 -*-
"""A job description answers the question the flow was going to ask.

The website step exists to get a domain. A JD usually carries one, and
when it does not it carries the company's name, which the same open
register turns into one. Either way the question has been answered
before it is asked, so it is not asked.

Rather than a second route into the lookup, the JD takes the one that
already works: it fills the website step and presses Continue, in the
same tick, so nothing of that screen is ever painted. Every guard on
that path -- the tidy, the shape check, the lookup itself -- applies
unchanged, because it is the same path.

What the reader did before that gets shown, not assumed: the panel opens
with the lines for reading the file and finding the role already ticked,
and the lookup's own three carry on from there. The count says five of
five, not three of three, because five things happened.

A JD with no role and no company in it is not a JD the page can use, and
it says so at the drop zone instead of opening an empty flow.
"""
import io
import sys

# --- the lookup shows what happened before it ------------------------

LOOK_EDITS = [
    ("""      function look() {
        step_busy(0);
        var site = brief.website;""",
     """      function look() {
        step_busy(0);
        var site = brief.website;"""),

    ("""        var ran = [];
        var now = 0;
        var stopped = false;
        var logo = '';""",
     """        // what the JD reader already did, if it was the way in
        var ran = jd_head.map(function (s) { return { say: s }; });
        var pre = ran.length;
        jd_head = [];
        var now = 0;
        var stopped = false;
        var logo = '';"""),

    ("""                (stopped ? 'Mira finished looking'
                         : 'Mira is working on step ' +
                           Math.min(now + 1, jobs.length) + ' of ' +
                           jobs.length) + '</p>' +""",
     """                (stopped ? 'Mira finished looking'
                         : 'Mira is working on step ' +
                           Math.min(ran.length + 1, pre + jobs.length) +
                           ' of ' + (pre + jobs.length)) + '</p>' +"""),
]

# --- the flow keeps what the JD said ---------------------------------

STATE = ("""    // the screens the chips put back, one per step
    var kept = {};""",
         """    // the screens the chips put back, one per step
    var kept = {};
    var jd = null;            // what a job description said, when there was one
    var jd_head = [];         // the reader's own steps, for the lookup's panel""")

# --- the door, wired --------------------------------------------------

WIRE_JS = r"""    // ---- the second way in: a job description ------------------------

    var drop = document.querySelector('.rec-drop');
    var drop_go = drop && drop.querySelector('.rec-drop-go');
    var drop_in = drop && drop.querySelector('.rec-drop-in');

    function drop_say(msg) {
      if (!drop) return;
      var p = drop.querySelector('.rec-drop-err');
      if (!p) {
        p = document.createElement('p');
        p.className = 'rec-drop-err';
        drop.appendChild(p);
      }
      p.textContent = msg || '';
      p.hidden = !msg;
      drop.classList.toggle('is-bad', !!msg);
    }

    function drop_busy(on, what) {
      if (!drop_go) return;
      var label = drop_go.querySelector('span');
      if (!label) return;
      if (on) {
        drop_go.setAttribute('data-was', label.innerHTML);
        label.textContent = what || 'Reading…';
        drop_go.disabled = true;
      } else {
        var was = drop_go.getAttribute('data-was');
        if (was) label.innerHTML = was;
        drop_go.disabled = false;
      }
    }

    // a name on the open register, turned into the domain the lookup wants
    function find_site(name) {
      var API = 'https://www.wikidata.org/w/api.php?origin=*&format=json&';
      return window.fetch(API + 'action=wbsearchentities&type=item&limit=5' +
                          '&language=en&search=' + encodeURIComponent(name))
        .then(function (r) { return r.json(); })
        .then(function (d) {
          var hits = (d && d.search) || [];
          if (!hits.length) return '';
          return window.fetch(API + 'action=wbgetentities&props=claims&ids=' +
                              hits.map(function (h) { return h.id; }).join('|'))
            .then(function (r) { return r.json(); })
            .then(function (e) {
              var all = (e && e.entities) || {};
              for (var i = 0; i < hits.length; i++) {
                var ent = all[hits[i].id];
                if (!ent) continue;
                var c = ent.claims || {};
                // a country has a website too: offer for something only a
                // company carries
                if (!(c.P452 || c.P2088 || c.P4264)) continue;
                var w = c.P856 && c.P856[0].mainsnak.datavalue;
                if (!w) continue;
                return String(w.value).replace(/^https?:\/\//i, '')
                  .replace(/^www\./i, '').replace(/[\/?#].*$/, '')
                  .toLowerCase();
              }
              return '';
            });
        })
        .catch(function () { return ''; });
    }

    // the website step, filled in and sent, in one tick: the screen it
    // belongs to is never painted
    function straight_to_lookup(domain) {
      open();
      if (jd && jd.title) brief.role = jd.title;
      var box = flow.querySelector('.rec-flow-in');
      var on = flow.querySelector('.rec-flow-next');
      if (!box || !on) return;
      box.value = domain;
      box.dispatchEvent(new Event('input', { bubbles: true }));
      on.click();
    }

    function from_jd(text, label) {
      var got = window.jdParse(text);
      if (!got.title && !got.company && !got.site) {
        drop_say('I couldn’t find a role or a company in that one. ' +
                 'Paste the text instead?');
        return;
      }
      drop_say('');
      jd = got;
      if (got.title && !field.value.trim()) field.value = got.title;
      jd_head = ['reading ' + label];
      jd_head.push(got.title ? 'finding the role: ' + got.title
                             : 'reading what it asks for');

      if (got.site) { straight_to_lookup(got.site); return; }
      if (!got.company) { open(); return; }   // offer for the website as usual

      drop_busy(true, 'Looking up ' + got.company + '…');
      find_site(got.company).then(function (host) {
        drop_busy(false);
        if (!host) { jd_head = []; open(); return; }
        jd_head.push('looking up ' + got.company + ': ' + host);
        straight_to_lookup(host);
      });
    }

    function take_file(file) {
      if (!file) return;
      drop_say('');
      drop_busy(true, 'Reading ' + (file.name || 'the file') + '…');
      read_jd(file).then(function (text) {
        drop_busy(false);
        from_jd(text, file.name || 'the file');
      }, function (err) {
        drop_busy(false);
        drop_say((err && err.message) || 'I couldn’t read that one.');
      });
    }

    if (drop_go && drop_in) {
      drop_go.addEventListener('click', function () { drop_in.click(); });
      drop_in.addEventListener('change', function () {
        take_file(drop_in.files && drop_in.files[0]);
        drop_in.value = '';
      });

      // the whole hero is the target: aiming at a 40px pill is not a
      // thing anyone should have to do with a file in hand
      var zone = drop.closest('.rec-compose-wrap') || drop;
      var deep = 0;
      zone.addEventListener('dragenter', function (e) {
        e.preventDefault(); deep++; drop.classList.add('is-over');
      });
      zone.addEventListener('dragover', function (e) { e.preventDefault(); });
      zone.addEventListener('dragleave', function () {
        deep = Math.max(0, deep - 1);
        if (!deep) drop.classList.remove('is-over');
      });
      zone.addEventListener('drop', function (e) {
        e.preventDefault();
        deep = 0;
        drop.classList.remove('is-over');
        var dt = e.dataTransfer;
        if (dt && dt.files && dt.files.length) { take_file(dt.files[0]); return; }
        var text = dt && dt.getData && dt.getData('text/plain');
        if (text && text.length > 200) from_jd(text, 'the text you dropped');
      });

      // a long paste is probably a JD. Probably is not certain, so it
      // offers rather than takes over.
      // not `ask`: that name builds a question screen one scope out
      var offer = document.createElement('button');
      offer.type = 'button';
      offer.className = 'rec-drop-ask';
      offer.hidden = true;
      offer.textContent = 'That looks like a job description — read it';
      drop.appendChild(offer);
      offer.addEventListener('click', function () {
        offer.hidden = true;
        from_jd(field.value, 'the text you pasted');
      });
      field.addEventListener('paste', function (e) {
        var text = e.clipboardData && e.clipboardData.getData('text/plain');
        if (text && text.length > 400) {
          window.setTimeout(function () { offer.hidden = false; }, 0);
        }
      });
      field.addEventListener('input', function () {
        if (field.value.trim().length < 400) offer.hidden = true;
      });
    }

"""

WIRE_ANCHOR = """    form.addEventListener('submit', function (e) {
      e.preventDefault();
      open();
    });"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'from_jd' not in s, path + ': already wired'

    old, new = STATE
    assert s.count(old) == 1, (path, 'state', s.count(old))
    s = s.replace(old, new, 1)

    for old, new in LOOK_EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    assert s.count(WIRE_ANCHOR) == 1, (path, 'wire', s.count(WIRE_ANCHOR))
    s = s.replace(WIRE_ANCHOR, WIRE_JS + WIRE_ANCHOR, 1)

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
