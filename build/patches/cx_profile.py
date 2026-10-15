# -*- coding: utf-8 -*-
"""The reply comes back as a company profile, not as role text.

Three changes, all of a piece:

* The prompt asks for seven labelled lines instead of prose, so the page
  can read it. Website is a bare domain, which is the key to everything
  else -- the logo is fetched from it client-side.

* What comes back lands in its own field, never the role box. The role box
  is for the role; a company profile pasted into it would end up as the
  designation on the review screen.

* Parsed, it becomes a card: logo, name, website, what the company does,
  and who you are. Kept in localStorage so it survives a reload, and
  removable.

The logo comes from Google's favicon service, which needs no key and
returns a 128px PNG for a domain. Clearbit's logo API, the usual choice,
no longer resolves at all. If the fetch fails the card falls back to a
lettered tile rather than a broken image.

Nothing here talks to a server. The profile is the viewer's, held in their
browser, and goes no further until the brief does.
"""
import io
import sys

CSS = """
    /* ---- what comes back from Claude ------------------------------------ */
    .rec-cx-take[hidden], .rec-co[hidden] { display:none; }
    .rec-cx-take { width:100%; max-width:560px; margin:14px auto 0;
                   text-align:left; }
    .rec-cx-take textarea { width:100%; box-sizing:border-box; min-height:92px;
                            resize:vertical; padding:13px 15px;
                            border:1px solid #DCD6EE; border-radius:14px;
                            background:#FFFFFF; font:inherit; font-size:14px;
                            line-height:1.5; color:var(--text-primary); }
    .rec-cx-take textarea:focus { outline:2px solid #7C5CF6;
                                  outline-offset:1px; border-color:#7C5CF6; }
    .rec-cx-take textarea::placeholder { color:#A49CC0; }
    .rec-cx-tip { display:flex; align-items:center; gap:10px; margin:8px 2px 0;
                  font-size:12.5px; color:var(--text-muted); }
    .rec-cx-drop { margin-left:auto; border:0; background:none; padding:2px;
                   font:inherit; font-size:12.5px; color:#8A82A8;
                   cursor:pointer; }
    .rec-cx-drop:hover { color:#5A4BD8; }

    .rec-co { display:flex; gap:14px; width:100%; max-width:560px;
              margin:14px auto 0; padding:16px 18px; box-sizing:border-box;
              border:1px solid rgba(124,92,246,.2); border-radius:16px;
              background:#FFFFFF; text-align:left;
              box-shadow:0 2px 14px rgba(18,22,32,.06); }
    .rec-co-mark { flex:none; width:42px; height:42px; border-radius:11px;
                   display:grid; place-items:center; overflow:hidden;
                   background:linear-gradient(135deg,#8B5CF6,#2684FF);
                   color:#FFFFFF; font-size:18px; font-weight:700; }
    .rec-co-mark img { width:100%; height:100%; object-fit:cover; display:block; }
    .rec-co-body { min-width:0; flex:1; }
    .rec-co-top { display:flex; align-items:baseline; gap:9px;
                  flex-wrap:wrap; }
    .rec-co-top b { font-size:15px; font-weight:700; color:var(--text-primary); }
    .rec-co-top a { font-size:13px; color:#6B4BE8; text-decoration:none; }
    .rec-co-top a:hover { text-decoration:underline; }
    .rec-co-about { margin:5px 0 0; font-size:13.5px; line-height:1.55;
                    color:var(--text-secondary); }
    .rec-co-who { margin:8px 0 0; font-size:12.5px; color:var(--text-muted); }
    .rec-co-who span + span::before { content:"\\00b7"; margin:0 7px;
                                      color:#C6BFE0; }
    .rec-co-x { flex:none; align-self:flex-start; width:26px; height:26px;
                border:0; border-radius:50%; background:none; cursor:pointer;
                color:#A49CC0; font-size:17px; line-height:1;
                transition:background .15s, color .15s; }
    .rec-co-x:hover { background:#F4F1FD; color:#4B4270; }
"""

CSS_ANCHOR = "    /* ---- Mira in the corner ---"

NEW_JS = r"""  // Connect your Claude. It opens claude.ai with a question already in the
  // box; what comes back is seven labelled lines, which this reads into a
  // company profile. Nothing is sent anywhere -- the profile lives in this
  // browser until the brief carries it.
  (function () {
    var row = document.querySelector('.rec-cx-row');
    var ask = row && row.querySelector('.rec-cx');
    if (!row || !ask) return;

    var KEY = 'wm-company';

    // seven lines, because the page has to read this back
    var PROMPT = [
      'I am briefing a role to Wisemonk\'s AI recruiter, Mira. Give it the ' +
        'basics about my company and about me.',
      '',
      'Reply with exactly these seven lines and nothing else:',
      '',
      'Company:',
      'Website:',
      'About:',
      'Size:',
      'Based:',
      'Name:',
      'Role:',
      '',
      'Website is the domain on its own, like example.com. About is one or ' +
        'two sentences on what the company does and who it sells to. Size is ' +
        'roughly how many people work there. Based is where the team works ' +
        'from. Name and Role are mine.',
      '',
      'Use what you already know. If you are unsure of the website, look it ' +
        'up rather than guessing. Leave a value empty if you do not know it ' +
        'and cannot find it.',
      '',
      'No preamble, no extra lines, no questions.'
    ].join('\n');

    var take, card;

    function esc(t) {
      return String(t == null ? '' : t)
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }

    // tolerant of markdown bolding, which Claude adds unasked often enough
    function read(text) {
      var got = {};
      String(text).split(/\r?\n/).forEach(function (line) {
        var m = line.match(
          /^\s*[-*]?\s*\**\s*(company|website|about|size|based|name|role)\s*\**\s*:\s*(.*)$/i);
        if (m) got[m[1].toLowerCase()] = m[2].replace(/\*+$/, '').trim();
      });
      return got;
    }

    function host(w) {
      return String(w || '').trim()
        .replace(/^https?:\/\//i, '').replace(/^www\./i, '')
        .replace(/[\/?#].*$/, '').toLowerCase();
    }

    function keep(co) {
      try { window.localStorage.setItem(KEY, JSON.stringify(co)); } catch (e) {}
    }

    function held() {
      try {
        var raw = window.localStorage.getItem(KEY);
        return raw ? JSON.parse(raw) : null;
      } catch (e) { return null; }
    }

    function show(co) {
      var site = host(co.website);
      var lines = [co.role, co.size, co.based].filter(Boolean);
      var who = co.name ? [esc(co.name)] : [];
      lines.forEach(function (l) { who.push(esc(l)); });

      card.innerHTML =
        '<span class="rec-co-mark">' + esc((co.company || '?').charAt(0)) +
        '</span>' +
        '<div class="rec-co-body">' +
          '<div class="rec-co-top"><b>' + esc(co.company || 'Your company') +
            '</b>' +
            (site ? '<a href="https://' + esc(site) + '" target="_blank" ' +
                    'rel="noreferrer noopener">' + esc(site) + '</a>' : '') +
          '</div>' +
          (co.about ? '<p class="rec-co-about">' + esc(co.about) + '</p>' : '') +
          (who.length ? '<p class="rec-co-who"><span>' +
            who.join('</span><span>') + '</span></p>' : '') +
        '</div>' +
        '<button type="button" class="rec-co-x" aria-label="Remove this ' +
          'profile">×</button>';

      // the mark carries the real logo when the domain yields one, and the
      // first letter when it does not
      if (site) {
        var mark = card.querySelector('.rec-co-mark');
        var img = new Image();
        img.alt = '';
        img.addEventListener('load', function () {
          mark.textContent = '';
          mark.appendChild(img);
        });
        img.src = 'https://www.google.com/s2/favicons?domain=' +
                  encodeURIComponent(site) + '&sz=128';
      }

      card.querySelector('.rec-co-x').addEventListener('click', function () {
        try { window.localStorage.removeItem(KEY); } catch (e) {}
        card.hidden = true;
        take.hidden = true;
        ask.hidden = false;
      });

      ask.hidden = true;
      take.hidden = true;
      card.hidden = false;
    }

    function build() {
      take = document.createElement('div');
      take.className = 'rec-cx-take';
      take.hidden = true;
      take.innerHTML =
        '<textarea aria-label="Claude\'s reply" placeholder="Paste what ' +
          'Claude wrote here"></textarea>' +
        '<p class="rec-cx-tip">Paste the whole reply — Mira reads it ' +
          'into a profile.' +
          '<button type="button" class="rec-cx-drop">Cancel</button></p>';
      row.appendChild(take);

      card = document.createElement('div');
      card.className = 'rec-co';
      card.hidden = true;
      row.appendChild(card);

      var box = take.querySelector('textarea');
      box.addEventListener('input', function () {
        var co = read(box.value);
        if (co.company) { keep(co); show(co); }
      });
      take.querySelector('.rec-cx-drop').addEventListener('click', function () {
        take.hidden = true;
        ask.hidden = false;
      });
    }

    build();

    var already = held();
    if (already && already.company) show(already);

    ask.addEventListener('click', function () {
      window.open('https://claude.ai/new?q=' + encodeURIComponent(PROMPT),
                  '_blank', 'noopener');
      ask.hidden = true;
      take.hidden = false;
      take.querySelector('textarea').focus();
    });
  }());

"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-co-mark' not in s, path + ': already has the profile'

    a = s.index('  // Connect your Claude: straight out to claude.ai')
    b = s.index('  // The hero chip carries two messages')
    s = s[:a] + NEW_JS + s[b:]

    assert s.count(CSS_ANCHOR) == 1, (path, 'css anchor', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS.lstrip('\n') + '\n' + CSS_ANCHOR, 1)

    assert 'Opened in Claude' not in s, path + ': the old row state survives'
    assert 'rec-compose-input' in s, path + ': the role box went missing'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
