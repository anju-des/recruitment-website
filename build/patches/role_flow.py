# -*- coding: utf-8 -*-
"""Send opens the brief: location, then budget, then skills, then publish.

Built in script and hung off <body>, like the testimonial sheet and for the
same reason: a fixed element is positioned against its nearest transformed
ancestor rather than the viewport, and this page is full of transforms.

The three questions are one screen each because that is the product's own
argument -- you say the role in a sentence and Mira asks for the rest. The
fourth screen is what it has understood, which is the only screen that could
honestly be called "publish".

Nothing is posted anywhere. The last screen says so in a line, because a
hiring manager who reaches a confirmation that says a role went live has been
told something untrue by a page that was only ever a demonstration.
"""
import io
import sys

CSS = """
    /* ---- the brief ---------------------------------------------------------- */
    /* A screen of its own, over everything. Fixed, so it is hung off <body> in
       script rather than written into a page this full of transforms. */
    .rec-flow[hidden] { display:none; }
    .rec-flow { position:fixed; inset:0; z-index:300; background:#FFFFFF;
                display:flex; flex-direction:column;
                font-size:15px; color:#2C2545;
                animation:rec-flow-in .22s ease both; }
    @keyframes rec-flow-in { from { opacity:0; } to { opacity:1; } }
    .rec-flow.is-out { animation:rec-flow-out .18s ease both; }
    @keyframes rec-flow-out { from { opacity:1; } to { opacity:0; } }
    .rec-flow-head { flex:none; display:flex; align-items:center;
                     justify-content:space-between; gap:16px;
                     padding:clamp(16px, 2.2vw, 26px) clamp(18px, 3vw, 40px); }
    .rec-flow-head img { display:block; width:92px; height:auto; }
    .rec-flow-step { font-size:12.5px; color:#8A82A8; letter-spacing:.01em; }
    .rec-flow-x { width:36px; height:36px; border-radius:50%; border:0;
                  display:grid; place-items:center; cursor:pointer;
                  background:#F2EFFB; color:#4E4470; font-size:19px;
                  line-height:1; font-family:inherit; transition:background .15s; }
    .rec-flow-x:hover { background:#E6E0F7; }
    /* the rail fills as the brief does */
    .rec-flow-bar { flex:none; height:3px; background:#EFECF9; }
    .rec-flow-bar span { display:block; height:100%; background:#7C5CF6;
                         width:var(--at, 25%); transition:width .25s ease; }
    .rec-flow-body { flex:1; min-height:0; overflow:auto;
                     display:flex; align-items:center; justify-content:center;
                     padding:clamp(24px, 4vw, 56px) clamp(18px, 3vw, 40px); }
    .rec-flow-card { width:min(620px, 100%); }
    .rec-flow-q { margin:0 0 10px; color:#1A1430;
                  font-size:clamp(24px, 1.8vw + 14px, 40px); font-weight:600;
                  line-height:1.16; letter-spacing:-0.028em; text-wrap:balance; }
    .rec-flow-hint { margin:0 0 clamp(22px, 2.6vw, 34px); color:#6F6790;
                     font-size:15px; }
    .rec-flow-in { width:100%; box-sizing:border-box; display:block;
                   border:1px solid #DCD6EE; border-radius:12px;
                   padding:15px 18px; font:inherit; font-size:17px;
                   color:#1A1430; background:#FFFFFF; outline:none;
                   transition:border-color .15s, box-shadow .15s; }
    .rec-flow-in::placeholder { color:#A49CC0; }
    .rec-flow-in:focus { border-color:#7C5CF6;
                         box-shadow:0 0 0 3px rgba(124,92,246,.16); }
    .rec-flow-chips { display:flex; flex-wrap:wrap; gap:9px; margin-top:14px; }
    .rec-flow-chip { border:1px solid #DCD6EE; background:#FFFFFF;
                     border-radius:100px; padding:8px 15px; cursor:pointer;
                     font:inherit; font-size:13.5px; color:#4B4270;
                     transition:background .15s, border-color .15s, color .15s; }
    .rec-flow-chip:hover { border-color:#BCAEF0; background:#F7F5FE; }
    .rec-flow-chip.is-on { background:#1A1430; border-color:#1A1430;
                           color:#FFFFFF; }
    /* the skills already added, each with its own way out */
    .rec-flow-tags { display:flex; flex-wrap:wrap; gap:9px; margin-top:14px; }
    .rec-flow-tag { display:inline-flex; align-items:center; gap:8px;
                    background:#F2EFFB; border-radius:100px;
                    padding:8px 9px 8px 15px; font-size:13.5px; color:#2C2545; }
    .rec-flow-tag button { width:18px; height:18px; border-radius:50%; border:0;
                           display:grid; place-items:center; cursor:pointer;
                           background:#DDD6F5; color:#4E4470; font-size:13px;
                           line-height:1; font-family:inherit;
                           transition:background .15s; }
    .rec-flow-tag button:hover { background:#C9BEF0; }
    .rec-flow-act { display:flex; align-items:center; gap:12px;
                    margin-top:clamp(26px, 3vw, 38px); }
    .rec-flow-next, .rec-flow-back {
      border:0; border-radius:10px; padding:13px 26px; cursor:pointer;
      font:inherit; font-size:15px; font-weight:600;
      transition:background .15s, color .15s, opacity .15s; }
    .rec-flow-next { background:#1A1430; color:#FFFFFF; }
    .rec-flow-next:hover { background:#2E2650; }
    .rec-flow-next[disabled] { opacity:.38; cursor:not-allowed;
                               background:#1A1430; }
    .rec-flow-back { background:none; color:#6F6790; padding-inline:8px; }
    .rec-flow-back:hover { color:#1A1430; }
    .rec-flow-skip { margin-left:auto; background:none; border:0; padding:8px;
                     cursor:pointer; font:inherit; font-size:13.5px;
                     color:#8A82A8; transition:color .15s; }
    .rec-flow-skip:hover { color:#4B4270; }
    /* what it has understood */
    .rec-flow-sum { margin:0 0 clamp(24px, 3vw, 34px);
                    border:1px solid #E7E2F6; border-radius:16px;
                    overflow:hidden; }
    .rec-flow-row { display:flex; gap:18px; padding:15px 20px;
                    border-top:1px solid #F0ECFA; }
    .rec-flow-row:first-child { border-top:0; }
    .rec-flow-row dt { flex:none; width:104px; margin:0; color:#8A82A8;
                       font-size:12.5px; letter-spacing:.02em;
                       text-transform:uppercase; padding-top:2px; }
    .rec-flow-row dd { margin:0; color:#1A1430; font-size:15px;
                       line-height:1.5; }
    .rec-flow-row dd em { font-style:normal; color:#A49CC0; }
    .rec-flow-done { text-align:center; }
    .rec-flow-done .rec-flow-tick { width:54px; height:54px; border-radius:50%;
                                    margin:0 auto 20px; display:grid;
                                    place-items:center; background:#EAF7F0;
                                    color:#12B76A; }
    .rec-flow-done .rec-flow-tick svg { width:26px; height:26px; }
    /* it would be a lie to end on a confirmation and leave it at that */
    .rec-flow-note { margin:18px 0 0; color:#8A82A8; font-size:13px; }
    @media (prefers-reduced-motion: reduce) {
      .rec-flow, .rec-flow.is-out { animation:none; }
      .rec-flow-bar span { transition:none; }
    }
    @media (max-width:600px) {
      .rec-flow-row { flex-direction:column; gap:4px; }
      .rec-flow-row dt { width:auto; }
      .rec-flow-act { flex-wrap:wrap; }
    }
"""

JS = r"""
  // Send opens the brief: the role in a sentence is the start of it, and the
  // three things Mira still needs come one screen at a time.
  (function () {
    var form = document.querySelector('.rec-compose');
    var field = document.querySelector('.rec-compose-input');
    if (!form || !field) return;

    var STEPS = [
      { key: 'location',
        q: 'Where is this role based?',
        hint: 'A city, a region, or remote. It is what Mira filters on first.',
        placeholder: 'e.g. Bengaluru, or Remote (India)',
        chips: ['Remote', 'Hybrid', 'On-site'] },
      { key: 'salary',
        q: 'What is the budget?',
        hint: 'A range is fine. Mira keeps every offer inside the band you set.',
        placeholder: 'e.g. 18-24 LPA, or $90k-$120k' },
      { key: 'skills',
        q: 'What must they be good at?',
        hint: 'Add a few. Every application is scored against these as it arrives.',
        placeholder: 'Type a skill and press Enter',
        tags: true }
    ];

    var brief = { role: '', location: '', salary: '', skills: [] };
    var at = 0;
    var flow = null;

    function esc(s) {
      return String(s).replace(/[&<>"]/g, function (c) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
      });
    }

    function build() {
      flow = document.createElement('div');
      flow.className = 'rec-flow';
      flow.hidden = true;
      flow.setAttribute('role', 'dialog');
      flow.setAttribute('aria-modal', 'true');
      flow.setAttribute('aria-label', 'New role');
      flow.innerHTML =
        '<div class="rec-flow-head">' +
          '<img src="mira-logo.svg" width="1152" height="365" alt="Mira">' +
          '<span class="rec-flow-step"></span>' +
          '<button type="button" class="rec-flow-x" aria-label="Close">&#215;</button>' +
        '</div>' +
        '<div class="rec-flow-bar"><span></span></div>' +
        '<div class="rec-flow-body"><div class="rec-flow-card"></div></div>';
      document.body.appendChild(flow);

      flow.querySelector('.rec-flow-x').addEventListener('click', close);
      // the page behind is scroll-driven; it should stay where it was
      flow.addEventListener('wheel', function (e) {
        if (!flow.querySelector('.rec-flow-body').contains(e.target)) e.preventDefault();
      }, { passive: false });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && flow && !flow.hidden) close();
      });
    }

    function open() {
      brief.role = field.value.trim();
      brief.location = '';
      brief.salary = '';
      brief.skills = [];
      at = 0;
      if (!flow) build();
      flow.classList.remove('is-out');
      flow.hidden = false;
      draw();
    }

    function close() {
      if (!flow || flow.hidden) return;
      flow.classList.add('is-out');
      window.setTimeout(function () {
        flow.hidden = true;
        flow.classList.remove('is-out');
      }, 180);
      field.focus();
    }

    function draw() {
      var card = flow.querySelector('.rec-flow-card');
      var total = STEPS.length + 1;
      flow.querySelector('.rec-flow-step').textContent =
        'Step ' + Math.min(at + 1, total) + ' of ' + total;
      flow.querySelector('.rec-flow-bar span').style.setProperty(
        '--at', Math.round((at + 1) / total * 100) + '%');
      card.innerHTML = at < STEPS.length ? ask(STEPS[at]) : review();
      wire(card);
    }

    function ask(step) {
      var val = step.tags ? '' : brief[step.key];
      return '<h2 class="rec-flow-q">' + esc(step.q) + '</h2>' +
        '<p class="rec-flow-hint">' + esc(step.hint) + '</p>' +
        '<input class="rec-flow-in" type="text" value="' + esc(val) + '"' +
        ' placeholder="' + esc(step.placeholder) + '" aria-label="' + esc(step.q) + '">' +
        (step.chips ? '<div class="rec-flow-chips">' + step.chips.map(function (c) {
          return '<button type="button" class="rec-flow-chip' +
            (brief[step.key] === c ? ' is-on' : '') + '">' + esc(c) + '</button>';
        }).join('') + '</div>' : '') +
        (step.tags ? '<div class="rec-flow-tags">' + brief.skills.map(function (s, i) {
          return '<span class="rec-flow-tag">' + esc(s) +
            '<button type="button" data-drop="' + i + '" aria-label="Remove ' +
            esc(s) + '">&#215;</button></span>';
        }).join('') + '</div>' : '') +
        '<div class="rec-flow-act">' +
          (at > 0 ? '<button type="button" class="rec-flow-back">Back</button>' : '') +
          '<button type="button" class="rec-flow-next">Continue</button>' +
          '<button type="button" class="rec-flow-skip">Skip for now</button>' +
        '</div>';
    }

    function review() {
      var rows = [
        ['Role', brief.role],
        ['Location', brief.location],
        ['Budget', brief.salary],
        ['Skills', brief.skills.join(', ')]
      ].map(function (r) {
        return '<div class="rec-flow-row"><dt>' + esc(r[0]) + '</dt><dd>' +
          (r[1] ? esc(r[1]) : '<em>Not given</em>') + '</dd></div>';
      }).join('');
      return '<h2 class="rec-flow-q">Ready to publish.</h2>' +
        '<p class="rec-flow-hint">This is what Mira has. Publish it and every ' +
        'application is read and ranked against it from the moment it lands.</p>' +
        '<dl class="rec-flow-sum">' + rows + '</dl>' +
        '<div class="rec-flow-act">' +
          '<button type="button" class="rec-flow-back">Back</button>' +
          '<button type="button" class="rec-flow-next">Publish role</button>' +
        '</div>';
    }

    function done() {
      flow.querySelector('.rec-flow-bar span').style.setProperty('--at', '100%');
      flow.querySelector('.rec-flow-step').textContent = '';
      flow.querySelector('.rec-flow-card').innerHTML =
        '<div class="rec-flow-done">' +
          '<span class="rec-flow-tick"><svg viewBox="0 0 24 24" fill="none" ' +
            'stroke="currentColor" stroke-width="2.4" stroke-linecap="round" ' +
            'stroke-linejoin="round" aria-hidden="true"><path d="M4 12.5l5 5L20 7"/>' +
          '</svg></span>' +
          '<h2 class="rec-flow-q">The role is live.</h2>' +
          '<p class="rec-flow-hint">Mira takes it from here: it reads every ' +
          'application the day it lands, ranks it against your brief and books ' +
          'the interviews.</p>' +
          '<div class="rec-flow-act" style="justify-content:center">' +
            '<button type="button" class="rec-flow-next">Done</button>' +
          '</div>' +
          '<p class="rec-flow-note">This is a walk-through of the flow. ' +
          'Nothing has been posted.</p>' +
        '</div>';
      flow.querySelector('.rec-flow-next').addEventListener('click', close);
    }

    function wire(card) {
      var step = STEPS[at];
      var input = card.querySelector('.rec-flow-in');
      var next = card.querySelector('.rec-flow-next');
      var back = card.querySelector('.rec-flow-back');
      var skip = card.querySelector('.rec-flow-skip');

      function ready() {
        if (!next || at >= STEPS.length) return;
        var has = step.tags ? brief.skills.length > 0
                            : input.value.trim().length > 0;
        next.disabled = !has;
      }

      function go() {
        if (at < STEPS.length) {
          if (!step.tags) brief[step.key] = input.value.trim();
          if (next.disabled) return;
        }
        if (at >= STEPS.length) { done(); return; }
        at++;
        draw();
      }

      if (input) {
        input.addEventListener('input', ready);
        input.addEventListener('keydown', function (e) {
          if (e.key !== 'Enter') return;
          e.preventDefault();
          if (step.tags) {
            var v = input.value.trim();
            if (!v) return;
            brief.skills.push(v);
            input.value = '';
            draw();
            flow.querySelector('.rec-flow-in').focus();
          } else {
            go();
          }
        });
        input.focus();
      }

      card.querySelectorAll('.rec-flow-chip').forEach(function (chip) {
        chip.addEventListener('click', function () {
          brief[step.key] = chip.textContent;
          input.value = chip.textContent;
          draw();
        });
      });

      card.querySelectorAll('[data-drop]').forEach(function (x) {
        x.addEventListener('click', function () {
          brief.skills.splice(parseInt(x.getAttribute('data-drop'), 10), 1);
          draw();
        });
      });

      if (next) next.addEventListener('click', go);
      if (back) back.addEventListener('click', function () { at--; draw(); });
      if (skip) skip.addEventListener('click', function () {
        if (!step.tags) brief[step.key] = '';
        at++;
        draw();
      });
      ready();
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      open();
    });
  }());
"""

CSS_MARK = "    /* ---- suggestions ------"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-flow' not in s, path + ': already has the flow'

    assert s.count(CSS_MARK) == 1, path + ': suggestions marker changed'
    s = s.replace(CSS_MARK, CSS.lstrip('\n') + '\n' + CSS_MARK, 1)

    i = s.rindex('</script>')
    s = s[:i] + JS + s[i:]

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
