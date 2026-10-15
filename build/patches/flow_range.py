# -*- coding: utf-8 -*-
"""The budget becomes a band you drag rather than a line you type.

Two native range inputs lying on top of each other, which is what gets a
two-ended slider without hand-rolling pointer maths: the inputs themselves
take no pointer events and only their thumbs do, so a drag always finds the
handle nearest the cursor and the keyboard works for free.

The low handle cannot pass the high one. Clamping rather than swapping,
because a handle that changes identity underneath a held mouse button is a
handle that fights you.
"""
import io
import sys

CSS = """    /* a band you drag: two range inputs stacked, each contributing one end */
    .rec-flow-range { margin-top:4px; }
    .rec-flow-range-val { display:block; color:#1A1430; font-size:30px;
                          font-weight:600; letter-spacing:-0.02em;
                          font-variant-numeric:tabular-nums;
                          margin-bottom:clamp(18px, 2vw, 26px); }
    .rec-flow-range-val small { font-size:17px; font-weight:500;
                                color:#6F6790; margin-left:6px; }
    .rec-flow-track { position:relative; height:26px; }
    .rec-flow-track::before { content:""; position:absolute; left:0; right:0;
                              top:11px; height:4px; border-radius:100px;
                              background:#E7E2F6; }
    .rec-flow-fill { position:absolute; top:11px; height:4px;
                     border-radius:100px; background:#7C5CF6;
                     left:var(--from, 0%); right:var(--to, 0%); }
    /* the inputs are invisible rails; only the thumbs answer the pointer */
    .rec-flow-track input { position:absolute; left:0; top:0; width:100%;
                            height:26px; margin:0; background:none;
                            pointer-events:none; -webkit-appearance:none;
                            appearance:none; }
    .rec-flow-track input:focus { outline:none; }
    .rec-flow-track input::-webkit-slider-thumb {
      -webkit-appearance:none; appearance:none; pointer-events:auto;
      width:22px; height:22px; border-radius:50%; cursor:grab;
      background:#FFFFFF; border:2px solid #7C5CF6;
      box-shadow:0 2px 6px rgba(58,38,116,.22); }
    .rec-flow-track input::-moz-range-thumb {
      pointer-events:auto; width:22px; height:22px; border-radius:50%;
      cursor:grab; background:#FFFFFF; border:2px solid #7C5CF6;
      box-shadow:0 2px 6px rgba(58,38,116,.22); }
    .rec-flow-track input:active::-webkit-slider-thumb { cursor:grabbing; }
    .rec-flow-track input:focus-visible::-webkit-slider-thumb {
      box-shadow:0 0 0 4px rgba(124,92,246,.28); }
    .rec-flow-track input:focus-visible::-moz-range-thumb {
      box-shadow:0 0 0 4px rgba(124,92,246,.28); }
    .rec-flow-ends { display:flex; justify-content:space-between;
                     margin-top:10px; color:#8A82A8; font-size:12.5px;
                     font-variant-numeric:tabular-nums; }
"""

CSS_ANCHOR = """    .rec-flow-chips { display:flex; flex-wrap:wrap; gap:9px; margin-top:14px; }"""

EDITS = [
    ("""      { key: 'salary',
        q: 'What is the budget?',
        hint: 'A range is fine. Mira keeps every offer inside the band you set.',
        placeholder: 'e.g. 18-24 LPA, or $90k-$120k' },""",
     """      { key: 'salary',
        q: 'What is the budget?',
        hint: 'Drag the band. Mira keeps every offer inside it.',
        range: { min: 4, max: 80, step: 1 } },"""),

    ("    var brief = { role: '', location: '', salary: '', skills: [] };",
     """    var brief = { role: '', location: '', salary: '', skills: [] };
    var band = { from: 18, to: 24 };"""),

    # the field, or the band, or neither
    ("""        (step.chipsOnly ? '' :
          '<input class="rec-flow-in" type="text" value="' + esc(val) + '"' +
          ' placeholder="' + esc(step.placeholder) + '" aria-label="' +
          esc(step.q) + '">') +""",
     """        (step.range ? rail(step.range) : step.chipsOnly ? '' :
          '<input class="rec-flow-in" type="text" value="' + esc(val) + '"' +
          ' placeholder="' + esc(step.placeholder) + '" aria-label="' +
          esc(step.q) + '">') +"""),

    ("""    function review() {""",
     """    function money(n, top) {
      return n >= top ? n + '+' : String(n);
    }

    function said(r) {
      return money(band.from, r.max) + '\\u2013' + money(band.to, r.max) + ' LPA';
    }

    function rail(r) {
      return '<div class="rec-flow-range">' +
        '<output class="rec-flow-range-val"></output>' +
        '<div class="rec-flow-track">' +
          '<span class="rec-flow-fill"></span>' +
          '<input type="range" class="rec-flow-lo" min="' + r.min + '" max="' +
            r.max + '" step="' + r.step + '" value="' + band.from +
            '" aria-label="Lowest in the band">' +
          '<input type="range" class="rec-flow-hi" min="' + r.min + '" max="' +
            r.max + '" step="' + r.step + '" value="' + band.to +
            '" aria-label="Highest in the band">' +
        '</div>' +
        '<div class="rec-flow-ends"><span>' + r.min + ' LPA</span><span>' +
          r.max + '+ LPA</span></div>' +
      '</div>';
    }

    function review() {"""),

    ("""        var has = step.tags ? brief.skills.length > 0
                : (input ? input.value.trim().length > 0
                         : !!brief[step.key]);""",
     """        var has = step.range ? true
                : step.tags ? brief.skills.length > 0
                : (input ? input.value.trim().length > 0
                         : !!brief[step.key]);"""),

    ("""        if (at < STEPS.length) {
          if (!step.tags && input) brief[step.key] = input.value.trim();
          if (next && next.disabled) return;
        }""",
     """        if (at < STEPS.length) {
          if (step.range) brief[step.key] = said(step.range);
          else if (!step.tags && input) brief[step.key] = input.value.trim();
          if (next && next.disabled) return;
        }"""),

    # wire the two ends
    ("""      var chips = card.querySelectorAll('.rec-flow-chip');""",
     """      if (step && step.range) {
        var lo = card.querySelector('.rec-flow-lo');
        var hi = card.querySelector('.rec-flow-hi');
        var fill = card.querySelector('.rec-flow-fill');
        var out = card.querySelector('.rec-flow-range-val');
        var span = step.range.max - step.range.min;
        var show = function () {
          // clamped, not swapped: a handle that changes identity under a held
          // mouse button is a handle that fights you
          band.from = Math.min(+lo.value, +hi.value);
          band.to = Math.max(+lo.value, +hi.value);
          if (+lo.value > +hi.value) lo.value = band.from;
          fill.style.setProperty('--from',
            ((band.from - step.range.min) / span * 100).toFixed(2) + '%');
          fill.style.setProperty('--to',
            ((step.range.max - band.to) / span * 100).toFixed(2) + '%');
          out.textContent = said(step.range);
        };
        lo.addEventListener('input', show);
        hi.addEventListener('input', show);
        show();
      }

      var chips = card.querySelectorAll('.rec-flow-chip');"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-flow-track' not in s, path + ': already has the band'

    assert s.count(CSS_ANCHOR) == 1, path + ': chips rule changed'
    s = s.replace(CSS_ANCHOR, CSS + CSS_ANCHOR, 1)

    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:44], s.count(old))
        s = s.replace(old, new, 1)

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
