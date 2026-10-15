# -*- coding: utf-8 -*-
"""Mira in the corner.

A launcher bottom-right, and a panel that opens above it: a greeting, three
things worth asking, and a field. Hung off <body> like the rest of the
overlays on this page, for the same reason -- a fixed element is positioned
against its nearest transformed ancestor, and this page is full of
transforms.

The replies are written, not generated. The page has no model behind it, so
Mira answers from what the page itself already says and hands anything
further to the two places that can actually do something: the brief, and the
product. A widget that improvised would be putting words in the product's
mouth.
"""
import io
import sys

CSS = """
    /* ---- Mira in the corner -------------------------------------------------- */
    .rec-bot-open { position:fixed; z-index:260; right:clamp(16px, 2.4vw, 32px);
                    bottom:clamp(16px, 2.4vw, 32px);
                    width:58px; height:58px; border-radius:50%; border:0;
                    display:grid; place-items:center; cursor:pointer;
                    background:linear-gradient(140deg, #7C5CF6, #5A4BD8);
                    box-shadow:0 10px 26px rgba(58,38,116,.34);
                    transition:transform .16s ease, box-shadow .16s ease; }
    .rec-bot-open:hover { transform:translateY(-2px);
                          box-shadow:0 16px 34px rgba(58,38,116,.42); }
    .rec-bot-open img { width:30px; height:auto; display:block;
                        filter:brightness(0) invert(1); }
    .rec-bot-open.is-on img { opacity:0; }
    /* the mark gives way to a cross while the panel is up */
    .rec-bot-open::after { content:"\\00d7"; position:absolute; color:#fff;
                           font-size:24px; line-height:1; opacity:0;
                           transition:opacity .16s; }
    .rec-bot-open.is-on::after { opacity:1; }

    .rec-bot[hidden] { display:none; }
    .rec-bot { position:fixed; z-index:261; right:clamp(16px, 2.4vw, 32px);
               bottom:calc(clamp(16px, 2.4vw, 32px) + 70px);
               width:min(368px, calc(100vw - 32px));
               max-height:min(560px, calc(100vh - 140px));
               display:flex; flex-direction:column; overflow:hidden;
               border-radius:18px; background:#FFFFFF; color:#2C2545;
               box-shadow:0 26px 60px rgba(20,12,48,.26),
                          0 0 0 1px rgba(124,92,246,.12);
               animation:rec-bot-in .2s ease both; }
    @keyframes rec-bot-in { from { opacity:0; transform:translateY(10px); }
                            to   { opacity:1; transform:none; } }
    .rec-bot.is-out { animation:rec-bot-out .16s ease both; }
    @keyframes rec-bot-out { from { opacity:1; } to { opacity:0; } }
    .rec-bot-head { flex:none; display:flex; align-items:center; gap:10px;
                    padding:15px 18px;
                    border-bottom:1px solid rgba(124,92,246,.14); }
    .rec-bot-head img { width:22px; height:auto; display:block; }
    .rec-bot-head b { font-size:14.5px; font-weight:600; color:#1A1430; }
    .rec-bot-head i { font-style:normal; margin-left:auto; font-size:12px;
                      color:#8A82A8; }
    .rec-bot-log { flex:1; min-height:0; overflow-y:auto;
                   padding:18px; display:flex; flex-direction:column;
                   gap:10px; font-size:14px; line-height:1.55; }
    .rec-bot-msg { max-width:84%; padding:11px 14px; border-radius:14px; }
    .rec-bot-msg.them { align-self:flex-start; background:#F4F1FD;
                        color:#2C2545; border-bottom-left-radius:5px; }
    .rec-bot-msg.you { align-self:flex-end; background:#1A1430; color:#FFFFFF;
                       border-bottom-right-radius:5px; }
    .rec-bot-asks { display:flex; flex-wrap:wrap; gap:7px; margin-top:2px; }
    .rec-bot-ask { border:1px solid #DCD6EE; background:#FFFFFF;
                   border-radius:100px; padding:7px 13px; cursor:pointer;
                   font:inherit; font-size:12.5px; color:#4B4270;
                   transition:background .15s, border-color .15s; }
    .rec-bot-ask:hover { background:#F7F5FE; border-color:#BCAEF0; }
    .rec-bot-say { flex:none; display:flex; gap:8px; align-items:center;
                   padding:12px 14px;
                   border-top:1px solid rgba(124,92,246,.14); }
    .rec-bot-say input { flex:1; min-width:0; border:0; outline:none;
                         background:none; font:inherit; font-size:14px;
                         color:#1A1430; }
    .rec-bot-say input::placeholder { color:#A49CC0; }
    .rec-bot-send { flex:none; width:34px; height:34px; border-radius:50%;
                    border:0; display:grid; place-items:center; cursor:pointer;
                    background:#7C5CF6; color:#fff; transition:background .15s; }
    .rec-bot-send:hover { background:#6B4BE8; }
    .rec-bot-send svg { width:16px; height:16px; }
    @media (prefers-reduced-motion: reduce) {
      .rec-bot, .rec-bot.is-out { animation:none; }
      .rec-bot-open { transition:none; }
      .rec-bot-open:hover { transform:none; }
    }
"""

JS = r"""
  // Mira in the corner. The replies are written, not generated: this page has
  // no model behind it, so she answers from what the page already says and
  // hands anything further to the two places that can act on it -- the brief,
  // and the product. Improvising here would be putting words in its mouth.
  (function () {
    var ASKS = [
      'What does Mira actually do?',
      'How does pricing work?',
      'Start a role'
    ];

    var SAYS = [
      [/price|pricing|cost|fee|charge|pay/i,
       'You pay when someone joins, and nothing before that. No retainer, ' +
       'no fee for a search that does not end in a hire.'],
      [/start|post|create|hire|role|job|vacancy|opening/i,
       'Tell me the role in a sentence and I will ask for the rest. Opening ' +
       'that for you now.'],
      [/interview|schedule|book|calendar|slot/i,
       'I book them. I hold your calendar and the panel\'s, offer the ' +
       'candidate what is actually free, and write the notes up before you ' +
       'are out of the room.'],
      [/score|rank|shortlist|cv|resume|application|screen/i,
       'Every application is read the day it lands and scored against your ' +
       'scorecard. You see a ranked shortlist, not an inbox.'],
      [/what|who|how|do|does|mira/i,
       'I do the work of hiring: read every application as it arrives, rank ' +
       'it against your scorecard, book the interviews and keep the record. ' +
       'The calls stay yours.']
    ];

    var FALL = 'I can tell you what I do, how pricing works, or take the ' +
      'brief for a role. For anything else the team will pick it up at ' +
      'talent.wisemonk.io.';

    var open, panel, log, field;

    function el(tag, cls, text) {
      var n = document.createElement(tag);
      if (cls) n.className = cls;
      if (text) n.textContent = text;
      return n;
    }

    function say(who, text) {
      var m = el('div', 'rec-bot-msg ' + who, text);
      log.appendChild(m);
      log.scrollTop = log.scrollHeight;
      return m;
    }

    function asks() {
      var row = el('div', 'rec-bot-asks');
      ASKS.forEach(function (q) {
        var b = el('button', 'rec-bot-ask', q);
        b.type = 'button';
        b.addEventListener('click', function () { send(q); });
        row.appendChild(b);
      });
      log.appendChild(row);
      log.scrollTop = log.scrollHeight;
    }

    function answer(q) {
      for (var i = 0; i < SAYS.length; i++) {
        if (SAYS[i][0].test(q)) return SAYS[i][1];
      }
      return FALL;
    }

    function send(q) {
      q = (q || '').trim();
      if (!q) return;
      say('you', q);
      field.value = '';
      var row = log.querySelector('.rec-bot-asks');
      if (row) row.remove();
      window.setTimeout(function () {
        say('them', answer(q));
        // the one answer that can do more than say something
        if (/start|post|create|hire|role|job|vacancy|opening/i.test(q)) {
          window.setTimeout(function () {
            close();
            var form = document.querySelector('.rec-compose');
            if (form) {
              form.dispatchEvent(new Event('submit', { cancelable: true,
                                                       bubbles: true }));
            }
          }, 700);
        }
      }, 320);
    }

    function build() {
      panel = el('div', 'rec-bot');
      panel.hidden = true;
      panel.setAttribute('role', 'dialog');
      panel.setAttribute('aria-label', 'Chat with Mira');
      panel.innerHTML =
        '<div class="rec-bot-head">' +
          '<img src="mira-mark.svg" alt="" width="412" height="300">' +
          '<b>Mira</b><i>Usually replies instantly</i>' +
        '</div>' +
        '<div class="rec-bot-log"></div>' +
        '<form class="rec-bot-say">' +
          '<input type="text" aria-label="Ask Mira" ' +
            'placeholder="Ask about hiring with Mira">' +
          '<button type="submit" class="rec-bot-send" aria-label="Send">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
              'stroke-width="2.2" stroke-linecap="round" ' +
              'stroke-linejoin="round" aria-hidden="true">' +
              '<path d="M12 19V5"/><path d="M5 12l7-7 7 7"/></svg>' +
          '</button>' +
        '</form>';
      document.body.appendChild(panel);

      log = panel.querySelector('.rec-bot-log');
      field = panel.querySelector('.rec-bot-say input');
      panel.querySelector('.rec-bot-say').addEventListener('submit', function (e) {
        e.preventDefault();
        send(field.value);
      });

      say('them', 'I am Mira. I read every application, book the interviews ' +
                  'and keep the record. What would you like to know?');
      asks();
    }

    function close() {
      panel.classList.add('is-out');
      open.classList.remove('is-on');
      open.setAttribute('aria-expanded', 'false');
      window.setTimeout(function () {
        panel.hidden = true;
        panel.classList.remove('is-out');
      }, 160);
    }

    open = el('button', 'rec-bot-open');
    open.type = 'button';
    open.setAttribute('aria-label', 'Chat with Mira');
    open.setAttribute('aria-expanded', 'false');
    open.innerHTML = '<img src="mira-mark.svg" alt="" width="412" height="300">';
    document.body.appendChild(open);

    open.addEventListener('click', function () {
      if (!panel) build();
      if (!panel.hidden) { close(); return; }
      panel.classList.remove('is-out');
      panel.hidden = false;
      open.classList.add('is-on');
      open.setAttribute('aria-expanded', 'true');
      field.focus();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && panel && !panel.hidden) close();
    });
  }());
"""

CSS_MARK = "    /* ---- suggestions ------"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-bot' not in s, path + ': already has the bubble'

    assert s.count(CSS_MARK) == 1, path + ': suggestions marker changed'
    s = s.replace(CSS_MARK, CSS.lstrip('\n') + '\n' + CSS_MARK, 1)

    i = s.rindex('</script>')
    s = s[:i] + JS + s[i:]

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
