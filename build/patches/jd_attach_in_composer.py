# -*- coding: utf-8 -*-
"""The job description attaches to the field, not beside it.

The pill under the composer was a second place to look and a second
thing to explain. The + was already sitting in the composer's own row
doing nothing, which is exactly where a person reaches to attach
something -- so it attaches, and the field itself takes a dropped file.

The decoration becomes a control: it is a real button now, with a label
and a focus ring, because the thing that opens a file picker has to be
reachable from a keyboard.

Where the file goes is said at the moment it matters rather than
standing on the page all the time: the line under the composer appears
while a file is being read, and says it is being read here.
"""
import io
import sys

# the pill, and the line under it, go
DROP_MARKUP_HEAD = '              <div class="rec-drop">'
DROP_MARKUP_TAIL = '              </div>\n'

# the field says what it takes now that it takes a document
SAY_OLD = """                          aria-label="Describe the role, paste a link, or add skills"
                          placeholder="What role are you hiring for?"></textarea>"""

SAY_NEW = """                          aria-label="Upload or paste a job description, or describe the role"
                          placeholder="Upload or paste a JD here"></textarea>"""

# the + becomes the way in, and takes the file input with it
PLUS_OLD = """                  <span class="rec-compose-tools" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>
                    <b>@</b>
                  </span>"""

PLUS_NEW = """                  <span class="rec-compose-tools">
                    <input type="file" class="rec-drop-in" hidden
                           accept=".pdf,.txt,.md,.text,application/pdf,text/plain">
                    <button type="button" class="rec-compose-clip"
                            aria-label="Attach a job description"
                            title="Attach a job description &mdash; read in your browser">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>
                    </button>
                    <b aria-hidden="true">@</b>
                  </span>"""

CSS = """    /* the + attaches a job description */
    .rec-compose-clip { display:inline-flex; align-items:center;
                        justify-content:center; width:26px; height:26px;
                        margin:-4px 0 -4px -5px; padding:0; border:0;
                        border-radius:50%; background:none; color:inherit;
                        cursor:pointer; transition:background .14s,
                                                   color .14s; }
    .rec-compose-clip svg { width:17px; height:17px; display:block; }
    .rec-compose-clip:hover { background:#F1F3F8; color:#4B3BC8; }
    .rec-compose-clip:focus-visible { outline:2px solid #7C5CF6;
                                      outline-offset:2px; }
    /* a file is over the field: the field says so */
    .rec-compose.is-over { border-color:#7C5CF6;
                           box-shadow:0 8px 28px rgba(124,92,246,.18); }
    .rec-compose.is-over::after { opacity:1; }
    .rec-drop-note { margin:10px 0 0; text-align:center; font-size:12.5px;
                     color:#8A93A6; }
    .rec-drop-note[hidden] { display:none; }
    .rec-drop-err { margin:10px 0 0; text-align:center; font-size:12.5px;
                    color:#B4443C; }
    .rec-drop-err[hidden] { display:none; }
    .rec-drop-ask { display:inline-flex; align-items:center; gap:8px;
                    margin:10px auto 0; padding:8px 14px; border-radius:100px;
                    border:1px solid #D8CFF8; background:#F6F3FF;
                    font:inherit; font-size:13px; color:#4B3BC8;
                    cursor:pointer; }
    .rec-drop-ask[hidden] { display:none; }
    .rec-drop-ask:hover { background:#EFEAFF; }
"""

CSS_ANCHOR = "    .rec-compose-wrap { width:100%; max-width:820px; margin:48px auto 0; }"

# --- the wiring moves to the composer ---------------------------------

OLD_WIRE_HEAD = "    // ---- the second way in: a job description ---------"
OLD_WIRE_TAIL = "    form.addEventListener('submit', function (e) {"

NEW_WIRE = r"""    // ---- the second way in: a job description ------------------------
    // It attaches to the composer: the + opens the picker, the field
    // takes a dropped file, and a long paste is offered rather than taken.

    var shelf = document.querySelector('.rec-compose-wrap');
    var clip = shelf && shelf.querySelector('.rec-compose-clip');
    var drop_in = shelf && shelf.querySelector('.rec-drop-in');

    function under(cls) {
      if (!shelf) return null;
      var el = shelf.querySelector('.' + cls);
      if (!el) {
        el = document.createElement('p');
        el.className = cls;
        el.hidden = true;
        shelf.appendChild(el);
      }
      return el;
    }

    function drop_say(msg) {
      var p = under('rec-drop-err');
      if (!p) return;
      p.textContent = msg || '';
      p.hidden = !msg;
    }

    function drop_busy(on, what) {
      var p = under('rec-drop-note');
      if (!p) return;
      p.textContent = on ? what : '';
      p.hidden = !on;
      if (clip) clip.disabled = !!on;
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
      if (!got.company) { open(); return; }   // ask for the website as usual

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
      drop_busy(true, 'Reading ' + (file.name || 'the file') +
                      ' — here, in your browser.');
      read_jd(file).then(function (text) {
        drop_busy(false);
        jd_file = file;
        jd_name = file.name || '';
        from_jd(text, file.name || 'the file');
      }, function (err) {
        drop_busy(false);
        drop_say((err && err.message) || 'I couldn’t read that one.');
      });
    }

    if (clip && drop_in) {
      clip.addEventListener('click', function () { drop_in.click(); });
      drop_in.addEventListener('change', function () {
        take_file(drop_in.files && drop_in.files[0]);
        drop_in.value = '';
      });

      // the field is the target, and the whole composer lights up
      var deep = 0;
      form.addEventListener('dragenter', function (e) {
        e.preventDefault(); deep++; form.classList.add('is-over');
      });
      form.addEventListener('dragover', function (e) { e.preventDefault(); });
      form.addEventListener('dragleave', function () {
        deep = Math.max(0, deep - 1);
        if (!deep) form.classList.remove('is-over');
      });
      form.addEventListener('drop', function (e) {
        e.preventDefault();
        deep = 0;
        form.classList.remove('is-over');
        var dt = e.dataTransfer;
        if (dt && dt.files && dt.files.length) { take_file(dt.files[0]); return; }
        var text = dt && dt.getData && dt.getData('text/plain');
        if (text && text.length > 200) {
          jd_file = null;
          jd_name = 'The job description you dropped';
          from_jd(text, 'the text you dropped');
        }
      });

      // a long paste is probably a JD. Probably is not certain, so it
      // offers rather than takes over.
      var offer = document.createElement('button');
      offer.type = 'button';
      offer.className = 'rec-drop-ask';
      offer.hidden = true;
      offer.textContent = 'That looks like a job description — read it';
      if (shelf) shelf.appendChild(offer);
      offer.addEventListener('click', function () {
        offer.hidden = true;
        jd_file = null;
        jd_name = 'The job description you pasted';
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


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-compose-clip' not in s, path + ': already attaches'

    # out with the pill
    at = s.index(DROP_MARKUP_HEAD)
    end = s.index(DROP_MARKUP_TAIL, s.index('rec-drop-say', at)) + \
        len(DROP_MARKUP_TAIL)
    s = s[:at] + s[end:]
    # the markup goes here; its styles are swept at the end
    assert '<button type="button" class="rec-drop-go">' not in s, \
        path + ': the pill survives'

    assert s.count(PLUS_OLD) == 1, (path, 'the +', s.count(PLUS_OLD))
    s = s.replace(PLUS_OLD, PLUS_NEW, 1)

    assert s.count(SAY_OLD) == 1, (path, 'placeholder', s.count(SAY_OLD))
    s = s.replace(SAY_OLD, SAY_NEW, 1)

    # and the wiring it had
    at = s.index(OLD_WIRE_HEAD)
    end = s.index(OLD_WIRE_TAIL, at)
    s = s[:at] + NEW_WIRE + s[end:]

    # the old pill's styles, now unused
    for dead in ['.rec-drop {', '.rec-drop-go {', '.rec-drop-go svg {',
                 '.rec-drop-go b {', '.rec-drop-go:hover {',
                 '.rec-drop-go:focus-visible {', '.rec-drop-say {',
                 '.rec-drop.is-over .rec-drop-go {',
                 '.rec-drop.is-bad .rec-drop-go {', '.rec-drop-err {',
                 '.rec-drop-err[hidden] {', '.rec-drop-ask {',
                 '.rec-drop-ask[hidden] {', '.rec-drop-ask:hover {']:
        at = s.find('    ' + dead)
        if at < 0:
            continue
        end = s.index('}', at) + 1
        while s[end] == '\n' and s[end + 1:end + 2] != '':
            end += 1
            break
        s = s[:at] + s[end:]

    # and what the sweep leaves behind: two headings over nothing, and a
    # media query for a pill that no longer exists
    for dead in ["""    /* the second door: quieter than the composer on purpose */
""",
                 """    /* a long paste is probably a JD, but that is the visitor's call */
""",
                 """    @media (max-width:640px) {
      .rec-drop-go { font-size:13px; padding:9px 14px; }
    }

"""]:
        assert s.count(dead) == 1, (path, dead.strip()[:40], s.count(dead))
        s = s.replace(dead, '', 1)
    assert 'rec-drop-go' not in s, path + ': a pill style survives'

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS_ANCHOR + '\n' + CSS, 1)

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
