# -*- coding: utf-8 -*-
"""The panel opens on step one, because the work starts there.

It used to read the file, parse it and resolve the company while the
hero sat there with a small note, and only then open the flow -- which
is why the first thing anyone saw was "step 5 of 6" with four lines
already ticked. True, but it looked like the flow had started without
them.

The flow opens first now and the reading happens inside it. Each of the
first three lines is on screen as current while the thing it names is
actually happening -- the file being read, the role being pulled out of
it, the company being looked up -- and ticks when it returns. The
lookup then carries on from four. Nothing is replayed and nothing is
faked; the same work simply happens where it can be seen.

Two things that fall out of opening earlier. The checks that can reject
a file on the spot -- too big, a .docx, not a document at all -- move
into a function of their own, so they can run before the flow opens and
a bad file never flashes one up. And a reading that fails later, when
the flow is already open, closes it and says why at the composer, which
is where the file came from.
"""
import io
import sys

# --- the checks, separated so they can run before anything opens -------

SPLIT_OLD = """  var JD_MAX = 8 * 1024 * 1024;
  var JD_PAGES = 12;

  // resolves to text, or rejects with something worth showing a person
  function read_jd(file) {
    if (!file) return Promise.reject(new Error('no file'));
    if (file.size > JD_MAX) {
      return Promise.reject(new Error('That file is over 8MB \\u2014 try the ' +
        'text, or a smaller export.'));
    }
    var name = (file.name || '').toLowerCase();
    if (/\\.(txt|md|text)$/.test(name) || file.type === 'text/plain') {
      return file.text();
    }
    if (/\\.docx?$/.test(name)) {
      return Promise.reject(new Error('I can\\u2019t read Word files yet \\u2014 ' +
        'paste the text, or export it as a PDF.'));
    }
    if (!/\\.pdf$/.test(name) && file.type !== 'application/pdf') {
      return Promise.reject(new Error('That looks like a ' +
        (name.split('.').pop() || 'file') + '. I can read a PDF or text.'));
    }
    return file.arrayBuffer().then(function (buf) {"""

SPLIT_NEW = """  var JD_MAX = 8 * 1024 * 1024;
  var JD_PAGES = 12;

  // what is wrong with this file, said in one line, or '' if nothing is.
  // Answerable without reading it, which is why the flow can wait on it.
  function jd_why_not(file) {
    if (!file) return 'No file there.';
    if (file.size > JD_MAX) {
      return 'That file is over 8MB \\u2014 try the text, or a smaller ' +
        'export.';
    }
    var name = (file.name || '').toLowerCase();
    if (/\\.(txt|md|text)$/.test(name) || file.type === 'text/plain') return '';
    if (/\\.docx?$/.test(name)) {
      return 'I can\\u2019t read Word files yet \\u2014 paste the text, or ' +
        'export it as a PDF.';
    }
    if (!/\\.pdf$/.test(name) && file.type !== 'application/pdf') {
      return 'That looks like a ' + (name.split('.').pop() || 'file') +
        '. I can read a PDF or text.';
    }
    return '';
  }

  // resolves to text, or rejects with something worth showing a person
  function read_jd(file) {
    var no = jd_why_not(file);
    if (no) return Promise.reject(new Error(no));
    var name = (file.name || '').toLowerCase();
    if (/\\.(txt|md|text)$/.test(name) || file.type === 'text/plain') {
      return file.text();
    }
    return file.arrayBuffer().then(function (buf) {"""

# --- the reader's own panel, and the entry rebuilt ---------------------

# find_site and straight_to_lookup live above from_jd and are rewritten
# with it, so the slice starts at the first of the three
OLD_HEAD = "    // a name on the open register, turned into the domain"
OLD_TAIL = "    if (clip && drop_in) {"

NEW_JS = r"""    // ---- the reader's three lines, on screen while they happen -------

    var jd_jobs = [];
    var jd_now = 0;
    // 2 reader steps and 3 lookup ones, or 3 and 3 when the company has
    // to be looked up. Which it is cannot be known until the document has
    // been read, so until then the panel counts without a total rather
    // than naming one it may have to take back.
    var jd_total = 0;

    function jd_paint() {
      if (!flow || flow.hidden) return;
      var card = flow.querySelector('.rec-flow-card');
      if (!card) return;
      card.innerHTML =
        '<h2 class="rec-flow-q is-alone">Reading your job description</h2>' +
        '<div class="rec-work" role="status" aria-live="polite">' +
          '<p class="rec-work-head"><span class="rec-work-dot"></span>' +
            'Mira is working on step ' + Math.min(jd_now + 1, jd_jobs.length) +
            (jd_total ? ' of ' + jd_total : '') + '</p>' +
          jd_jobs.slice(0, jd_now).map(function (say) {
            return '<p class="rec-work-line is-done"><i>✓</i><span>' +
              esc(say) + '</span></p>';
          }).join('') +
          (jd_now < jd_jobs.length
            ? '<p class="rec-work-line is-now"><i>›</i><span>' +
              esc(jd_jobs[jd_now]) + '…</span><b></b></p>'
            : '') +
        '</div>';
    }

    // open on step one: the question screen is drawn and replaced in the
    // same tick, so it is never painted
    function jd_begin(label) {
      jd_jobs = [label];
      jd_now = 0;
      jd_total = 0;
      open();
      step_busy(0);
      jd_paint();
    }

    // the line that was current is done; `say` renames it to what it found
    function jd_tick(say, next) {
      if (say) jd_jobs[jd_now] = say;
      jd_now++;
      if (next) jd_jobs.push(next);
      jd_paint();
    }

    function jd_stop(why) {
      jd_jobs = [];
      jd_now = 0;
      close();
      drop_say(why);
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
                // a country has a website too: ask for something only a
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

    // what the lookup's panel shows as already done, in its own words
    function jd_done_lines() {
      return jd_jobs.slice(0, jd_now);
    }

    function from_jd(text) {
      var got = window.jdParse(text);
      if (!got.title && !got.company && !got.site) {
        jd_stop('I couldn’t find a role or a company in that one. ' +
                'Paste the text instead?');
        return;
      }
      jd = got;
      if (got.title && !field.value.trim()) field.value = got.title;

      // known now: a domain in the document saves a step
      jd_total = (got.site ? 2 : 3) + 3;
      jd_tick(got.title ? 'finding the role: ' + got.title
                        : 'reading what it asks for');

      if (got.site) {
        jd_head = jd_done_lines();
        window.setTimeout(function () { straight_to_lookup(got.site); }, 520);
        return;
      }
      if (!got.company) {          // ask for the website as usual
        jd_jobs = []; jd_now = 0;
        open();
        return;
      }

      // the parse is instant, so its line would be ticked in the same
      // frame it appeared: let it stand before the next one starts
      window.setTimeout(function () {
        if (!flow || flow.hidden) return;
        jd_jobs.push('looking up ' + got.company);
        jd_paint();
        go_find();
      }, 520);
      return;

      function go_find() {
      not_before(520, find_site(got.company)).then(function (host) {
        if (!host) {               // nothing on the register: ask
          jd_jobs = []; jd_now = 0;
          jd_head = [];
          open();
          return;
        }
        jd_tick('looking up ' + got.company + ': ' + host);
        jd_head = jd_done_lines();
        window.setTimeout(function () { straight_to_lookup(host); }, 520);
      });
      }
    }

    // the reading can be quicker than a line can be read. The work is
    // real either way; this only stops it going by unseen.
    function not_before(ms, work) {
      return Promise.all([work, new Promise(function (ok) {
        window.setTimeout(ok, ms);
      })]).then(function (both) { return both[0]; });
    }

    function take_file(file) {
      if (!file) return;
      drop_say('');
      var no = jd_why_not(file);   // answerable now: nothing need open
      if (no) { drop_say(no); return; }

      jd_file = file;
      jd_name = file.name || '';
      jd_begin('reading ' + (file.name || 'the file'));
      not_before(620, read_jd(file)).then(function (text) {
        jd_tick('reading ' + (file.name || 'the file'),
                'finding the role in it');
        from_jd(text);
      }, function (err) {
        jd_stop((err && err.message) || 'I couldn’t read that one.');
      });
    }

    function take_text(text, label) {
      drop_say('');
      jd_file = null;
      jd_name = label;
      jd_begin('reading ' + label.toLowerCase());
      // the text is already here, so this line is true for as long as it
      // takes to read it, which is no time at all
      window.setTimeout(function () {
        jd_tick('reading ' + label.toLowerCase(), 'finding the role in it');
        from_jd(text);
      }, 480);
    }

"""

# --- the two places that handed text in --------------------------------

CALLERS = [
    ("""        var text = dt && dt.getData && dt.getData('text/plain');
        if (text && text.length > 200) {
          jd_file = null;
          jd_name = 'The job description you dropped';
          from_jd(text, 'the text you dropped');
        }""",
     """        var text = dt && dt.getData && dt.getData('text/plain');
        if (text && text.length > 200) {
          take_text(text, 'The job description you dropped');
        }"""),

    ("""        offer.hidden = true;
        jd_file = null;
        jd_name = 'The job description you pasted';
        from_jd(field.value, 'the text you pasted');""",
     """        offer.hidden = true;
        take_text(field.value, 'The job description you pasted');"""),
]

# the reader's note at the composer is the panel's job now
DEAD = """    function drop_busy(on, what) {
      var p = under('rec-drop-note');
      if (!p) return;
      p.textContent = on ? what : '';
      p.hidden = !on;
      if (clip) clip.disabled = !!on;
    }

"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'function jd_begin' not in s, path + ': already starts at one'

    # spliced between escape-free anchors: the lines being replaced carry
    # em-dashes and curly quotes the file stores as characters, which a
    # patch written with \u escapes can never match
    head = "  var JD_MAX = 8 * 1024 * 1024;\n"
    tail = "    return file.arrayBuffer().then(function (buf) {"
    at = s.index(head)
    end = s.index(tail, at)
    assert 'function read_jd' in s[at:end], (path, 'not the reader')
    fresh = SPLIT_NEW[SPLIT_NEW.index(head):SPLIT_NEW.rindex(tail)]
    s = s[:at] + fresh + s[end:]

    at = s.index(OLD_HEAD)
    end = s.index(OLD_TAIL, at)
    assert end > at, (path, 'the entry slice runs backwards')
    s = s[:at] + NEW_JS + s[end:]

    for old, new in CALLERS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    assert s.count(DEAD) == 1, (path, 'the note', s.count(DEAD))
    s = s.replace(DEAD, '', 1)

    # and the style it was the only user of
    dead_css = """    .rec-drop-note { margin:10px 0 0; text-align:center; font-size:12.5px;
                     color:#8A93A6; }
    .rec-drop-note[hidden] { display:none; }
"""
    assert s.count(dead_css) == 1, (path, 'note style', s.count(dead_css))
    s = s.replace(dead_css, '', 1)

    for gone in ['drop_busy', 'rec-drop-note']:
        assert gone not in s, (path, gone + ' survives')
    assert s.count('function find_site') == 1, (path, 'two find_sites')
    assert s.count('function straight_to_lookup') == 1, (path, 'two of those')

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
